# -*- coding: utf-8 -*-
{
    'name': "Integration EDI - IT Grupo Catalogs",
    'description': """
Integracion de catalogos de sunat IT Grupo con facturacion electronica internacional
    """,

    'author': "Conflux",
    'website': "https://conflux.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['biocell_pe_facturacion_electronica', 'biocell_nucleo_contable_operativo_2', 'biocell_gestion_devoluciones_comerciales','biocell_gestion_sedes_empresa_3'],

    # always loaded
    'data': [
        #'views/account_move_view.xml',
        'views/biocell_gestion_sedes_empresa_view.xml',
        'views/report_invoice.xml',
    ]
}
