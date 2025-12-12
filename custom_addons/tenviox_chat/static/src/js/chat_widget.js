/** @odoo-module **/

import { Component, useState, useRef, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class GeminiChatWidget extends Component {
    setup() {
        this.orm = useService("orm");
        this.state = useState({
            history: [],
            currentInput: "",
            isSending: false,
        });
        this.chatBodyRef = useRef("chatBody");

        onWillStart(() => {
             this._addMessage('Zhipu AI', "你好！我是由 TenvioX AI 驱动的智能助手，很高兴为你服务。今天需要我帮你做些什么？", 'gemini');
        });
    }

    _addMessage(sender, text, type) {
        this.state.history.push({
            sender,
            text,
            type,
            timestamp: new Date().toLocaleTimeString(),
        });
        // Scroll to bottom next tick
        Promise.resolve().then(() => this._scrollToBottom());
    }

    _scrollToBottom() {
        if (this.chatBodyRef.el) {
            this.chatBodyRef.el.scrollTop = this.chatBodyRef.el.scrollHeight;
        }
    }

    async _onSendMessage() {
        const prompt = this.state.currentInput.trim();
        if (!prompt) return;

        this._addMessage('User', prompt, 'user');
        this.state.currentInput = "";
        this.state.isSending = true;

        try {
            const result = await this.orm.call("zhipu.chat.history", "action_zhipu_chat", [], { 
                prompt: prompt 
            });
            
            if (result.error) {
                this._addMessage('System Error', result.error, 'error');
            } else {
                this._addMessage('Zhipu AI', result.response, 'gemini');
            }
        } catch (error) {
             this._addMessage('System Error', 'Network or server communication failed.', 'error');
             console.error("Gemini Chat Error:", error);
        } finally {
            this.state.isSending = false;
        }
    }

    _onInputKeydown(ev) {
        if (ev.keyCode === 13 && !ev.shiftKey) {
            ev.preventDefault();
            this._onSendMessage();
        }
    }
}

GeminiChatWidget.template = "odoo_gemini_chat.GeminiChatWidget";
registry.category("actions").add("gemini.chat.widget", GeminiChatWidget);