from odoo import models


class InvoiceWarranty(models.Model):
    _inherit = 'pos.order'

    def get_warranty_details(self):
        # Dummy warranty details; customize as needed
        return {
            'period': '2 Years',
            'terms': 'Standard Manufacturer Warranty',
        }
