<template>
  <el-container>
    <el-header>
      <h2>📊 AI 股票预测模拟系统</h2>
    </el-header>
    <el-main>
      <el-form :model="form">
        <el-form-item label="模拟天数">
          <el-input-number v-model="form.days" :min="1" :max="365" />
        </el-form-item>

        <el-form-item label="Agent数量 (Num_Person)">
          <el-slider v-model="form.persons" :min="1" :max="12" show-input />
        </el-form-item>

        <el-form-item label="股票数量 (Num_Stock)">
          <el-slider v-model="form.stocks" :min="1" :max="10" show-input />
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="test" :loading="isLoading" :disabled="isLoading">
            {{ isLoading ? '仿真进行中...' : '开始模拟' }}
          </el-button>
          <el-button @click="resetForm">重置参数</el-button>
        </el-form-item>
      </el-form>
      <el-divider>模拟进度</el-divider>
      <el-progress :percentage="progress" :status="progressStatus" style="width: 400px" />

      <!-- 添加loading提示 -->
      <div v-if="isLoading" style="margin-top: 20px; text-align: center;">
        <el-icon class="is-loading" size="20" style="margin-right: 8px;">
          <Loading />
        </el-icon>
        <span style="color: #409EFF;">正在执行仿真，请耐心等待...</span>
      </div>
    </el-main>
  </el-container>
</template>

<script lang="ts" setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { Loading } from '@element-plus/icons-vue'
import http from '../utils/http'

const router = useRouter()
// 默认值
const form = reactive({
  days: 30,
  persons: 3,
  stocks: 3
})

const progress = ref(0)
const progressStatus = ref<'success' | 'exception' | 'warning' | 'active'>('active')
const isLoading = ref(false)

function submitSimulation() {
  progress.value = 10
  progressStatus.value = 'active'

  // 模拟异步调用，可替换为后端请求提交任务并跳转页面
  setTimeout(() => {
    progress.value = 100
    progressStatus.value = 'success'
    router.push('/simulation')
  }, 1000)
}

async function test() {
  try {
    // 开始loading状态
    isLoading.value = true
    progress.value = 10
    progressStatus.value = 'active'

    const res = await http.get('/api/paraminit', {
      params: {
        No_Days: form.days,
        Num_Person: form.persons,
        Num_Stock: form.stocks
      }
    })

    console.log(res)

    // 检查响应状态
    if (res.data.status === 'success') {
      // 仿真完成，直接设置为100%
      progress.value = 100
      progressStatus.value = 'success'

      // 跳转到模拟页面
      setTimeout(() => {
        router.push('/simulation')
      }, 500)

    } else {
      // 处理错误情况
      progress.value = 0
      progressStatus.value = 'exception'
      console.error('初始化失败:', res.data.message)
      // 这里可以添加错误提示
    }

  } catch (error) {
    progress.value = 0
    progressStatus.value = 'exception'
    console.error('请求失败:', error)
    // 这里可以添加错误提示
  } finally {
    // 结束loading状态
    isLoading.value = false
  }
}

</script>

<style scoped>
el-container {
  padding: 20px;
}
</style>
