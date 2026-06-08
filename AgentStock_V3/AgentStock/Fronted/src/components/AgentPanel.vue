<template>
  <el-card class="agent-panel" shadow="hover">
    <h3>Agent {{ agentId }}</h3>

    <el-collapse>
      <el-collapse-item title="Prompt 输入">
        <el-input type="textarea" :model-value="prompt" readonly autosize />
      </el-collapse-item>
    </el-collapse>

    <el-divider>收益变化曲线</el-divider>
    <v-chart :option="chartOption" autoresize style="height: 300px" />

    <el-divider>操作记录</el-divider>
    <el-table :data="actions" style="width: 100%">
      <el-table-column prop="day" label="Day" width="80" />
      <el-table-column prop="action" label="操作" width="100" />
      <el-table-column prop="stock" label="股票" />
      <el-table-column prop="amount" label="数量" />
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { use } from 'echarts/core'
import VChart from 'vue-echarts'
import { LineChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, GridComponent } from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'

use([LineChart, TitleComponent, TooltipComponent, GridComponent, CanvasRenderer])

const props = defineProps<{
  agentId: number,
  prompt: string,
  profitCurve: number[],
  actions: {
    day: number,
    action: string,
    stock: string,
    amount: number
  }[]
}>()

const chartOption = computed(() => {
  return {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: props.profitCurve.map((_, i) => `Day ${i + 1}`) },
    yAxis: { type: 'value' },
    series: [
      {
        data: props.profitCurve,
        type: 'line',
        smooth: true,
        name: `Agent ${props.agentId}`
      }
    ]
  }
})
</script>

<style scoped>
.agent-panel {
  margin-bottom: 20px;
}
</style>
