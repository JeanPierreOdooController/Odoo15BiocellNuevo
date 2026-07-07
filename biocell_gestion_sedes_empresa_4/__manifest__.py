# -*- coding: utf-8 -*-
{
    'name': "Perú Company Branch - E-invoicing Despatchs",

    'summary': """
        Adds Despatch Integration with company branch.""",

    'description': """
        Adds Despatch Integration with company branch.
    """,

    'author': "Conflux",
    'website': "https://conflux.pe",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Localization/Peru',
    'version': '15.0.1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['biocell_pe_facturacion_electronica_despatch', 'biocell_pe_facturacion_electronica_company_branch'],

    # always loaded
    'data': [
    ]
}