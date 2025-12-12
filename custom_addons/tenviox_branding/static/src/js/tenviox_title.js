/** @odoo-module **/

import { WebClient } from "@web/webclient/webclient";
import { patch } from "@web/core/utils/patch";
import { useService } from "@web/core/utils/hooks";

// Patch WebClient to override the title logic
patch(WebClient.prototype, {
    setup() {
        super.setup();
        const titleService = useService("title");
        // 强制设置基础标题为 TenvioX
        titleService.setParts({ z_openerp: "TenvioX" });
    }
});