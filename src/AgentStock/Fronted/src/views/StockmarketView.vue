<template>
  <el-container direction="vertical">
    <el-header>
      <h2>📈 股票 K 线图</h2>
      <!-- 股票选择器 -->
      <el-select 
        v-model="selectedStockId" 
        @change="handleStockChange"
        style="margin-top: 10px; width: 200px;"
      >
        <el-option 
          v-for="stock in allStocks" 
          :key="stock.id" 
          :label="stock.name" 
          :value="stock.id"
        />
      </el-select>
    </el-header>
    <el-main>
      <!-- 加载状态 -->
      <div v-if="loading" style="text-align: center; padding: 50px; position: relative; z-index: 10;">
        <el-icon class="is-loading" size="30">
          <LoadingIcon />
        </el-icon>
        <p style="margin-top: 10px;">正在加载股票数据...</p>
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
      <el-card v-if="!loading || priceData.length > 0" class="stock-card">
        <h3>股票 {{ selectedStockId }}: {{ stockName }}</h3>
        <!-- K线图 -->
        <div style="height: 400px; margin-bottom: 20px;">
          <v-chart :option="priceChartOption" autoresize />
        </div>
        
        <!-- 每日价格表格 -->
        <el-table 
          :data="priceData" 
          border 
          style="width: 100%"
          class="price-table"
        >
          <el-table-column prop="day" label="天数" width="80" />
          <el-table-column prop="open" label="开盘价" />
          <el-table-column prop="close" label="收盘价" />
          <el-table-column prop="high" label="最高价" />
          <el-table-column prop="low" label="最低价" />
        </el-table>
      </el-card>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { use } from 'echarts/core'
import VChart from 'vue-echarts'
import { CandlestickChart, LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { 
  TooltipComponent, 
  GridComponent, 
  TitleComponent,
  LegendComponent
} from 'echarts/components'
import { Loading as LoadingIcon } from '@element-plus/icons-vue'
import http from '../utils/http'

// 注册组件
use([
  CandlestickChart,
  LineChart,
  TooltipComponent,
  GridComponent,
  TitleComponent,
  LegendComponent,
  CanvasRenderer
])

// 父组件传参
const props = defineProps({
  stockId: {
    type: Number,
    required: true
  }
})

// 状态管理
const stockName = ref('')
const priceData = ref([])
const loading = ref(true)
const error = ref('')
const selectedStockId = ref(props.stockId)
const allStocks = ref([])

// 默认数据
const setDefaultData = () => {
  stockName.value = '默认股票 (数据加载失败)'
  priceData.value = [
    { day: 1, open: 100, close: 102, high: 105, low: 99 },
    { day: 2, open: 102, close: 105, high: 107, low: 101 },
    { day: 3, open: 105, close: 103, high: 106, low: 102 },
    { day: 4, open: 103, close: 108, high: 110, low: 102 },
    { day: 5, open: 108, close: 106, high: 109, low: 105 }
  ]
}
setDefaultData()

// 获取数据
const fetchStockData = async () => {
  try {
    loading.value = true;
    const response = await http.get('/api/stock_data', {
      params: { stock_id: selectedStockId.value }
    })
    console.log('后端返回数据:', response.data)

    if (response.data.status === 'success' && response.data.data?.stocks) {
      allStocks.value = response.data.data.stocks;
      const currentStock = response.data.data.stocks.find(
        (stock: any) => stock.id === selectedStockId.value
      );
      
      if (currentStock) {
        stockName.value = currentStock.name;
        priceData.value = currentStock.prices;
      } else {
    
        setDefaultData();
      }
    } else {
      error.value = response.data.message || '股票数据异常';
      setDefaultData();
    }
  } catch (err) {
    error.value = '网络请求失败';
    setDefaultData();
  } finally {
    loading.value = false;
  }
};

// 切换股票
const handleStockChange = (newStockId: number) => {
  selectedStockId.value = newStockId;
  fetchStockData();
};

// K线图配置（核心优化部分）
const priceChartOption = computed(() => {
  return {
    // 标题优化
    title: {
      text: `${stockName.value} K线图`,
      left: 'center',
      textStyle: {
        fontSize: 16,
        fontWeight: 'bold',
        color: '#333'
      },
      padding: [10, 0, 20, 0] // 增加底部间距
    },
    // 提示框优化
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'cross', // 十字光标，更精准
        lineStyle: {
          color: '#ccc',
          width: 1,
          type: 'dashed'
        }
      },
      backgroundColor: 'rgba(255, 255, 255, 0.9)', // 半透明白色背景
      borderColor: '#ddd',
      borderWidth: 1,
      padding: 10,
      textStyle: { color: '#333' },
      formatter: params => {
        const data = params[0]?.data || [];
        return `
          <div style="font-weight: bold;">${params[0]?.name || '未知'}</div>
          <div>开盘: ${data[1]?.toFixed(2) || '0.00'}</div>
          <div>最高: ${data[3]?.toFixed(2) || '0.00'}</div>
          <div>最低: ${data[4]?.toFixed(2) || '0.00'}</div>
          <div>收盘: ${data[2]?.toFixed(2) || '0.00'}</div>
        `;
      }
    },
    // 网格布局优化（让图表更居中）
    grid: {
      left: '5%',
      right: '5%',
      bottom: '10%',
      top: '15%',
      containLabel: true
    },
    // X轴优化
    xAxis: {
      type: 'category',
      data: priceData.value.map(item => `Day ${item.day}`), // 显示为"Day 1"更直观
      axisLine: { lineStyle: { color: '#ddd' } }, // 轴线颜色
      axisTick: { show: false }, // 隐藏刻度线
      axisLabel: {
        color: '#666',
        interval: 0, // 强制显示所有标签
        rotate: 0 // 标签不旋转（避免拥挤）
      },
      splitLine: { show: false } // 隐藏X轴网格线
    },
    // Y轴优化
    yAxis: {
      type: 'value',
      name: '价格',
      nameTextStyle: { color: '#666' },
      axisLine: { show: false }, // 隐藏轴线
      axisTick: { show: false }, // 隐藏刻度线
      axisLabel: {
        color: '#666',
        formatter: '{value}' // 保持数值原样
      },
      splitLine: {
        lineStyle: {
          color: '#f0f0f0', // 浅灰色网格线
          type: 'dashed' // 虚线网格，不抢眼
        }
      },
      scale: true,
      // 控制Y轴刻度间隔，避免数值密集时重叠
      minInterval: 1
    },
    // K线样式核心优化
    series: [
      {
        name: 'K线',
        type: 'candlestick',
        data: priceData.value.map(item => [
          item.open,
          item.close,
          item.high,
          item.low
        ]),
        // 调整K线宽度，避免过宽或过窄
        itemStyle: {
          color: '#ef232a', // 上涨红色
          color0: '#14b143', // 下跌绿色
          borderColor: '#ef232a',
          borderColor0: '#14b143',
          borderWidth: 1 // 边框细一点更精致
        },
        // 蜡烛图宽度比例（0-1）
        barWidth: '60%', // 占格子宽度的60%，避免拥挤
        barMaxWidth: 30, // 最大宽度限制
        // 鼠标悬停效果
        emphasis: {
          itemStyle: {
            shadowBlur: 8,
            shadowColor: 'rgba(0,0,0,0.4)', // 深色阴影，突出当前K线
            borderWidth: 2 // 悬停时边框加粗
          }
        }
      }
    ]
  }
})

// 初始化加载
onMounted(() => {
  fetchStockData()
})
</script>

<style scoped>
el-header {
  margin-bottom: 20px;
  padding: 15px 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

/* 卡片样式优化 */
.stock-card {
  border: none;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08); /* 轻微阴影，提升层次感 */
  border-radius: 6px;
  overflow: hidden;
}

.stock-card >>> .el-card__header {
  padding: 15px 20px;
  border-bottom: 1px solid #f0f0f0;
}

/* 表格样式优化 */
.price-table >>> .el-table__header-wrapper th {
  background-color: #fafafa;
  color: #666;
  font-weight: 500;
}

.price-table >>> .el-table__body tr:hover > td {
  background-color: #f9f9f9; /* 行 hover 效果 */
}

/* 加载动画优化 */
.is-loading {
  animation: spin 1.5s linear infinite;
}
@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
</style>