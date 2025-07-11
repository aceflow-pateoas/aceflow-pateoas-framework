<template>
  <div class="task-card-wrapper">
    <div 
      class="task-card"
      :class="{ 
        'completed': task.status === 'completed',
        'high-priority': task.priority === 'high',
        'due-soon': isDueSoon
      }"
    >
      <div class="task-header">
        <div class="task-status-indicator">
          <span 
            class="status-dot"
            :class="getStatusClass(task.status)"
            @click="$emit('toggle-status', task)"
          ></span>
        </div>
        <h3 class="task-title" @click="$emit('edit', task)">{{ task.title }}</h3>
        <el-dropdown>
          <el-icon class="task-menu"><MoreFilled /></el-icon>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item @click="$emit('edit', task)">
                <el-icon><Edit /></el-icon>
                编辑
              </el-dropdown-item>
              <el-dropdown-item @click="$emit('duplicate', task)">
                <el-icon><CopyDocument /></el-icon>
                复制
              </el-dropdown-item>
              <el-dropdown-item divided @click="$emit('delete', task.id)" class="danger">
                <el-icon><Delete /></el-icon>
                删除
              </el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
      </div>
      
      <p class="task-description">{{ task.description || '暂无描述' }}</p>
      
      <div class="task-meta">
        <el-tag
          :type="getStatusType(task.status)"
          size="small"
          @click="$emit('toggle-status', task)"
          class="clickable-tag"
        >
          {{ getStatusText(task.status) }}
        </el-tag>
        
        <el-tag
          :type="getPriorityType(task.priority)"
          size="small"
          effect="plain"
          class="priority-tag"
        >
          <el-icon><Flag /></el-icon>
          {{ getPriorityText(task.priority) }}
        </el-tag>
      </div>
      
      <div class="task-footer">
        <div class="task-dates">
          <span class="task-date">
            <el-icon><Clock /></el-icon>
            {{ formatDate(task.created_at) }}
          </span>
          <span v-if="task.due_date" class="task-due" :class="{ 'overdue': isOverdue }">
            <el-icon><Calendar /></el-icon>
            截止：{{ formatDate(task.due_date) }}
          </span>
        </div>
        <div class="task-actions">
          <el-button 
            size="small" 
            type="text" 
            @click="$emit('toggle-status', task)"
            :disabled="task.status === 'completed'"
          >
            {{ getNextStatusText(task.status) }}
          </el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'

export default {
  name: 'TaskCard',
  props: {
    task: {
      type: Object,
      required: true
    }
  },
  emits: ['edit', 'delete', 'toggle-status', 'duplicate'],
  setup(props) {
    const isDueSoon = computed(() => {
      if (!props.task.due_date) return false
      const dueDate = new Date(props.task.due_date)
      const today = new Date()
      const diffTime = dueDate - today
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays <= 3 && diffDays >= 0
    })
    
    const isOverdue = computed(() => {
      if (!props.task.due_date) return false
      const dueDate = new Date(props.task.due_date)
      const today = new Date()
      return dueDate < today && props.task.status !== 'completed'
    })
    
    const getStatusClass = (status) => {
      return `status-${status}`
    }
    
    const getStatusType = (status) => {
      const types = {
        todo: '',
        in_progress: 'warning',
        completed: 'success'
      }
      return types[status] || ''
    }
    
    const getStatusText = (status) => {
      const texts = {
        todo: '待办',
        in_progress: '进行中',
        completed: '已完成'
      }
      return texts[status] || status
    }
    
    const getNextStatusText = (status) => {
      const texts = {
        todo: '开始',
        in_progress: '完成',
        completed: '重新开始'
      }
      return texts[status] || '更新'
    }
    
    const getPriorityType = (priority) => {
      const types = {
        high: 'danger',
        medium: 'warning',
        low: 'info'
      }
      return types[priority] || ''
    }
    
    const getPriorityText = (priority) => {
      const texts = {
        high: '高',
        medium: '中',
        low: '低'
      }
      return texts[priority] || priority
    }
    
    const formatDate = (dateString) => {
      if (!dateString) return ''
      const date = new Date(dateString)
      return date.toLocaleDateString('zh-CN', {
        month: 'short',
        day: 'numeric'
      })
    }
    
    return {
      isDueSoon,
      isOverdue,
      getStatusClass,
      getStatusType,
      getStatusText,
      getNextStatusText,
      getPriorityType,
      getPriorityText,
      formatDate
    }
  }
}
</script>

<style scoped>
.task-card-wrapper {
  height: 100%;
}

.task-card {
  background: white;
  border-radius: 16px;
  padding: 20px;
  height: 100%;
  display: flex;
  flex-direction: column;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
  border: 1px solid #f0f0f0;
  position: relative;
  overflow: hidden;
}

.task-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: #e9ecef;
  transition: all 0.3s ease;
}

.task-card.high-priority::before {
  background: linear-gradient(180deg, #ff6b6b 0%, #feca57 100%);
}

.task-card.due-soon::before {
  background: linear-gradient(180deg, #ff9ff3 0%, #f368e0 100%);
}

.task-card:hover {
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.12);
  transform: translateY(-2px);
}

.task-card.completed {
  opacity: 0.8;
  background: #f8f9fa;
}

.task-header {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  margin-bottom: 15px;
}

.task-status-indicator {
  margin-top: 2px;
}

.status-dot {
  width: 12px;
  height: 12px;
  border-radius: 50%;
  display: block;
  cursor: pointer;
  transition: all 0.2s;
  border: 2px solid transparent;
}

.status-dot:hover {
  transform: scale(1.2);
}

.status-todo {
  background-color: #909399;
}

.status-in_progress {
  background-color: #e6a23c;
  animation: pulse 2s infinite;
}

.status-completed {
  background-color: #67c23a;
}

@keyframes pulse {
  0% { opacity: 1; }
  50% { opacity: 0.7; }
  100% { opacity: 1; }
}

.task-title {
  font-size: 1.1rem;
  font-weight: 600;
  color: #333;
  margin: 0;
  flex: 1;
  line-height: 1.4;
  cursor: pointer;
  transition: color 0.2s;
}

.task-title:hover {
  color: #667eea;
}

.task-card.completed .task-title {
  text-decoration: line-through;
  color: #999;
}

.task-menu {
  color: #999;
  cursor: pointer;
  padding: 4px;
  border-radius: 4px;
  transition: all 0.2s;
}

.task-menu:hover {
  background: #f0f0f0;
  color: #333;
}

.task-description {
  color: #666;
  margin-bottom: 15px;
  line-height: 1.5;
  flex: 1;
  font-size: 0.9rem;
}

.task-meta {
  display: flex;
  gap: 8px;
  margin-bottom: 15px;
  flex-wrap: wrap;
}

.clickable-tag {
  cursor: pointer;
  transition: all 0.2s;
}

.clickable-tag:hover {
  opacity: 0.8;
  transform: scale(1.05);
}

.priority-tag {
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-footer {
  border-top: 1px solid #f0f0f0;
  padding-top: 15px;
  margin-top: auto;
}

.task-dates {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 10px;
}

.task-date,
.task-due {
  font-size: 0.85rem;
  color: #999;
  display: flex;
  align-items: center;
  gap: 4px;
}

.task-due {
  color: #e6a23c;
  font-weight: 500;
}

.task-due.overdue {
  color: #f56565;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  10%, 90% { transform: translate3d(-1px, 0, 0); }
  20%, 80% { transform: translate3d(2px, 0, 0); }
  30%, 50%, 70% { transform: translate3d(-4px, 0, 0); }
  40%, 60% { transform: translate3d(4px, 0, 0); }
}

.task-actions {
  display: flex;
  justify-content: flex-end;
}

.danger {
  color: #f56565;
}

@media (max-width: 768px) {
  .task-card {
    padding: 15px;
  }
  
  .task-title {
    font-size: 1rem;
  }
  
  .task-meta {
    flex-direction: column;
    gap: 5px;
  }
}
</style>