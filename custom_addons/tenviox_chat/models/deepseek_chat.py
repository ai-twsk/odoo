from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging
import os

_logger = logging.getLogger(__name__)

class DeepseekConfiguration(models.TransientModel):
    _name = 'deepseek.configuration'
    _description = 'Deepseek API Configuration'

    # 将 API Key 存储在系统参数中，并使用 Char 字段配合 store=False 进行输入
    deepseek_api_key = fields.Char(
        string="Deepseek API Key", 
        help="Paste your Deepseek API Key here.",
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

class DeepseekChatHistory(models.Model):
    _name = 'deepseek.chat.history'
    _description = 'Deepseek Chat History'
    _order = 'create_date desc'

    user_id = fields.Many2one('res.users', string="User", default=lambda self: self.env.user, required=True)
    prompt = fields.Text(string="User Prompt", required=True)
    response = fields.Text(string="Gemini Response")
    model_name = fields.Char(string="Model Used", default='gemini-2.5-flash')
    request_time = fields.Float(string="Response Time (s)")
    is_successful = fields.Boolean(string="Successful Request", default=True)

    @api.model
    def action_gemini_chat(self, prompt, model_name='deepseek-chat'):
        """ 处理前端发送的消息，调用 DeepSeek API，并记录历史 """
        import requests
        import json
        import time
        
        start_time = time.time()
        ICPSudo = self.env['ir.config_parameter'].sudo()
        api_key = ICPSudo.get_param('gemini.api.key')
        
        # Fallback to environment variable (preserving compatibility with previous setup)
        if not api_key:
            api_key = os.getenv('GEMINI_API_KEY')
            
        # Fallback to provided DeepSeek Key
        if not api_key:
            api_key = "sk-50125a903b3948cb96edbbedd2b8da26"

        if not api_key:
            return {'error': "API Key is not configured."}

        # 1. 调用 DeepSeek API
        try:
            url = "https://api.deepseek.com/chat/completions"
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}"
            }
            data = {
                "model": "deepseek-chat",
                "messages": [
                    {"role": "system", "content": "You are an helpful and friendly AI assistant integrated into an Odoo ERP system. Be concise and accurate."},
                    {"role": "user", "content": prompt}
                ],
                "stream": False
            }
            
            response = requests.post(url, headers=headers, json=data, timeout=60)
            
            if response.status_code == 200:
                result = response.json()
                gemini_response = result['choices'][0]['message']['content']
                is_successful = True
            else:
                gemini_response = f"DeepSeek API Error: {response.status_code} - {response.text}"
                is_successful = False
                
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