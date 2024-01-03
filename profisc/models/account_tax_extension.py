from odoo import api, fields, models


class AccountTaxExtension(models.Model):
    _inherit = ['account.tax']

    profisc_tax_exempt_reason = fields.Selection(
        [('EXPORT_OF_GOODS', 'EXPORT_OF_GOODS'), ('TAX_FREE', 'TAX_FREE'), ('TYPE_1', 'TYPE_1'), ('TYPE_2', 'TYPE_2'),
         ('MARGIN_SCHEME', 'MARGIN_SCHEME')],
        string='CIS Type', store=True)
