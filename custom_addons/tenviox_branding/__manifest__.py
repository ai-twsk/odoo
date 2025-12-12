# tenviox_branding/__manifest__.py
{
    'name': "TenvioX Nexus平台",
    'summary': """
        TenvioX(北京天纬数科) 致力于构建中国领先的智能数据基础设施，推动企业的“数据智能化”全面升级。企业数字化正在向“智能时代”演进，而 TenvioX 的使命是：让数据会说话，让人人都能成为数据驱动者。
    """,
    'description': """
        - TenvioX 致力于构建中国领先的智能数据基础设施，推动企业的“数据智能化”全面升级。
        - 企业数字化正在向“智能时代”演进，而 TenvioX 的使命是：让数据会说话，让人人都能成为数据驱动者。
    """,
    'author': 'TenvioX - 北京天纬数科',
    'website': 'https://www.data-os.cn',
    'category': 'Productivity',
    'version': '19.0.1.0.0',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'views/web_layout.xml',
    ],
    'assets': {
        'web._assets_primary_variables': [
            "tenviox_branding/static/src/scss/primary_variables.scss",
        ],
        'web.assets_backend': [
            'tenviox_branding/static/src/js/tenviox_title.js',

            'tenviox_branding/static/src/scss/variables.scss',
            'tenviox_branding/static/src/scss/tenviox_theme.scss',
            
            'tenviox_branding/static/src/fonts/AlibabaPuHuiTi-3-35-Thin.ttf',
            'tenviox_branding/static/src/fonts/AlibabaPuHuiTi-3-45-Light.ttf',
            'tenviox_branding/static/src/fonts/AlibabaPuHuiTi-3-55-Regular.ttf',
            'tenviox_branding/static/src/fonts/AlibabaPuHuiTi-3-65-Medium.ttf'
        ],
    },
    # 'post_init_hook': 'post_init_hook',
    'qweb': [],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
    'license': 'LGPL-3',
    'images': ['static/description/icon.png'],
}