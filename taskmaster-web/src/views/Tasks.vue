<template>
  <div class="tasks-container">
    <div class="tasks-header">
      <h1 class="tasks-title">
        <el-icon class="title-icon"><List /></el-icon>
        我的任务
      </h1>
      <el-button
        type="primary"
        size="large"
        @click="showCreateDialog = true"
      >
        <el-icon><Plus /></el-icon>
        新建任务
      </el-button>
    </div>

    <div class="tasks-controls">
      <div class="filters">
        <el-select
          v-model="statusFilter"
          placeholder="按状态筛选"
          clearable
          @change="applyFilters"
        >
          <el-option label="全部" value="" />
          <el-option label="待办" value="todo" />
          <el-option label="进行中" value="in_progress" />
          <el-option label="已完成" value="completed" />
        </el-select>
        
        <el-select
          v-model="priorityFilter"
          placeholder="按优先级筛选"
          clearable
          @change="applyFilters"
        >
          <el-option label="全部" value="" />
          <el-option label="高" value="high" />
          <el-option label="中" value="medium" />
          <el-option label="低" value="low" />
        </el-select>
      </div>
      
      <div class="search">
        <el-input
          v-model="searchQuery"
          placeholder="搜索任务..."
          prefix-icon="Search"
          clearable
          @input="applyFilters"
        />
      </div>
    </div>

    <div class="tasks-content">
      <LoadingSpinner v-if="loading" text="正在加载任务..." />
      
      <div v-else-if="filteredTasks.length === 0" class="empty-state">
        <el-icon class="empty-icon"><Document /></el-icon>
        <p class="empty-text">
          {{ tasks.length === 0 ? '暂无任务，创建您的第一个任务吧！' : '没有符合条件的任务' }}
        </p>
      </div>
      
      <div v-else class="tasks-grid">
        <TaskCard
          v-for="task in filteredTasks"
          :key="task.id"
          :task="task"
          @edit="editTask"
          @delete="deleteTask"
          @toggle-status="toggleTaskStatus"
          @duplicate="duplicateTask"
        />
      </div>
    </div>

    <!-- 创建/编辑任务对话框 -->
    <el-dialog
      v-model="showCreateDialog"
      :title="editingTask ? '编辑任务' : '新建任务'"
      width="500px"
    >
      <el-form
        ref="taskFormRef"
        :model="taskFormData"
        :rules="taskRules"
        label-width="80px"
      >
        <el-form-item label="标题" prop="title">
          <el-input
            v-model="taskFormData.title"
            placeholder="请输入任务标题"
            clearable
          />
        </el-form-item>
        
        <el-form-item label="描述">
          <el-input
            v-model="taskFormData.description"
            type="textarea"
            rows="3"
            placeholder="请输入任务描述"
          />
        </el-form-item>
        
        <el-form-item label="优先级">
          <el-select v-model="taskFormData.priority" placeholder="选择优先级">
            <el-option label="高" value="high" />
            <el-option label="中" value="medium" />
            <el-option label="低" value="low" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="状态">
          <el-select v-model="taskFormData.status" placeholder="选择状态">
            <el-option label="待办" value="todo" />
            <el-option label="进行中" value="in_progress" />
            <el-option label="已完成" value="completed" />
          </el-select>
        </el-form-item>
        
        <el-form-item label="截止日期">
          <el-date-picker
            v-model="taskFormData.due_date"
            type="date"
            placeholder="选择截止日期"
            value-format="YYYY-MM-DD"
            style="width: 100%"
          />
        </el-form-item>
      </el-form>
      
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="closeDialog">取消</el-button>
          <el-button type="info" @click="testSave">测试函数</el-button>
          <el-button type="primary" @click="saveTask" :loading="saving">
            {{ saving ? '保存中...' : '保存' }}
          </el-button>
        </span>
      </template>
    </el-dialog>
  </div>
</template>

<script>
import { ref, reactive, computed, onMounted } from 'vue'
import { useTaskStore } from '../stores/task'
import { ElMessage, ElMessageBox } from 'element-plus'
import TaskCard from '../components/TaskCard.vue'
import LoadingSpinner from '../components/LoadingSpinner.vue'

export default {
  name: 'Tasks',
  components: {
    TaskCard,
    LoadingSpinner
  },
  setup() {
    const taskStore = useTaskStore()
    const taskFormRef = ref(null)
    const showCreateDialog = ref(false)
    const editingTask = ref(null)
    const saving = ref(false)
    const statusFilter = ref('')
    const priorityFilter = ref('')
    const searchQuery = ref('')
    
    const taskFormData = reactive({
      title: '',
      description: '',
      priority: 'medium',
      status: 'todo',
      due_date: ''
    })
    
    const taskRules = {
      title: [
        { required: true, message: '请输入任务标题', trigger: 'blur' },
        { min: 1, max: 255, message: '标题长度为1-255个字符', trigger: 'blur' }
      ]
    }
    
    const tasks = computed(() => taskStore.tasks)
    const loading = computed(() => taskStore.loading)
    
    const filteredTasks = computed(() => {
      let filtered = tasks.value
      
      if (statusFilter.value) {
        filtered = filtered.filter(task => task.status === statusFilter.value)
      }
      
      if (priorityFilter.value) {
        filtered = filtered.filter(task => task.priority === priorityFilter.value)
      }
      
      if (searchQuery.value) {
        const query = searchQuery.value.toLowerCase()
        filtered = filtered.filter(task => 
          task.title.toLowerCase().includes(query) ||
          (task.description && task.description.toLowerCase().includes(query))
        )
      }
      
      return filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at))
    })
    
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
        year: 'numeric',
        month: 'short',
        day: 'numeric'
      })
    }
    
    const resetForm = () => {
      Object.assign(taskFormData, {
        title: '',
        description: '',
        priority: 'medium',
        status: 'todo',
        due_date: ''
      })
    }
    
    const closeDialog = () => {
      showCreateDialog.value = false
      editingTask.value = null
      resetForm()
    }
    
    const editTask = (task) => {
      editingTask.value = task
      Object.assign(taskFormData, {
        title: task.title,
        description: task.description || '',
        priority: task.priority,
        status: task.status,
        due_date: task.due_date || ''
      })
      showCreateDialog.value = true
    }
    
    const testSave = () => {
      console.log('testSave called')
      alert('测试函数被调用了！taskFormData: ' + JSON.stringify(taskFormData))
    }
    
    const saveTask = async () => {
      console.log('saveTask called')
      console.log('taskFormRef.value:', taskFormRef.value)
      console.log('taskFormData:', taskFormData)
      
      // 检查必需字段
      if (!taskFormData.title || taskFormData.title.trim() === '') {
        ElMessage.error('任务标题不能为空')
        return
      }
      
      if (!taskFormRef.value) {
        console.error('taskFormRef is null!')
        ElMessage.error('表单引用未找到')
        return
      }
      
      // 准备发送的数据
      const dataToSend = {
        title: taskFormData.title.trim(),
        description: taskFormData.description?.trim() || '',
        priority: taskFormData.priority || 'medium',
        status: taskFormData.status || 'todo',
        due_date: taskFormData.due_date || null
      }
      console.log('Data to send:', dataToSend)
      
      await taskFormRef.value.validate(async (valid) => {
        console.log('Validation result:', valid)
        if (valid) {
          saving.value = true
          try {
            if (editingTask.value) {
              console.log('Updating task:', editingTask.value.id, dataToSend)
              await taskStore.updateTask(editingTask.value.id, dataToSend)
              ElMessage.success('任务更新成功')
            } else {
              console.log('Creating task:', dataToSend)
              await taskStore.createTask(dataToSend)
              ElMessage.success('任务创建成功')
            }
            closeDialog()
          } catch (error) {
            console.error('Save error:', error)
            console.error('Error response:', error.response?.data)
            const errorMsg = error.response?.data?.error || 
                           error.response?.data?.errors?.[0]?.msg || 
                           '保存失败'
            ElMessage.error(errorMsg)
          } finally {
            saving.value = false
          }
        } else {
          console.log('Form validation failed')
          ElMessage.error('请检查表单输入')
        }
      })
    }
    
    const deleteTask = async (id) => {
      try {
        await ElMessageBox.confirm('确定要删除这个任务吗？', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        })
        
        await taskStore.deleteTask(id)
        ElMessage.success('任务删除成功')
      } catch (error) {
        if (error !== 'cancel') {
          ElMessage.error('删除失败')
        }
      }
    }
    
    const toggleTaskStatus = async (task) => {
      const statusMap = {
        todo: 'in_progress',
        in_progress: 'completed',
        completed: 'todo'
      }
      
      console.log('Toggle status for task:', task.id, 'from', task.status, 'to', statusMap[task.status])
      
      try {
        // 只发送允许更新的字段
        const updateData = {
          title: task.title,
          description: task.description,
          status: statusMap[task.status],
          priority: task.priority,
          due_date: task.due_date
        }
        console.log('Update data:', updateData)
        
        await taskStore.updateTask(task.id, updateData)
        ElMessage.success('状态更新成功')
      } catch (error) {
        console.error('Status update error:', error)
        ElMessage.error('状态更新失败')
      }
    }
    
    const duplicateTask = async (task) => {
      try {
        const duplicatedTask = {
          title: `${task.title} (复制)`,
          description: task.description,
          priority: task.priority,
          status: 'todo',
          due_date: task.due_date
        }
        await taskStore.createTask(duplicatedTask)
        ElMessage.success('任务复制成功')
      } catch (error) {
        ElMessage.error('任务复制失败')
      }
    }
    
    const applyFilters = () => {
      // 过滤逻辑在computed中处理
    }
    
    onMounted(() => {
      taskStore.fetchTasks()
    })
    
    return {
      tasks,
      loading,
      filteredTasks,
      showCreateDialog,
      editingTask,
      saving,
      taskFormData,
      taskFormRef,
      taskRules,
      statusFilter,
      priorityFilter,
      searchQuery,
      getStatusType,
      getStatusText,
      getPriorityType,
      getPriorityText,
      formatDate,
      closeDialog,
      editTask,
      testSave,
      saveTask,
      deleteTask,
      toggleTaskStatus,
      duplicateTask,
      applyFilters
    }
  }
}
</script>

<style scoped>
.tasks-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.tasks-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.tasks-title {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 2rem;
  font-weight: 600;
  color: #333;
}

.title-icon {
  font-size: 2rem;
  color: #667eea;
}

.tasks-controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
  gap: 20px;
}

.filters {
  display: flex;
  gap: 15px;
}

.search {
  flex: 1;
  max-width: 300px;
}

.tasks-content {
  min-height: 400px;
}

.empty-state {
  text-align: center;
  padding: 80px 20px;
  color: #999;
}

.empty-icon {
  font-size: 4rem;
  margin-bottom: 20px;
}

.empty-text {
  font-size: 1.1rem;
}

.tasks-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 20px;
  align-items: start;
}

.danger {
  color: #e74c3c;
}

@media (max-width: 768px) {
  .tasks-container {
    padding: 10px;
  }
  
  .tasks-header {
    flex-direction: column;
    gap: 20px;
    align-items: stretch;
  }
  
  .tasks-controls {
    flex-direction: column;
    gap: 15px;
  }
  
  .filters {
    flex-direction: column;
    gap: 10px;
  }
  
  .search {
    max-width: none;
  }
  
  .tasks-grid {
    grid-template-columns: 1fr;
    gap: 15px;
  }
  
  .task-card {
    padding: 15px;
  }
}
</style>