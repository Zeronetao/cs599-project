#!/usr/bin/env python
"""
简单的Django测试脚本
"""
import os
import sys
import django

# 添加项目路径到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 设置Django环境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AgentStock.settings')
django.setup()

from django.test import Client
from django.http import HttpRequest

def test_simple_endpoint():
    """测试simple_test端点"""
    try:
        # 使用Django测试客户端
        client = Client()
        response = client.get('/api/simple_test')
        
        print(f"Status Code: {response.status_code}")
        print(f"Content: {response.content.decode()}")
        print(f"Headers: {dict(response.items())}")
        
        return response.status_code == 200
    except Exception as e:
        print(f"Error: {e}")
        return False

if __name__ == "__main__":
    success = test_simple_endpoint()
    print(f"Test {'PASSED' if success else 'FAILED'}")