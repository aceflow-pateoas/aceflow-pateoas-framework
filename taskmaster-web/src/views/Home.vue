<template>
  <div class="home-container">
    <div class="hero-section">
      <div class="hero-content">
        <h1 class="hero-title">
          <el-icon class="hero-icon"><Document /></el-icon>
          TaskMaster
        </h1>
        <p class="hero-subtitle">高效的个人任务管理系统</p>
        <p class="hero-description">
          让您轻松管理日常任务，提升工作效率，实现目标
        </p>
        <div class="hero-buttons">
          <el-button
            v-if="!isAuthenticated"
            type="primary"
            size="large"
            @click="$router.push('/register')"
          >
            开始使用
          </el-button>
          <el-button
            v-if="isAuthenticated"
            type="primary"
            size="large"
            @click="$router.push('/tasks')"
          >
            管理任务
          </el-button>
          <el-button
            v-if="!isAuthenticated"
            size="large"
            @click="$router.push('/login')"
          >
            立即登录
          </el-button>
        </div>
      </div>
    </div>

    <div class="features-section">
      <div class="features-container">
        <h2 class="section-title">核心功能</h2>
        <div class="features-grid">
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon size="40"><Plus /></el-icon>
            </div>
            <h3 class="feature-title">快速创建</h3>
            <p class="feature-description">
              一键创建任务，支持详细描述、优先级设置和截止日期
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon size="40"><Edit /></el-icon>
            </div>
            <h3 class="feature-title">灵活管理</h3>
            <p class="feature-description">
              随时编辑任务状态，支持待办、进行中、已完成状态切换
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon size="40"><Filter /></el-icon>
            </div>
            <h3 class="feature-title">智能筛选</h3>
            <p class="feature-description">
              按状态、优先级、日期等条件筛选，快速找到目标任务
            </p>
          </div>
          
          <div class="feature-card">
            <div class="feature-icon">
              <el-icon size="40"><TrendCharts /></el-icon>
            </div>
            <h3 class="feature-title">进度跟踪</h3>
            <p class="feature-description">
              实时查看任务完成情况，掌握工作进度和效率
            </p>
          </div>
        </div>
      </div>
    </div>

    <div class="cta-section">
      <div class="cta-content">
        <h2 class="cta-title">准备好开始了吗？</h2>
        <p class="cta-description">
          立即注册账户，开始您的高效任务管理之旅
        </p>
        <el-button
          v-if="!isAuthenticated"
          type="primary"
          size="large"
          @click="$router.push('/register')"
        >
          免费注册
        </el-button>
      </div>
    </div>
  </div>
</template>

<script>
import { computed } from 'vue'
import { useAuthStore } from '../stores/auth'

export default {
  name: 'Home',
  setup() {
    const authStore = useAuthStore()
    const isAuthenticated = computed(() => authStore.isAuthenticated)
    
    return {
      isAuthenticated
    }
  }
}
</script>

<style scoped>
.home-container {
  min-height: calc(100vh - 80px);
}

.hero-section {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.hero-content {
  max-width: 800px;
  margin: 0 auto;
}

.hero-title {
  font-size: 3.5rem;
  font-weight: 700;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 15px;
}

.hero-icon {
  font-size: 3.5rem;
}

.hero-subtitle {
  font-size: 1.5rem;
  margin-bottom: 15px;
  opacity: 0.9;
}

.hero-description {
  font-size: 1.1rem;
  margin-bottom: 40px;
  opacity: 0.8;
  line-height: 1.6;
}

.hero-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
  flex-wrap: wrap;
}

.features-section {
  padding: 80px 20px;
  background: #f8f9fa;
}

.features-container {
  max-width: 1200px;
  margin: 0 auto;
}

.section-title {
  text-align: center;
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 60px;
  color: #333;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 40px;
}

.feature-card {
  background: white;
  padding: 40px 30px;
  border-radius: 16px;
  text-align: center;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.feature-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(0, 0, 0, 0.15);
}

.feature-icon {
  width: 80px;
  height: 80px;
  margin: 0 auto 25px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: white;
}

.feature-title {
  font-size: 1.4rem;
  font-weight: 600;
  margin-bottom: 15px;
  color: #333;
}

.feature-description {
  color: #666;
  line-height: 1.6;
  font-size: 1rem;
}

.cta-section {
  background: #333;
  color: white;
  padding: 80px 20px;
  text-align: center;
}

.cta-content {
  max-width: 600px;
  margin: 0 auto;
}

.cta-title {
  font-size: 2.5rem;
  font-weight: 600;
  margin-bottom: 20px;
}

.cta-description {
  font-size: 1.1rem;
  margin-bottom: 40px;
  opacity: 0.9;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
    flex-direction: column;
    gap: 10px;
  }
  
  .hero-icon {
    font-size: 2.5rem;
  }
  
  .hero-subtitle {
    font-size: 1.2rem;
  }
  
  .hero-description {
    font-size: 1rem;
  }
  
  .hero-buttons {
    flex-direction: column;
    align-items: center;
  }
  
  .section-title {
    font-size: 2rem;
  }
  
  .features-grid {
    grid-template-columns: 1fr;
    gap: 30px;
  }
  
  .feature-card {
    padding: 30px 20px;
  }
  
  .cta-title {
    font-size: 2rem;
  }
}
</style>