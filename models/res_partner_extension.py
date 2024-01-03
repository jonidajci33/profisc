from odoo import api, fields, models
import base64
from server.odoo import http
from server.odoo.http import request


class ResPartnerExtension(models.Model):
    _inherit = ['res.partner']

    profisc_customer_vat_type = fields.Selection([
        ('ID', 'ID'),
        ('9923', 'NUIS'),
        ('VAT', 'VAT '),
    ], string='Customer Vat Type', default='ID')

    def get_tax_payer(self):
        self.env['profisc.api.helper'].getTaxPayer(self.vat)

    @api.model
    def action_print_custom_report(self, partner):

        print(partner['id'])
        report = self.env['ir.actions.report']
        partner_ids = [partner['id']] if isinstance(partner['id'], int) else partner['id']
        pdf_content = report._render_qweb_pdf("profisc.report_warranty", res_ids=partner_ids)
        # Assuming _render_qweb_pdf returns a tuple with the PDF content first

        # Encode the PDF content to Base64
        base64_encoded_pdf = base64.b64encode(pdf_content[0]).decode('utf-8')

        return base64_encoded_pdf

