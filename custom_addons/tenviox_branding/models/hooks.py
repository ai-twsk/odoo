# tenviox_brand_theme/hooks.py
from odoo import api, SUPERUSER_ID
import base64
import os

def post_init_hook(env):
    """
    模块安装后执行：
    1. 修改主公司名称和Logo
    2. 修改系统参数
    """
    # 获取图片路径
    module_path = os.path.dirname(__file__)
    img_path = os.path.join(module_path, 'static', 'src', 'img', 'logo.png')
    
    logo_content = False
    if os.path.exists(img_path):
        with open(img_path, 'rb') as f:
            logo_content = base64.b64encode(f.read())

    # 使用超级管理员权限
    env = api.Environment(env.cr, SUPERUSER_ID, {})
    
    # 1. 修改主公司信息 (ID通常为1)
    main_company = env.ref('base.main_company', raise_if_not_found=False)
    if main_company:
        vals = {
            'name': '北京天纬数科 (TenvioX)',
            'email': 'it-support@data-os.cn',
            'website': 'https://www.data-os.cn',
        }
        if logo_content:
            vals['logo'] = logo_content
        main_company.write(vals)

    # 2. 修改系统参数 (web.base.url 等) - 可选
    # param_obj = env['ir.config_parameter']
    # param_obj.set_param('web.base.title', 'TenvioX System') # 部分版本支持