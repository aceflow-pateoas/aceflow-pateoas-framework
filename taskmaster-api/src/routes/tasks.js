const express = require('express');
const { body, validationResult, query } = require('express-validator');
const database = require('../models/database');

const router = express.Router();
const db = database.getDb();

// 获取用户的所有任务
router.get('/', [
  query('status').optional().isIn(['todo', 'in_progress', 'completed']),
  query('priority').optional().isIn(['low', 'medium', 'high']),
  query('page').optional().isInt({ min: 1 }),
  query('limit').optional().isInt({ min: 1, max: 100 })
], async (req, res) => {
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    return res.status(400).json({ errors: errors.array() });
  }

  const { status, priority, page = 1, limit = 10 } = req.query;
  const userId = req.user.userId;
  const offset = (page - 1) * limit;

  try {
    let whereClause = 'WHERE user_id = ?';
    let params = [userId];

    if (status) {
      whereClause += ' AND status = ?';
      params.push(status);
    }

    if (priority) {
      whereClause += ' AND priority = ?';
      params.push(priority);
    }

    const tasks = await new Promise((resolve, reject) => {
      const query = `
        SELECT id, title, description, status, priority, due_date, created_at, updated_at
        FROM tasks 
        ${whereClause}
        ORDER BY created_at DESC
        LIMIT ? OFFSET ?
      `;
      params.push(limit, offset);
      
      db.all(query, params, (err, rows) => {
        if (err) reject(err);
        else resolve(rows);
      });
    });

    // 获取总数
    const totalCount = await new Promise((resolve, reject) => {
      const countQuery = `SELECT COUNT(*) as count FROM tasks ${whereClause}`;
      db.get(countQuery, params.slice(0, -2), (err, row) => {
        if (err) reject(err);
        else resolve(row.count);
      });
    });

    res.json({
      tasks,
      pagination: {
        page: parseInt(page),
        limit: parseInt(limit),
        total: totalCount,
        pages: Math.ceil(totalCount / limit)
      }
    });

  } catch (error) {
    console.error('Get tasks error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 创建新任务
router.post('/', [
  body('title').trim().isLength({ min: 1, max: 255 }),
  body('description').optional().trim(),
  body('priority').optional().isIn(['low', 'medium', 'high']),
  body('due_date').optional().isISO8601().toDate()
], async (req, res) => {
  console.log('=== 创建任务请求 ===');
  console.log('请求体:', req.body);
  console.log('请求头:', req.headers);
  console.log('用户信息:', req.user);
  
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    console.log('验证错误:', errors.array());
    return res.status(400).json({ errors: errors.array() });
  }

  const { title, description, priority = 'medium', due_date } = req.body;
  const userId = req.user.userId;
  
  console.log('提取的数据:', { title, description, priority, due_date, userId });

  try {
    const taskId = await new Promise((resolve, reject) => {
      db.run(
        'INSERT INTO tasks (user_id, title, description, priority, due_date) VALUES (?, ?, ?, ?, ?)',
        [userId, title, description, priority, due_date],
        function(err) {
          if (err) {
            console.error('数据库插入错误:', err);
            reject(err);
          } else {
            console.log('任务插入成功，ID:', this.lastID);
            resolve(this.lastID);
          }
        }
      );
    });

    // 获取创建的任务
    const task = await new Promise((resolve, reject) => {
      db.get(
        'SELECT id, title, description, status, priority, due_date, created_at, updated_at FROM tasks WHERE id = ?',
        [taskId],
        (err, row) => {
          if (err) reject(err);
          else resolve(row);
        }
      );
    });

    res.status(201).json({
      message: 'Task created successfully',
      task
    });

  } catch (error) {
    console.error('Create task error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 更新任务状态
router.put('/:id', [
  body('title').optional().trim().isLength({ min: 1, max: 255 }),
  body('description').optional().trim(),
  body('status').optional().isIn(['todo', 'in_progress', 'completed']),
  body('priority').optional().isIn(['low', 'medium', 'high']),
  // 移除 due_date 的验证，在后面手动处理
], async (req, res) => {
  console.log('=== 更新任务请求 ===');
  console.log('任务ID:', req.params.id);
  console.log('请求体:', req.body);
  console.log('用户信息:', req.user);
  
  const errors = validationResult(req);
  if (!errors.isEmpty()) {
    console.log('验证错误:', errors.array());
    return res.status(400).json({ errors: errors.array() });
  }

  const taskId = req.params.id;
  const userId = req.user.userId;
  const updates = req.body;

  try {
    // 检查任务是否存在且属于当前用户
    const existingTask = await new Promise((resolve, reject) => {
      db.get(
        'SELECT id FROM tasks WHERE id = ? AND user_id = ?',
        [taskId, userId],
        (err, row) => {
          if (err) reject(err);
          else resolve(row);
        }
      );
    });

    if (!existingTask) {
      return res.status(404).json({ error: 'Task not found' });
    }

    // 构建更新查询
    const updateFields = [];
    const params = [];
    
    Object.keys(updates).forEach(key => {
      if (updates[key] !== undefined) {
        updateFields.push(`${key} = ?`);
        params.push(updates[key]);
      }
    });

    if (updateFields.length === 0) {
      return res.status(400).json({ error: 'No valid fields to update' });
    }

    updateFields.push('updated_at = CURRENT_TIMESTAMP');
    params.push(taskId, userId);

    await new Promise((resolve, reject) => {
      const query = `UPDATE tasks SET ${updateFields.join(', ')} WHERE id = ? AND user_id = ?`;
      db.run(query, params, function(err) {
        if (err) reject(err);
        else resolve();
      });
    });

    // 获取更新后的任务
    const updatedTask = await new Promise((resolve, reject) => {
      db.get(
        'SELECT id, title, description, status, priority, due_date, created_at, updated_at FROM tasks WHERE id = ?',
        [taskId],
        (err, row) => {
          if (err) reject(err);
          else resolve(row);
        }
      );
    });

    res.json({
      message: 'Task updated successfully',
      task: updatedTask
    });

  } catch (error) {
    console.error('Update task error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// 删除任务
router.delete('/:id', async (req, res) => {
  const taskId = req.params.id;
  const userId = req.user.userId;

  try {
    const result = await new Promise((resolve, reject) => {
      db.run(
        'DELETE FROM tasks WHERE id = ? AND user_id = ?',
        [taskId, userId],
        function(err) {
          if (err) reject(err);
          else resolve(this.changes);
        }
      );
    });

    if (result === 0) {
      return res.status(404).json({ error: 'Task not found' });
    }

    res.json({ message: 'Task deleted successfully' });

  } catch (error) {
    console.error('Delete task error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

module.exports = router;