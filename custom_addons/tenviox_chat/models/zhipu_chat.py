from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import os

_logger = logging.getLogger(__name__)

class ZhipuConfiguration(models.TransientModel):
    _name = 'zhipu.configuration'
    _description = 'TenvioX API Configuration'

    # 将 API Key 存储在系统参数中，并使用 Char 字段配合 store=False 进行输入
    zhipu_api_key = fields.Char(
        string="TenvioX API Key", 
        help="Paste your TenvioX API Key here.",
        store=False
    )
    
    # 辅助字段，用于显示当前的配置状态
    current_key_display = fields.Char(
        string="Current API Key",
        compute='_compute_current_key',
        readonly=True
    )

    def _compute_current_key(self):
        ICPSudo = self.env['ir.config_parameter'].sudo()
        key = ICPSudo.get_param('gemini.api.key')
        if not key and os.getenv('GEMINI_API_KEY'):
             self.current_key_display = 'Configured (via Env Var)'
        elif not key and not os.getenv('GEMINI_API_KEY'):
             self.current_key_display = 'Configured (Hardcoded)'
        else:
             self.current_key_display = 'Configured (Encrypted)' if key else 'Not Configured'


    def save_configuration(self):
        """ 将配置保存到系统参数中，实际应用中建议使用 ir.config_parameter 存储敏感信息 """
        if not self.gemini_api_key:
            raise UserError(_("Please provide a valid Gemini API Key."))
            
        self.env['ir.config_parameter'].sudo().set_param(
            'gemini.api.key', 
            self.gemini_api_key
        )
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': _('Success'),
                'message': _('Gemini API Key saved successfully!'),
                'sticky': False,
            }
        }

class ZhipuChatHistory(models.Model):
    _name = 'zhipu.chat.history'
    _description = 'TenvioX Chat History'
    _order = 'create_date desc'

    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, required=True)
    prompt = fields.Text(string="User Prompt", required=True)
    response = fields.Text(string="TenvioX Response")
    model_name = fields.Char(string="Model Used", default='glm-4.5-flash')
    request_time = fields.Float(string="Response Time (s)")
    is_successful = fields.Boolean(string="Successful Request", default=True)

    @api.model
    def action_zhipu_chat(self, prompt, model_name='glm-4.5-flash'):
        """ 处理前端发送的消息，调用 TenvioX API，并记录历史 """
        try:
            from openai import OpenAI
        except ImportError:
            return {'error': "The 'openai' library is not installed on the server. Please install it with `pip install openai`."}
        
        import time
        
        start_time = time.time()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        api_key = ICPSudo.get_param('zhipu.api.key')
        
        # Fallback to environment variable (preserving compatibility with previous setup)
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY') # Keeping legacy env var check just in case, or remove if strictly zhipu
            
        # Fallback to provided Key
        if not api_key:
            api_key = "cb7a7cf460c142e7b9f1c207f26c1279.jn7dvHE0PXbjA9Ot"

        if not api_key:
            return {'error': "API Key is not configured."}

        is_successful = False
        gemini_response = ""

        # 1. 调用 API
        try:
            client = OpenAI(
                api_key=api_key,
                base_url="https://open.bigmodel.cn/api/paas/v4/"
            )

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
            gemini_response = f"An unexpected error occurred: {str(e)}"
            is_successful = False
            
        end_time = time.time()
        
        # 2. 记录对话历史
        self.sudo().create({
            'user_id': self.env.user.id,
            'prompt': prompt,
            'response': gemini_response,
            'model_name': model_name,
            'request_time': end_time - start_time,
            'is_successful': is_successful,
        })
        
        # 3. 返回结果给前端
        return {
            'response': gemini_response,
            'successful': is_successful
        }