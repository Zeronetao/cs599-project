<template>
  <el-container direction="vertical">
    <el-header>
      <h2>📊 Agent 策略对比</h2>
    </el-header>
    <el-main>
      <!-- 加载状态 -->
      <div v-if="loading" style="text-align: center; padding: 50px;">
        <el-icon class="is-loading" size="30">
          <Loading />
        </el-icon>
        <p style="margin-top: 10px;">正在加载对比数据...</p>
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
      <template v-if="!loading">
        <el-card>
          <h3>收益曲线对比</h3>
          <v-chart :option="chartOption" autoresize style="height: 400px" />
        </el-card>

        <el-card style="margin-top: 20px">
          <h3>最终收益排行</h3>
          <el-table :data="rankedAgents" style="width: 100%">
            <el-table-column prop="id" label="Agent ID" width="100" />
            <el-table-column prop="finalValue" label="最终收益" />
          </el-table>
        </el-card>
      </template>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { use } from 'echarts/core'
import VChart from 'vue-echarts'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { Loading } from '@element-plus/icons-vue'
import http from '../utils/http'

use([LineChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, CanvasRenderer])

const agents = ref([])
const dayLabels = ref([])
const loading = ref(true)
const error = ref('')

// 获取Agent对比数据
const fetchAgentComparison = async () => {
  try {
    loading.value = true
    error.value = ''
    
    const response = await http.get('/api/agent_comparison')
    
    if (response.data.status === 'success') {
      agents.value = response.data.data.agents
      dayLabels.value = response.data.data.dayLabels
    } else {
      error.value = response.data.message || '获取对比数据失败'
      // 如果API失败，使用默认数据
      agents.value = [
        {
          id: 1,
          profitCurve: [100000, 101200, 102500, 103000],
          finalValue: 103000
        },
        {
          id: 2,
          profitCurve: [100000, 99700, 100300, 101500],
          finalValue: 101500
        },
        {
          id: 3,
          profitCurve: [100000, 100500, 100800, 102000],
          finalValue: 102000
        }
      ]
      dayLabels.value = ['Day 1', 'Day 2', 'Day 3', 'Day 4']
    }
  } catch (err) {
    console.error('获取Agent对比数据失败:', err)
    error.value = '网络请求失败'
    // 使用默认数据作为后备
    agents.value = [
      {
        id: 1,
        profitCurve: [100000, 101200, 102500, 103000],
        finalValue: 103000
      },
      {
        id: 2,
        profitCurve: [100000, 99700, 100300, 101500],
        finalValue: 101500
      },
      {
        id: 3,
        profitCurve: [100000, 100500, 100800, 102000],
        finalValue: 102000
      }
    ]
    dayLabels.value = ['Day 1', 'Day 2', 'Day 3', 'Day 4']
  } finally {
    loading.value = false
  }
}

const chartOption = computed(() => {
  return {
    tooltip: { trigger: 'axis' },
    legend: { data: agents.value.map(a => `Agent ${a.id}`) },
    xAxis: { type: 'category', data: dayLabels.value },
    yAxis: { type: 'value' },
    series: agents.value.map(agent => ({
      name: `Agent ${agent.id}`,
      type: 'line',
      data: agent.profitCurve
    }))
  }
})

const rankedAgents = computed(() => {
  return [...agents.value].sort((a, b) => b.finalValue - a.finalValue)
})

// 组件挂载时获取数据
onMounted(() => {
  fetchAgentComparison()
})
</script>

<style scoped>
el-header {
  margin-bottom: 20px;
}
</style>
