/** @odoo-module */
import {PartnerDetailsEdit} from "@point_of_sale/app/screens/partner_list/partner_editor/partner_editor";
import {patch} from "@web/core/utils/patch";

const id_types = [
    {value: "ID", label: "ID"},
    {value: "9923", label: "NUIS"},
    {value: "VAT", label: "VAT"}]

patch(PartnerDetailsEdit.prototype, {
    setup() {
        super.setup(...arguments);
        this.props.id_types = id_types;

        const selectedPartner = this.props.partner;
        this.changes.profisc_customer_vat_type = selectedPartner.profisc_customer_vat_type

        console.log({selectedPartner, "this.changes": this.changes})

    }
});