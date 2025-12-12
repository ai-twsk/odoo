# odoo_gemini_chat/__manifest__.py
{
    'name': "TenvioX AI Chatbot for Odoo",
    'summary': "Integrate TenvioX API Key for a powerful conversational AI assistant within Odoo.",
    'description': """
        此模块将 Google Gemini 大语言模型集成到 Odoo 中，
        提供一个强大的对话式 AI 助手，同时记录聊天历史和配置 API Key。
    """,
    'author': "TenvioX Chatbot",
    'website': "https://data-os.cn",
    'category': 'Productivity',
    'version': '1.0',
    'depends': ['base', 'web'], 
    
    # 引用数据文件和安全文件
    'data': [
        # 1. 安全配置：允许用户访问新模型
        'security/ir.model.access.csv',
        # 2. 视图和菜单定义
        'views/gemini_chat_views.xml',
    ],
    
    # 引用前端资产 (JS, XML, CSS)
    'assets': {
        'web.assets_backend': [
            # JavaScript 逻辑
            'tenviox_chat/static/src/js/chat_widget.js',
            # QWeb 模板
            'tenviox_chat/static/src/xml/chat_template.xml',
            # CSS 样式 (新增的文件)
            'tenviox_chat/static/src/css/chat.css', 
        ],
    },
    'license': 'LGPL-3',
}