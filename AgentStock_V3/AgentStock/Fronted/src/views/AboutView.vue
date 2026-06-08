<template>
  <el-container direction="vertical">
    <el-header>
      <h2>📖 系统说明</h2>
    </el-header>
    <el-main>
      <el-card class="system-intro">
        <template #header>
          <div class="card-header">
            <span>🚀 AgentStock - AI 股票预测模拟系统</span>
          </div>
        </template>
        <div class="intro-content">
          <p class="system-description">
            AgentStock 是一个基于人工智能的股票交易模拟系统，通过多智能体（Multi-Agent）技术模拟真实的股票市场交易环境。
            系统采用先进的机器学习算法和自然语言处理技术，让AI智能体能够分析市场数据、制定交易策略并执行买卖决策。
          </p>
        </div>
      </el-card>

      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="12">
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <span>🎯 核心功能</span>
              </div>
            </template>
            <ul class="feature-list">
              <li><strong>智能参数配置：</strong>支持自定义模拟天数、Agent数量和股票数量</li>
              <li><strong>多Agent模拟：</strong>每个AI智能体独立分析和决策，模拟真实交易者行为</li>
              <li><strong>实时数据分析：</strong>基于历史股价数据进行技术分析和趋势预测</li>
              <li><strong>策略对比：</strong>可视化展示不同Agent的交易策略和收益表现</li>
              <li><strong>风险管理：</strong>内置风险控制机制，避免过度交易和资金损失</li>
            </ul>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card class="feature-card">
            <template #header>
              <div class="card-header">
                <span>🔧 技术特色</span>
              </div>
            </template>
            <ul class="feature-list">
              <li><strong>深度学习模型：</strong>使用LSTM、Transformer等先进模型预测股价走势</li>
              <li><strong>自然语言处理：</strong>分析新闻情感和市场舆论对股价的影响</li>
              <li><strong>强化学习：</strong>Agent通过不断学习优化交易策略</li>
              <li><strong>实时可视化：</strong>动态图表展示交易过程和收益变化</li>
              <li><strong>数据持久化：</strong>完整记录每次模拟的交易历史和结果</li>
            </ul>
          </el-card>
        </el-col>
      </el-row>

      <el-card style="margin-top: 20px;" class="usage-guide">
        <template #header>
          <div class="card-header">
            <span>📋 使用指南</span>
          </div>
        </template>
        <el-steps :active="4" finish-status="success" align-center>
          <el-step title="参数设置" description="在首页配置模拟参数：天数、Agent数量、股票数量"></el-step>
          <el-step title="开始模拟" description="点击开始模拟按钮，系统将初始化AI智能体和市场环境"></el-step>
          <el-step title="查看详情" description="在模拟详情页面观察每个Agent的交易决策和收益变化"></el-step>
          <el-step title="策略对比" description="在对比页面分析不同Agent的策略效果和最终收益排名"></el-step>
        </el-steps>
      </el-card>

      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="8">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>💡 系统优势</span>
              </div>
            </template>
            <ul class="advantage-list">
              <li>无风险模拟环境</li>
              <li>多种交易策略测试</li>
              <li>实时性能监控</li>
              <li>历史数据回测</li>
              <li>智能风险控制</li>
            </ul>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>🎓 适用场景</span>
              </div>
            </template>
            <ul class="scenario-list">
              <li>量化交易策略研究</li>
              <li>金融市场教学演示</li>
              <li>投资策略回测验证</li>
              <li>AI算法性能评估</li>
              <li>风险管理培训</li>
            </ul>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card class="info-card">
            <template #header>
              <div class="card-header">
                <span>⚠️ 注意事项</span>
              </div>
            </template>
            <ul class="notice-list">
              <li>仅供学习和研究使用</li>
              <li>不构成投资建议</li>
              <li>模拟结果不代表真实收益</li>
              <li>请合理设置参数范围</li>
              <li>建议定期保存模拟结果</li>
            </ul>
          </el-card>
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script setup lang="ts">
import { Warning } from '@element-plus/icons-vue'
</script>

<style scoped>
.el-header {
  margin-bottom: 20px;
}

.system-intro .intro-content {
  padding: 10px 0;
}

.system-description {
  font-size: 16px;
  line-height: 1.8;
  color: #606266;
  text-align: justify;
  margin: 0;
}

.card-header {
  font-weight: 600;
  font-size: 16px;
  color: #303133;
}

.feature-card, .info-card {
  height: 100%;
}

.feature-list, .advantage-list, .scenario-list, .notice-list {
  list-style: none;
  padding: 0;
  margin: 0;
}

.feature-list li, .advantage-list li, .scenario-list li, .notice-list li {
  padding: 8px 0;
  border-bottom: 1px solid #f0f0f0;
  color: #606266;
  line-height: 1.6;
}

.feature-list li:last-child, .advantage-list li:last-child, 
.scenario-list li:last-child, .notice-list li:last-child {
  border-bottom: none;
}

.usage-guide {
  background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
}

.contact-content {
  padding: 10px 0;
}

.contact-content p {
  margin: 10px 0;
  color: #606266;
  line-height: 1.6;
}

.disclaimer {
  background-color: #fff3cd;
  border: 1px solid #ffeaa7;
  border-radius: 4px;
  padding: 12px;
  margin-top: 20px;
  color: #856404;
  display: flex;
  align-items: flex-start;
  gap: 8px;
}

.disclaimer .el-icon {
  margin-top: 2px;
  color: #f39c12;
}

.el-steps {
  margin: 20px 0;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .el-row {
    margin: 10px 0 !important;
  }
  
  .system-description {
    font-size: 14px;
  }
  
  .feature-list li, .advantage-list li, .scenario-list li, .notice-list li {
    font-size: 14px;
  }
}
</style>