# -*- coding: utf-8 -*-
{
    'name': "Profisc",
    'version': '2.0',
    'summary': "Profisc Application",
    'sequence': 11,
    'description': """
                    ProFisc eshte nje program i certifikuar per fiskalizimin dhe e-faturen. Test bu_code=ao242je671, "
                   "tcr_code=ds683tq557, operator_code=cw384em859    """,
    'author': "Tetra Pro",
    'category': 'Accounting/Accounting',
    'website': "https://profisc.al/",
    'images': ['static/description/icon.png'],
    'external_dependencies': {'python': ['pyqrcode==1.2.1', 'pypng==0.20220715.0', 'pycountry==22.3.5']},
    'depends': ['base', 'account', 'mail', 'hr', 'point_of_sale', 'stock'],
    'data': [
        'security/ir.model.access.csv',
        'views/account_move_extension.xml',
        'views/res_partner_extension.xml',
        'views/account_payment_term_extension_view.xml',
        'views/account_tax_extension.xml',
        'views/res_users_extension.xml',
        'views/hr_empolyee_exension.xml',
        'views/res_company_extension.xml',
        'views/point_of_sale_orders_ext.xml',
        'views/pos_config_extension.xml',
        'views/pos_tree_order_extension.xml',
        'views/profisc_uoms_management.xml',
        'views/profisc_profisc_management.xml',
        'views/stock_picking_extension.xml',
        'views/stock_warehouse_extension.xml',
        'views/profisc_einvoice_profiles.xml',
        'views/profisc_pos_payment_method.xml',
        'views/profisc_payment_methods.xml',
        'static/data/payment_terms.xml',
        # 'static/data/account_tax_data.xml',
        'static/data/pro_uoms.xml',
        'static/data/einvoice_profiles.xml',
        'static/data/profisc_payment_methods.xml',
        #'views/reports/report_deliveryslip_ext.xml',
        # 'report/invoice_warranty.xml',
        'views/reports/report_template.xml',
        'views/reports/report.xml',
        'report/warranty_record.xml'

    ],
    'installable': True,
    'application': True,
    'assets': {
        'point_of_sale._assets_pos': [
            'profisc/static/src/**/*'
        ],
    },
    'license': 'LGPL-3',
}
