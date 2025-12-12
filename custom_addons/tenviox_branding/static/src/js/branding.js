odoo.define('tenviox_enterprise_customization.branding', function (require) {
    "use strict";

    var core = require('web.core');
    var session = require('web.session');
    var WebClient = require('web.WebClient');

    // 修改页面标题
    WebClient.include({
        init: function() {
            this._super.apply(this, arguments);
            this.set('title_part', {"zopenerp": "TenvioX - 北京天纬数科"});
        },
        
        start: function() {
            var self = this;
            return this._super().then(function() {
                // 页面加载完成后执行品牌替换
                self._replaceBranding();
                
                // 监听DOM变化，持续替换可能出现的新元素
                self._watchForChanges();
            });
        },
        
        _replaceBranding: function() {
            // 替换页面中的品牌文字
            this._replaceTextContent();
            
            // 更新页面标题
            document.title = document.title.replace(/Odoo/g, 'TenvioX');
            
            // 添加自定义品牌元素
            this._addTenvioxBranding();
        },
        
        _replaceTextContent: function() {
            // 查找并替换页面中的品牌文字
            var elements = document.querySelectorAll('*');
            for (var i = 0; i < elements.length; i++) {
                var element = elements[i];
                
                // 替换直接文本节点
                if (element.nodeType === Node.ELEMENT_NODE) {
                    var walker = document.createTreeWalker(
                        element,
                        NodeFilter.SHOW_TEXT,
                        null,
                        false
                    );
                    
                    var textNodes = [];
                    var node;
                    while (node = walker.nextNode()) {
                        textNodes.push(node);
                    }
                    
                    textNodes.forEach(function(textNode) {
                        var newText = textNode.nodeValue
                            .replace(/Odoo/g, 'TenvioX')
                            .replace(/Open Source ERP/g, '企业数字化管理平台')
                            .replace(/open source ERP/g, '企业数字化管理平台')
                            .replace(/Visit our website for more information/g, '如需更多信息，请访问我们的网站')
                            .replace(/Contact us for support/g, '技术支持请联系：it-support@data-os.cn');
                        
                        if (newText !== textNode.nodeValue) {
                            textNode.nodeValue = newText;
                        }
                    });
                }
            }
        },
        
        _addTenvioxBranding: function() {
            // 添加自定义品牌标识
            var brandingDiv = document.getElementById('branding-replacement');
            if (!brandingDiv) {
                brandingDiv = document.createElement('div');
                brandingDiv.id = 'branding-replacement';
                brandingDiv.innerHTML = 'TenvioX v19.0.1 - 北京天纬数科';
                document.body.appendChild(brandingDiv);
            }
        },
        
        _watchForChanges: function() {
            var self = this;
            var observer = new MutationObserver(function(mutations) {
                mutations.forEach(function(mutation) {
                    if (mutation.type === 'childList') {
                        // 新增节点时重新执行品牌替换
                        setTimeout(function() {
                            self._replaceTextContent();
                        }, 100);
                    }
                });
            });
            
            observer.observe(document.body, {
                childList: true,
                subtree: true
            });
        }
    });

    // 修改登录页面
    $(document).ready(function() {
        // 替换登录页面的品牌信息
        setTimeout(function() {
            $('body').find('*').contents().filter(function() {
                return this.nodeType === 3 && /Odoo/.test(this.textContent);
            }).each(function() {
                this.textContent = this.textContent.replace(/Odoo/g, 'TenvioX');
            });
            
            // 更新页脚
            var footer = $('footer');
            if (footer.length > 0) {
                footer.html('<div style="text-align: center; padding: 10px; color: #6c757d;">' +
                           'Powered by TenvioX - 北京天纬数科 | ' +
                           '技术支持: <a href="mailto:it-support@data-os.cn">it-support@data-os.cn</a></div>');
            } else {
                var newFooter = $('<footer style="text-align: center; padding: 20px; color: #6c757d; background: #f8f9fa; margin-top: 20px;">' +
                                 'Powered by TenvioX - 北京天纬数科 | ' +
                                 '技术支持: <a href="mailto:it-support@data-os.cn" style="color: #1e3c72;">it-support@data-os.cn</a></footer>');
                $('body').append(newFooter);
            }
        }, 500);
    });

    return WebClient;
});