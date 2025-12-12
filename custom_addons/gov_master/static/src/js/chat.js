/** @odoo-module **/

import { registry } from "@web/core/registry";
import { onMounted } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { Component } from "@odoo/owl";

export class GovChatInterface extends Component {
    setup() {
        this.orm = useService("orm");
        this.rpc = useService("rpc");
        onMounted(this.mountChat.bind(this));
    }

    mountChat() {
        const input = document.querySelector("#gov_chat_input");
        const button = document.querySelector("#gov_chat_send");
        const messages = document.querySelector("#gov_chat_messages");

        button?.addEventListener("click", async () => {
            const text = input.value.trim();
            if (!text) return;
            input.value = "";
            messages.innerHTML += `<div class="msg user">${text}</div>`;
            const res = await this.rpc("/gov_master/chat", {
                message: text,
                session_id: this.props.recordId,
            });
            messages.innerHTML += `<div class="msg bot">${res.reply}</div>`;
        });
    }
}

GovChatInterface.template = "gov_master.GovChatInterface";

registry.category("views").add("gov_chat_interface", GovChatInterface);
