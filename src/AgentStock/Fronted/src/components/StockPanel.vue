<template>
  <el-card>
    <div slot="header" style="display: flex; justify-content: space-between; align-items: center;">
      <h3>股票 {{ stockId }}: {{ stockName }}</h3>
    </div>
    
    <!-- K线图 -->
    <div style="height: 300px; margin-bottom: 20px;">
      <v-chart :option="priceChartOption" autoresize />
    </div>
    
    <!-- 每日价格表格 -->
    <el-table :data="priceData" border style="width: 100%">
      <el-table-column prop="day" label="天数" width="80" />
      <el-table-column prop="open" label="开盘价" />
      <el-table-column prop="close" label="收盘价" />
      <el-table-column prop="high" label="最高价" />
      <el-table-column prop="low" label="最低价" />
    </el-table>
  </el-card>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { use } from 'echarts/core'
import VChart from 'vue-echarts'
import { CandlestickChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { TooltipComponent, GridComponent } from 'echarts/components'

// 注册K线图所需组件
use([
  CandlestickChart,
  TooltipComponent,
  GridComponent,
  CanvasRenderer
])

// 接收父组件传递的参数
const props = defineProps({
  stockId: {
    type: Number,
    required: true
  },
  stockName: {
    type: String,
    required: true
  },
  priceData: {
    type: Array,
    required: true,
    default: () => []
  }
})

// K线图配置
const priceChartOption = computed(() => {
  return {
    title: {
      text: `${props.stockName} K线图`,
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      },
      formatter: params => {
        const data = params[0].data
        return `
          天数: ${params[0].name}<br/>
          开盘: ${data[0]}<br/>
          最高: ${data[3]}<br/>
          最低: ${data[2]}<br/>
          收盘: ${data[1]}
        `
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: props.priceData.map(item => item.day),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      name: '价格',
      scale: true // 自动调整刻度以适应K线范围
    },
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        // K线数据格式: [开盘价, 收盘价, 最低价, 最高价]
        data: props.priceData.map(item => [
          item.open,
          item.close,
          item.high,
          item.low
        ]),
        itemStyle: {
          color: '#ef232a', // 上涨颜色(收盘价 > 开盘价)
          color0: '#14b143', // 下跌颜色(收盘价 <= 开盘价)
          borderColor: '#ef232a',
          borderColor0: '#14b143'
        },
        emphasis: {
          itemStyle: {
            shadowBlur: 10,
            shadowColor: 'rgba(0,0,0,0.3)'
          }
        }
      }
    ]
  }
})
</script>

<style scoped>
/* 可自定义组件样式 */
</style>