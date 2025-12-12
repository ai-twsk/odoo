# odoo_gemini_chat/controllers/main.py
from odoo import http
from odoo.http import request
import json
import time
import os

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class GeminiChatController(http.Controller):

    @http.route('/gemini/chat/send', type='jsonrpc', auth='user', methods=['POST'], csrf=True)
    def send_message(self, prompt, model_name='glm-4.5-flash'):
        """ 处理前端发送的消息，调用 TenvioX API，并记录历史 """
        
        if not OpenAI:
            return {'error': "The 'openai' library is not installed on the server."}
        
        start_time = time.time()
        ICPSudo = request.env['ir.config_parameter'].sudo()
        api_key = ICPSudo.get_param('zhipu.api.key')
        
        # Fallback to environment variable
        if not api_key:
             api_key = os.getenv('GEMINI_API_KEY')

        # Fallback to provided Key
        if not api_key:
            api_key = "cb7a7cf460c142e7b9f1c207f26c1279.jn7dvHE0PXbjA9Ot"
        
        if not api_key:
            return {'error': "TenvioX API Key is not configured. Please contact the administrator."}

        # 1. 初始化 Client
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://open.bigmodel.cn/api/paas/v4/"
            )
        except Exception as e:
            return {'error': f"Failed to initialize client: {str(e)}"}
            
        gemini_response = ""
        is_successful = False
        
        try:
            # 2. 调用生成 API
            completion = client.chat.completions.create(
                model=model_name,
                messages=[
                    {"role": "system", "content": "You are an helpful and friendly AI assistant integrated into an Odoo ERP system. Be concise and accurate."},
                    {"role": "user", "content": prompt}
                ],
                stream=False,
                top_p=0.7,
                temperature=0.9
            )
            
            gemini_response = completion.choices[0].message.content
            is_successful = True
            
        except Exception as e:
            gemini_response = f"API Error: {str(e)}"
            
        end_time = time.time()
        
        # 3. 记录对话历史
        # Note: Using zhipu.chat.history model now
        try:
            request.env['zhipu.chat.history'].sudo().create({
                'user_id': request.env.user.id,
                'prompt': prompt,
                'response': gemini_response,
                'model_name': model_name,
                'request_time': end_time - start_time,
                'is_successful': is_successful,
            })
        except Exception as e:
            # Fallback for old model if new one doesn't exist yet (though it should)
             request.env['gemini.chat.history'].sudo().create({
                'user_id': request.env.user.id,
                'prompt': prompt,
                'response': gemini_response,
                'model_name': model_name,
                'request_time': end_time - start_time,
                'is_successful': is_successful,
            })
        
        # 4. 返回结果给前端
        return {
            'response': gemini_response,
            'successful': is_successful
        }