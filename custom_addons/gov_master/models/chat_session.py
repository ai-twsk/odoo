from odoo import models, fields, api
from datetime import datetime
from odoo.http import request
from openai import OpenAI

class GovChatSession(models.Model):
    _name = 'gov.chat.session'
    _description = 'Chat Session'

    name = fields.Char(default='New Session')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    message_ids = fields.One2many('gov.chat.message', 'session_id', string='Messages')
    
    @api.model
    def action_send_message(self):
        """调用控制器接口实现一次对话"""        
        client = OpenAI(
            api_key="cb7a7cf460c142e7b9f1c207f26c1279.jn7dvHE0PXbjA9Ot",
            base_url="https://open.bigmodel.cn/api/paas/v4/"
        )
                
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

        reply = completion.choices[0].message.content
        self.env['gov.chat.message'].create({
            'session_id': self.id,
            'content': reply,
            'is_bot': True
        })
        return True


class GovChatMessage(models.Model):
    _name = 'gov.chat.message'
    _description = 'Chat Message'

    session_id = fields.Many2one('gov.chat.session', ondelete='cascade')
    user_id = fields.Many2one('res.users', default=lambda self: self.env.user)
    content = fields.Text()
    is_bot = fields.Boolean(default=False)
    create_date = fields.Datetime(default=fields.Datetime.now)
