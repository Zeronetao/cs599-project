import axios from 'axios'

const http = axios.create({
  //baseURL: 'http://localhost:8000', // 你的后端地址
  baseURL: 'http://localhost:8000', // 你的后端地址
  timeout: 300000 // 5分钟超时，适应长时间仿真
})

export default http