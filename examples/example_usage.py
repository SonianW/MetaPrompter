#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
MetaPrompter API 调用示例

这个脚本演示了如何使用 Python 的 requests 库调用 MetaPrompter 的所有主要 API 端点。
在运行之前，请确保：
1. Django 开发服务器正在运行（默认端口 8000）
2. 已安装必要的依赖：pip install requests

使用方法：
  python example_usage.py

或者添加执行权限后直接运行：
  chmod +x example_usage.py
  ./example_usage.py
"""

import requests
import json
import time
from typing import Dict, Any, Optional, List

class MetaPrompterAPI:
    """MetaPrompter API 客户端类，封装了所有 API 调用方法"""
    
    def __init__(self, base_url: str = "http://localhost:8000/api"):
        """初始化 API 客户端
        
        Args:
            base_url: API 基础 URL，默认为本地开发服务器地址
        """
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        
    def _handle_response(self, response: requests.Response) -> Dict[str, Any]:
        """处理 API 响应，统一错误处理逻辑
        
        Args:
            response: requests 库的响应对象
        
        Returns:
            解析后的 JSON 数据
        
        Raises:
            Exception: 当 API 返回错误状态码时
        """
        try:
            data = response.json()
        except json.JSONDecodeError:
            data = {"error": "Invalid JSON response", "content": response.text}
        
        if response.status_code >= 400:
            error_msg = data.get("error", data.get("detail", f"HTTP Error {response.status_code}"))
            raise Exception(f"API 请求失败 ({response.status_code}): {error_msg}")
        
        return data
    
    def generate_prompt(self, requirement: str, model: str = "gpt-4o-mini", 
                       title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """生成新的提示词
        
        Args:
            requirement: 提示词需求描述
            model: 使用的 LLM 模型，默认为 gpt-4o-mini
            title: 提示词标题（可选）
            description: 提示词描述（可选）
        
        Returns:
            生成的提示词信息
        """
        url = f"{self.base_url}/prompts/generate/"
        data = {
            "requirement": requirement,
            "model": model
        }
        
        # 添加可选参数
        if title: data["title"] = title
        if description: data["description"] = description
        
        response = self.session.post(url, data=json.dumps(data))
        result = self._handle_response(response)
        return result["prompt"]
    
    def evaluate_prompt(self, prompt_id: int, detailed: bool = True, model: str = "gpt-4o-mini") -> str:
        """评估提示词质量
        
        Args:
            prompt_id: 提示词 ID
            detailed: 是否返回详细评估结果，默认为 True
            model: 使用的 LLM 模型，默认为 gpt-4o-mini
        
        Returns:
            评估结果文本
        """
        url = f"{self.base_url}/prompts/{prompt_id}/evaluate/"
        data = {
            "detailed": detailed,
            "model": model
        }
        
        response = self.session.post(url, data=json.dumps(data))
        result = self._handle_response(response)
        return result["evaluation_result"]
    
    def optimize_prompt(self, prompt_id: int, model: str = "gpt-4o-mini") -> Dict[str, Any]:
        """优化提示词
        
        Args:
            prompt_id: 提示词 ID
            model: 使用的 LLM 模型，默认为 gpt-4o-mini
        
        Returns:
            优化后的提示词信息
        """
        url = f"{self.base_url}/prompts/{prompt_id}/optimize/"
        data = {"model": model}
        
        response = self.session.post(url, data=json.dumps(data))
        result = self._handle_response(response)
        # 为了兼容前端代码，将optimized_content重命名为content
        result['content'] = result.get('optimized_content', '')
        return result
    
    def get_prompts(self) -> List[Dict[str, Any]]:
        """获取所有提示词列表
        
        Returns:
            提示词列表
        """
        url = f"{self.base_url}/prompts/"
        response = self.session.get(url)
        return self._handle_response(response)
    
    def get_prompt(self, prompt_id: int) -> Dict[str, Any]:
        """获取单个提示词详情
        
        Args:
            prompt_id: 提示词 ID
        
        Returns:
            提示词详情
        """
        url = f"{self.base_url}/prompts/{prompt_id}/"
        response = self.session.get(url)
        return self._handle_response(response)
    
    def create_prompt(self, title: str, content: str, description: Optional[str] = None) -> Dict[str, Any]:
        """手动创建提示词
        
        Args:
            title: 提示词标题
            content: 提示词内容
            description: 提示词描述（可选）
        
        Returns:
            创建的提示词信息
        """
        url = f"{self.base_url}/prompts/"
        data = {
            "title": title,
            "content": content
        }
        
        if description: data["description"] = description
        
        response = self.session.post(url, data=json.dumps(data))
        return self._handle_response(response)
    
    def update_prompt(self, prompt_id: int, title: Optional[str] = None, 
                     content: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
        """更新提示词
        
        Args:
            prompt_id: 提示词 ID
            title: 新的提示词标题（可选）
            content: 新的提示词内容（可选）
            description: 新的提示词描述（可选）
        
        Returns:
            更新后的提示词信息
        """
        url = f"{self.base_url}/prompts/{prompt_id}/"
        data = {}
        
        # 只添加提供的参数
        if title is not None: data["title"] = title
        if content is not None: data["content"] = content
        if description is not None: data["description"] = description
        
        response = self.session.patch(url, data=json.dumps(data))
        return self._handle_response(response)
    
    def delete_prompt(self, prompt_id: int) -> bool:
        """删除提示词
        
        Args:
            prompt_id: 提示词 ID
        
        Returns:
            删除是否成功
        """
        url = f"{self.base_url}/prompts/{prompt_id}/"
        response = self.session.delete(url)
        
        # 检查删除是否成功（204 No Content 表示成功）
        if response.status_code == 204:
            return True
        
        # 处理其他情况
        self._handle_response(response)
        return True  # 如果没有抛出异常，默认成功
    
    def use_prompt(self, prompt_id: int) -> Dict[str, Any]:
        """使用提示词（记录使用历史）
        
        Args:
            prompt_id: 提示词 ID
        
        Returns:
            操作结果
        """
        url = f"{self.base_url}/prompts/{prompt_id}/use/"
        response = self.session.post(url)
        return self._handle_response(response)
    
    def get_histories(self) -> List[Dict[str, Any]]:
        """获取操作历史记录
        
        Returns:
            历史记录列表
        """
        url = f"{self.base_url}/histories/"
        response = self.session.get(url)
        return self._handle_response(response)
    
    def get_statistics(self) -> List[Dict[str, Any]]:
        """获取统计信息
        
        Returns:
            统计信息列表
        """
        url = f"{self.base_url}/statistics/"
        response = self.session.get(url)
        return self._handle_response(response)
    
    def get_public_prompts(self) -> List[Dict[str, Any]]:
        """获取公开提示词列表
        
        Returns:
            公开提示词列表
        """
        url = f"{self.base_url}/public-prompts/"
        response = self.session.get(url)
        return self._handle_response(response)


def print_separator(title: str):
    """打印分隔线和标题"""
    print("\n" + "=" * 80)
    print(f"{title.center(80)}")
    print("=" * 80)


def main():
    """主函数，演示所有 API 调用"""
    # 创建 API 客户端实例
    api = MetaPrompterAPI()
    created_prompt_id = None
    generated_prompt_id = None
    
    try:
        # 1. 查看当前所有提示词
        print_separator("1. 查看当前所有提示词")
        prompts = api.get_prompts()
        print(f"共找到 {len(prompts)} 个提示词")
        
        if prompts:
            for i, prompt in enumerate(prompts, 1):
                print(f"{i}. [{prompt['id']}] {prompt['title']}")
                print(f"   描述: {prompt['description']}")
                print(f"   内容预览: {prompt['content'][:50]}...")
        else:
            print("暂无提示词")
        
        # 2. 手动创建一个新的提示词
        print_separator("2. 手动创建一个新的提示词")
        new_prompt = api.create_prompt(
            title="测试提示词",
            description="这是一个测试用的提示词",
            content="你是一个助手，请简要回答用户的问题。保持回答简洁明了。"
        )
        created_prompt_id = new_prompt["id"]
        print(f"创建成功！提示词ID: {created_prompt_id}")
        print(f"标题: {new_prompt['title']}")
        print(f"内容: {new_prompt['content']}")
        
        # 3. 使用 AI 生成一个新的提示词
        print_separator("3. 使用 AI 生成一个新的提示词")
        generated_prompt = api.generate_prompt(
            requirement="请生成一个用于写邮件的提示词模板",
            model="gpt-4o-mini",
            title="邮件撰写提示词"
        )
        generated_prompt_id = generated_prompt["id"]
        print(f"生成成功！提示词ID: {generated_prompt_id}")
        print(f"标题: {generated_prompt['title']}")
        print(f"内容:\n{generated_prompt['content']}")
        
        # 4. 评估生成的提示词质量
        print_separator("4. 评估生成的提示词质量")
        evaluation = api.evaluate_prompt(generated_prompt_id, detailed=True)
        print(f"评估结果:\n{evaluation}")
        
        # 5. 优化生成的提示词
        print_separator("5. 优化生成的提示词")
        optimized_prompt = api.optimize_prompt(generated_prompt_id)
        print(f"优化成功！")
        print(f"优化后内容:\n{optimized_prompt['content']}")
        
        # 6. 使用提示词（记录使用历史）
        print_separator("6. 使用提示词")
        use_result = api.use_prompt(generated_prompt_id)
        print(f"使用成功: {use_result['status']}")
        
        # 7. 查看历史记录
        print_separator("7. 查看历史记录")
        histories = api.get_histories()
        print(f"共找到 {len(histories)} 条历史记录")
        
        # 只显示最近的 5 条记录
        recent_histories = histories[-5:]
        for i, history in enumerate(recent_histories, 1):
            prompt_id = history.get("prompt", "N/A")
            operation = history.get("operation_type", "N/A")
            created_at = history.get("created_at", "N/A")
            print(f"{i}. 操作: {operation}, 提示词ID: {prompt_id}, 时间: {created_at}")
        
        # 8. 查看统计信息
        print_separator("8. 查看统计信息")
        statistics = api.get_statistics()
        print(f"共找到 {len(statistics)} 条统计记录")
        
        if statistics:
            for stat in statistics:
                prompt_id = stat.get("prompt", "N/A")
                usage = stat.get("total_usage", 0)
                optimizations = stat.get("optimization_count", 0)
                print(f"提示词ID: {prompt_id}, 使用次数: {usage}, 优化次数: {optimizations}")
        
        # 9. 更新提示词
        print_separator("9. 更新提示词")
        updated_prompt = api.update_prompt(
            generated_prompt_id,
            description="这是一个由 AI 生成并优化的邮件撰写提示词"
        )
        print(f"更新成功！")
        print(f"更新后描述: {updated_prompt['description']}")
        
        # 10. 查看公开提示词
        print_separator("10. 查看公开提示词")
        public_prompts = api.get_public_prompts()
        print(f"共找到 {len(public_prompts)} 个公开提示词")
        
        if public_prompts:
            for i, prompt in enumerate(public_prompts, 1):
                print(f"{i}. [{prompt['id']}] {prompt['title']}")
        
        # 11. 删除测试创建的提示词
        print_separator("11. 清理测试数据")
        if created_prompt_id:
            api.delete_prompt(created_prompt_id)
            print(f"已删除手动创建的提示词 (ID: {created_prompt_id})")
            
        # 注意：为了演示，我们保留 AI 生成的提示词不删除
        print("已完成所有 API 调用演示！")
        
    except Exception as e:
        print(f"发生错误: {e}")
        
    finally:
        # 确保清理所有测试数据
        if created_prompt_id:
            try:
                api.delete_prompt(created_prompt_id)
            except:
                pass


if __name__ == "__main__":
    print("MetaPrompter API 调用示例开始执行...")
    print("请确保 Django 开发服务器正在 http://localhost:8000 运行")
    print("\n正在连接 API...")
    time.sleep(1)  # 给用户一点时间阅读提示
    main()
    print("\n示例执行完毕！")