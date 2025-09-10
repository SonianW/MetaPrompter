#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
测试提示词优化功能的脚本
用于验证优化结果是否合理
"""

import requests
import json
import time

# 后端 API 地址
BASE_URL = "http://localhost:8000/api"


def print_separator(title):
    """打印分隔线和标题"""
    print("=" * 80)
    print(title.center(80))
    print("=" * 80)


def create_test_prompt():
    """创建一个测试提示词"""
    url = f"{BASE_URL}/prompts/"
    data = {
        "title": "测试优化的提示词",
        "content": "写一篇关于人工智能的文章",
        "description": "这是一个用于测试优化功能的简单提示词"
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        prompt = response.json()
        print(f"创建测试提示词成功，ID: {prompt['id']}")
        return prompt['id']
    else:
        print(f"创建测试提示词失败: {response.status_code}")
        print(response.text)
        return None


def optimize_test_prompt(prompt_id):
    """优化测试提示词"""
    url = f"{BASE_URL}/prompts/{prompt_id}/optimize/"
    # 可以尝试指定或不指定模型
    data = {"model": "deepseek/deepseek-chat-v3.1:free"}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        print("优化结果:")
        print(f"原始提示词: {result['original_content']}")
        print(f"优化后提示词: {result['optimized_content']}")
        return result
    else:
        print(f"优化提示词失败: {response.status_code}")
        print(response.text)
        return None


def update_prompt_optimization_template():
    """测试更新优化模板后的效果"""
    # 这里我们可以通过修改后端代码来更新优化模板
    # 但作为演示，我们先使用当前的模板进行测试
    pass


def evaluate_prompt(prompt_id):
    """评估优化后的提示词"""
    url = f"{BASE_URL}/prompts/{prompt_id}/evaluate/"
    data = {"model": "deepseek/deepseek-chat-v3.1:free"}
    response = requests.post(url, json=data)
    if response.status_code == 200:
        result = response.json()
        print("评估结果:")
        print(result['evaluation_result'])
        return result
    else:
        print(f"评估提示词失败: {response.status_code}")
        print(response.text)
        return None


def delete_test_prompt(prompt_id):
    """删除测试提示词"""
    url = f"{BASE_URL}/prompts/{prompt_id}/"
    response = requests.delete(url)
    if response.status_code == 204:
        print(f"已删除测试提示词 (ID: {prompt_id})")
    else:
        print(f"删除测试提示词失败: {response.status_code}")


def main():
    """主函数"""
    try:
        # 创建测试提示词
        print_separator("创建测试提示词")
        prompt_id = create_test_prompt()
        if not prompt_id:
            return
        
        # 等待1秒
        time.sleep(1)
        
        # 优化测试提示词
        print_separator("优化测试提示词")
        optimize_result = optimize_test_prompt(prompt_id)
        if not optimize_result:
            return
        
        # 等待1秒
        time.sleep(1)
        
        # 评估优化后的提示词
        print_separator("评估优化后的提示词")
        evaluate_result = evaluate_prompt(prompt_id)
        
        # 等待1秒
        time.sleep(1)
        
        # 删除测试提示词
        print_separator("清理测试数据")
        delete_test_prompt(prompt_id)
        
        print_separator("测试完成")
        
        # 根据测试结果提出改进建议
        if optimize_result:
            # 检查优化是否有实质性改进
            original_len = len(optimize_result['original_content'])
            optimized_len = len(optimize_result['optimized_content'])
            
            print("\n优化分析:")
            print(f"原始长度: {original_len} 字符")
            print(f"优化后长度: {optimized_len} 字符")
            print(f"长度变化: {optimized_len - original_len} 字符")
            
            if original_len == optimized_len and optimize_result['original_content'] == optimize_result['optimized_content']:
                print("警告: 优化结果与原始提示词完全相同")
            elif optimized_len < original_len * 1.5:
                print("可能的问题: 优化结果可能不够详细")
    except Exception as e:
        print(f"测试过程中发生错误: {str(e)}")


if __name__ == "__main__":
    main()