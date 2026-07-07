# -*- encoding: utf-8 -*-
{
    'name': 'Kardex Fisico',
    'version': '1.0',
    'author': 'ITGRUPO-KARDEX',
    'website': '',
    'category': 'Kardex',
    'depends': ['product','stock','account','biocell_kardex_cierre_periodico_2','biocell_calculo_costo_fabricacion'],
    'description': """KARDEX""",
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'views/stock_picking_views.xml',
        'wizard/make_kardex_view.xml',
        'data/tipo.xml',
        'views/einvoice_catalog_12.xml'
    ],
    'auto_install': False,
    'installable': True
}
