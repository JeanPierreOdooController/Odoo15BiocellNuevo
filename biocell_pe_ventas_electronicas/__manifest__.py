# -*- coding: utf-8 -*-
{
    'name': "Perú Sale - E-invoicing",

    'summary': """
        Adds direct relation between sales and einvoices.""",

    'description': """
        Adds direct relation between sales and einvoices.
    """,

    'author': "Conflux",
    'website': "https://conflux.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization/Peru',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['biocell_pe_facturacion_electronica', 'sale'],

    # always loaded
    'data': [
        
    ]
}