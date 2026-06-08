<template>
  <el-container style="height: 100vh; overflow: hidden">
    <el-aside width="220px" style="background-color: #001529; color: white; height: 100vh; overflow: hidden">
      <div style="height: 60px; display: flex; align-items: center; justify-content: center; font-weight: bold; font-size: 18px; color: #fff; border-bottom: 1px solid #333;">
        📈 AgentStock
      </div>
      <el-menu
        :default-active="$route.path"
        class="el-menu-vertical-demo"
        @select="onNavigate"
        background-color="#001529"
        text-color="#fff"
        active-text-color="#409EFF"
      >
        <el-menu-item index="/">
          <i class="el-icon-setting"></i>
          <span>参数设置</span>
        </el-menu-item>
        <el-menu-item index="/simulation">
          <i class="el-icon-data-analysis"></i>
          <span>模拟详情</span>
        </el-menu-item>
        <el-menu-item index="/compare">
          <i class="el-icon-pie-chart"></i>
          <span>Agent 对比</span>
        </el-menu-item>
        <el-menu-item index="/stock">
          <i class="el-icon-pie-chart"></i>
          <span>股票 价格</span>
        </el-menu-item>
        <el-menu-item index="/about">
          <i class="el-icon-info"></i>
          <span>系统说明</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container style="overflow: hidden">
      <el-header style="background: #f0f2f5; text-align: center; box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);">
        <h2 style="margin: 0; font-weight: 500">📊 AI 股票预测系统</h2>
      </el-header>
      <el-main style="background: #fff; padding: 24px; overflow: auto">
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<script setup lang="ts">
import { useRouter } from 'vue-router'

const router = useRouter()

function onNavigate(path: string) {
  if (router.currentRoute.value.path !== path) {
    router.push(path)
  }
}
</script>

<style scoped>
.el-menu-vertical-demo {
  border-right: none;
  height: 100%;
  background-color: #001529;
}
.el-header {
  line-height: 60px;
}
</style>
