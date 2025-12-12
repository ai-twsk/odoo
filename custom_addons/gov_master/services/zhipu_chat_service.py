# -*- coding: utf-8 -*-

import re
import json
import httpx
from openai import OpenAI 

from loguru import logger



class ZhipuAIChatService:
    
    _model = "glm-4.5-flash" #"glm-4-flash-250414"
    
    def __init__(self, api_key: str = "cb7a7cf460c142e7b9f1c207f26c1279.jn7dvHE0PXbjA9Ot", 
                 model: str = _model):
        self.base_url = "https://open.bigmodel.cn/api/paas/v4/"
        self.api_key = api_key
        self.model = model
        self.client = httpx.AsyncClient(base_url=self.base_url, headers={
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    async def chat(self, messages, top_p=0.7, temperature=0.9):
        url = "chat/completions"
        payload = {
            "model": self.model,
            "messages": messages,
            "top_p": top_p,
            "temperature": temperature
        }
        try:
            response = await self.client.post(url, json=payload, timeout=30)
            response.raise_for_status()
            result = response.json()

            # return completion["choices"][0]["message"]["content"]
            
            # return result["choices"][0]["message"]["content"]
            
            return self.extract_json_from_response(response_text=result["choices"][0]["message"]["content"])
    
        
        except httpx.HTTPStatusError as e:
            logger.info("HTTP error: {} - {}", e.response.status_code, e.response.text)
            return None
        except Exception as e:
            logger.info("Unexpected error: {}", str(e))
            return None

    async def close(self):
        await self.client.aclose()


    def extract_json_from_response(self, response_text: str) -> dict:
        """
        处理 REST API 返回的文本内容，提取 JSON 格式的数据。

        :param response_text: API 返回的原始字符串
        :return: 解析后的 JSON（字典类型）
        :raises ValueError: 当无法提取或解析 JSON 时抛出异常
        """
        # 1. 查找 markdown 中的 ```json ... ``` 区块
        # match = re.search(r'```json\s*(.*?)\s*```', response_text, re.DOTALL)
        match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL | re.IGNORECASE)
        if match:
            json_str = match.group(1)
        else:
            json_str = response_text.strip()

        # 2. 尝试解析 JSON 内容
        try:
            result = json.loads(json_str)
        except json.JSONDecodeError as e:
            raise ValueError("无法解析为有效的 JSON") from e

        return result


