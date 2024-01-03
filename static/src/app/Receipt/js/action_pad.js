/** @odoo-module */

import {ActionpadWidget} from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import {patch} from "@web/core/utils/patch";

const id_types = [
    {value: "ID", label: "ID"},
    {value: "9923", label: "NUIS"},
    {value: "VAT", label: "VAT"}]


patch(ActionpadWidget.prototype, {


    setup() {
        super.setup(...arguments);
        this.props.show_profisc = false
        // this.currentOrder = this.env.services.pos.get_order();
        this.currentCompany = this.env.services.pos.company;
        this.checkCompanyParams();
        this.props.changeFiscType = this.changeFiscType;
        this.props.id_types = id_types;

    },
    checkCompanyParams() {
        this.props.show_profisc = this.currentCompany.profisc_manual_fisc_select;
    },
    setProfiscType(type = "0") {
        if (this.currentOrder) {
            this.currentOrder.profisc_fisc_type = type;
            // console.log({order: this.currentOrder}); // This will log the value of the selected option
        }
    },
    changeFiscType() {
        const dropdown = document.querySelector('.changeFiscType');
        this.setProfiscType(dropdown.options[dropdown.selectedIndex].value);


    }
});