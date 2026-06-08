<template>
  <el-container direction="vertical">
    <el-header>
      <h2>📈 模拟详情</h2>
    </el-header>
    <el-main>
      <!-- 加载状态 -->
      <div v-if="loading" style="text-align: center; padding: 50px;">
        <el-icon class="is-loading" size="30">
          <Loading />
        </el-icon>
        <p style="margin-top: 10px;">正在加载模拟结果...</p>
      </div>
      
      <!-- 错误状态 -->
      <el-alert
        v-if="error && !loading"
        :title="error"
        type="warning"
        show-icon
        style="margin-bottom: 20px;"
      />
      
      <!-- 数据展示 -->
      <el-row :gutter="20" v-for="agent in agents" :key="agent.id" style="margin-bottom: 20px">
        <el-col :span="24">
          <agent-panel
            :agent-id="agent.id"
            :prompt="agent.prompt"
            :profit-curve="agent.profitCurve"
            :actions="agent.actions"
          />
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import AgentPanel from '../components/AgentPanel.vue'
import { ref, onMounted } from 'vue'
import { Loading } from '@element-plus/icons-vue'
import http from '../utils/http'

const agents = ref([])
const loading = ref(true)
const error = ref('')

// 获取模拟结果数据
const fetchSimulationResults = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await http.get('/api/simulation_results', {
      params: {
        simulation_id: 'sim01' // 可以根据需要动态设置
      }
    })
    
    if (response.data.status === 'success') {
      agents.value = response.data.data.agents
    } else {
      error.value = response.data.message || '获取数据失败'
      // 如果API失败，使用默认数据
      agents.value = [
        {
          id: 1,
          prompt: 'You are an agent deciding on AAPL for day 1...',
          profitCurve: [100000, 101200, 102500, 103000],
          actions: [
            { day: 1, action: 'BUY', stock: 'AAPL', amount: 100 },
            { day: 2, action: 'SELL', stock: 'AAPL', amount: 100 },
          ]
        },
        {
          id: 2,
          prompt: 'You are an agent deciding on MSFT for day 1...',
          profitCurve: [100000, 99700, 100300, 101500],
          actions: [
            { day: 1, action: 'BUY', stock: 'MSFT', amount: 150 },
            { day: 3, action: 'SELL', stock: 'MSFT', amount: 150 },
          ]
        }
      ]
    }
  } catch (err) {
    console.error('获取模拟结果失败:', err)
    error.value = '网络请求失败'
    // 使用默认数据作为后备
    agents.value = [
      {
        id: 1,
        prompt: 'You are an agent deciding on AAPL for day 1...',
        profitCurve: [100000, 101200, 102500, 103000],
        actions: [
          { day: 1, action: 'BUY', stock: 'AAPL', amount: 100 },
          { day: 2, action: 'SELL', stock: 'AAPL', amount: 100 },
        ]
      },
      {
        id: 2,
        prompt: 'You are an agent deciding on MSFT for day 1...',
        profitCurve: [100000, 99700, 100300, 101500],
        actions: [
          { day: 1, action: 'BUY', stock: 'MSFT', amount: 150 },
          { day: 3, action: 'SELL', stock: 'MSFT', amount: 150 },
        ]
      }
    ]
  } finally {
    loading.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchSimulationResults()
})
</script>

<style scoped>
el-header {
  margin-bottom: 20px;
}
</style>
