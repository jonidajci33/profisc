from odoo import api, fields, models


class AccountMoveExtension(models.Model):
    _inherit = 'account.move'

    profisc_cis_type = fields.Selection(
        [('0', 'No Fiscalization'), ('-1', 'Fiscalization'), ('1', 'E-Invoice')],
        string='CIS Type', store=True, default='0')

    profisc_fisc_status = fields.Char(string='Fiscal Status')
    profisc_iic = fields.Char(string='IIC')
    profisc_fic = fields.Char(string='FIC')
    profisc_eic = fields.Char(string='EIC')
    profisc_qr_code = fields.Char(string='Qr Url')
    profisc_qr_code_check = fields.Binary(string='Qr Code', attachment=True)
    profisc_fisc_downloaded = fields.Boolean(string='Fiscal Downloaded')
    profisc_einvoice_downloaded = fields.Boolean(string='E-Invoice Downloaded')
    profisc_fic_error_code = fields.Char(string='FIC Error Code')
    profisc_fic_error_description = fields.Char(string='FIC Error Description')
    profisc_eic_error_code = fields.Char(string='EIC Error Code')
    profisc_eic_error_description = fields.Char(string='EIC Error Description')
    profisc_ubl_id = fields.Char(string='UBL ID')

    profisc_invoice_type = fields.Selection(
        [('380', 'Commercial'), ('384', 'Corrective'), ('389', 'Self-billed Invoice')],
        string='Invoice Type', store=True, )

    # profisc_tcr_code = fields.Selection([
    #     ('ch226pz644', 'ch226pz644'),
    # ], store=True, string='TCR Code')

    # profisc_bu_code = fields.Selection([
    #     ('cs862wh907', 'Tetra PRO - Tirane, Kompleksi KIKA 2, Rruga "Tish Daija", kati i dyte, godina Nr.7, '
    #                    'njesia Bashkiake Nr.5, Tirane'),
    # ], store=True, string='Bu Code')

    profisc_tcr_code = fields.Selection(selection='_get_tcr_list', string='TCR')
    profisc_bu_code = fields.Selection(selection='_get_business_units', string='Business Unit')

    profisc_status_control = fields.Selection([('0', 'In Process'), ('2', 'Error'), ('3', 'Success'), ], store=True,
                                              string='Status Control')

    profisc_profile_id = fields.Selection([
        ('P1', 'P1 - Invoicing the supply of goods and services ordered on a contract basis'),
        ('P2', 'P2 - Periodic invoicing of contract-based delivery'),
        ('P10', 'P10 - Corrective Invoice'),
        ('P12', 'P12 - Self Invoice'),
    ], store=True, string='Profile ID', default='P1')

    profisc_subseq = fields.Selection([
        ('NO INTERNET', 'NO INTERNET'),
        ('SERVICE', 'SERVICE'),
        ('TECHNICAL ERROR', 'TECHNICAL ERROR'),
        ('BOUNDBOOK', 'BOUNDBOOK'),
    ], store=True, string='Subseq')
    profisc_start_date = fields.Date(string='Start Date')
    profisc_end_date = fields.Date(string='End Date')
    profisc_reference_invoice_date = fields.Date(string='Reference Invoice Date')
    profisc_reference_invoice_iic = fields.Char(string='Reference Invoice IIC')

    profisc_self_invoice_type = fields.Selection([
        ('AGREEMENT', 'AGREEMENT'),
        ('DOMESTIC', 'DOMESTIC'),
        ('ABROAD', 'ABROAD'),
        ('SELF', 'SELF'),
        ('OTHER', 'OTHER'),
    ], store=True, string='Self Invoice Type')
    profisc_reverse_charge = fields.Boolean(string='Reverse Charge')

    def _get_business_units(self):
        bus = self.env['profisc.business_units'].search([('company_id', '=', self.env.company.id)])
        return [(bu.code, bu.code) for bu in bus]

    def _get_tcr_list(self):
        bus = self.env['profisc.tcr'].search([('company_id', '=', self.env.company.id)])
        return [(bu.code, bu.code) for bu in bus]

    def send_to_profisc(self):
        self.env['profisc.api.helper'].sendToProfisc(self.id)

    def get_fisc_pdf(self):
        self.env['profisc.api.helper'].getFiscPdf(self.id)

    def get_e_invoice_pdf(self):
        self.env['profisc.api.helper'].getEinvoicePdf(self.id)

    def get_qr_code(self):
        self.env['profisc.api.helper'].getQrCode(self.id)
