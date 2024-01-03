/** @odoo-module */

import {Order} from "@point_of_sale/app/store/models";
import {patch} from "@web/core/utils/patch";


patch(Order.prototype, {
    setup() {
        super.setup(...arguments);
        this.createQrImage = this.createQrImage.bind(this);
    },
    getOrderData() {
        this.originalData = super.export_for_printing(...arguments);
        let current_order = this.env.services.pos.get_order();
        this.env.services.orm.call('pos.order', 'get_profisc_fields', [current_order.access_token]).then(function (result) {
            this.originalData.profisc_iic = result['profisc_iic']
            this.originalData.profisc_fic = result['profisc_fic']
            this.originalData.profisc_ubl_id = result['profisc_ubl_id']
            if (!this.originalData.profisc_fic) {
                this.originalData.profisc_fic = "Statusi i Faturës referuar Ligjit do të bëhet e ditur jo më vonë se 48 orë nga koha e lëshimit! Ju lutem, provoni përsëri me vonë."
            }
            this.originalData.profisc_eic = result['profisc_eic']
            this.originalData.profisc_qr_code = result['profisc_qr_code']
            this.originalData.profisc_fic_error_code = result['profisc_fic_error_code']
            this.originalData.profisc_fic_error_description = result['profisc_fic_error_description']
            this.createQrImage()

        }.bind(this)).catch(function (error) {
            console.error("Error:", error);
        });
        return this.originalData;
    },
    export_for_printing() {

        if (!this.originalData)
            this.getOrderData();

        return this.originalData;
    },
    createQrImage() {
        const codeWriter = new window.ZXing.BrowserQRCodeSvgWriter();
        let qr_code_svg = new XMLSerializer().serializeToString(codeWriter.write(this.originalData.profisc_qr_code, 150, 150));
        this.originalData.qrCode = 'data:image/svg+xml;base64,' + window.btoa(qr_code_svg);
    }, init_from_JSON(json) {
        super.init_from_JSON(...arguments);
        this.profisc_ubl_id = json.profisc_ubl_id
        this.profisc_iic = json.profisc_iic
        this.profisc_fic = json.profisc_fic
        this.profisc_eic = json.profisc_eic
        this.profisc_qr_code = json.profisc_qr_code
        this.profisc_fic_error_code = json.profisc_fic_error_code
        this.profisc_fic_error_description = json.profisc_fic_error_description
    }
});
