<template>
  <div style="padding: 20px;">
    <h3>表单测试</h3>
    <p>输入值: {{ formData.title }}</p>
    <input v-model="formData.title" placeholder="测试输入" />
    <br><br>
    <p>描述: {{ formData.description }}</p>
    <textarea v-model="formData.description" placeholder="测试描述"></textarea>
    <br><br>
    <button @click="showData">显示数据</button>
    <pre>{{ JSON.stringify(formData, null, 2) }}</pre>
  </div>
</template>

<script>
import { reactive } from 'vue'

export default {
  name: 'FormTest',
  setup() {
    const formData = reactive({
      title: '',
      description: ''
    })
    
    const showData = () => {
      console.log('Form Data:', formData)
      alert(JSON.stringify(formData, null, 2))
    }
    
    return {
      formData,
      showData
    }
  }
}
</script>