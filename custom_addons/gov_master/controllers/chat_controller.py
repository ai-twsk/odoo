from odoo import http
from odoo.http import request
import openai  # 需 pip install openai
from openai import OpenAI

openai.api_key = 'YOUR_OPENAI_API_KEY'  # 可以放到 Odoo System Parameters


client = OpenAI(
    api_key="cb7a7cf460c142e7b9f1c207f26c1279.jn7dvHE0PXbjA9Ot",
    base_url="https://open.bigmodel.cn/api/paas/v4/"
)

class GovChatController(http.Controller):
    

    @http.route('/gov_master/chat', type='jsonrpc', auth='user')
    def chat(self, message, session_id=None):
        """接收用户消息，调用 ChatGPT 返回内容"""
        session = request.env['gov.chat.session'].sudo()
        message_model = request.env['gov.chat.message'].sudo()

        if session_id:
            session_rec = session.browse(session_id)
        else:
            session_rec = session.create({'name': 'Chat Session'})

        # 保存用户消息
        message_model.create({
            'session_id': session_rec.id,
            'content': message,
            'is_bot': False
        })

        # 调用 OpenAI ChatGPT
        try:
            # response = openai.ChatCompletion.create(
            #     model="gpt-3.5-turbo",
            #     messages=[{"role": "user", "content": message}],
            #     max_tokens=500
            # )
            # bot_reply = response['choices'][0]['message']['content']
            
            completion = client.chat.completions.create(
                model="glm-4.5-flash",
                messages=[
                    {"role": "system", "content": "你是一个聪明且富有创造力的小说作家"},
                    {"role": "user", "content": "请你作为童话故事大王，写一篇短篇童话故事"}
                ],
                stream=False,
                top_p=0.7,
                temperature=0.9
            )
            
            bot_reply = completion.choices[0].message.content
            
        except Exception as e:
            bot_reply = f"Error: {str(e)}"

        # 保存机器人回复
        message_model.create({
            'session_id': session_rec.id,
            'content': bot_reply,
            'is_bot': True
        })

        return {
            'session_id': session_rec.id,
            'reply': bot_reply
        }
