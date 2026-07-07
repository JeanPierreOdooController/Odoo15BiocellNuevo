# -*- encoding: utf-8 -*-
{
    'name': 'Kardex',
    'version': '1.0',
    'author': 'ITGRUPO-KARDEX',
    'website': '',
    'category': 'account',
    'depends': ['biocell_kardex_costeo_existencias','product_expiry'],
    'description': """KARDEX""",
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/make_kardex_view.xml',
    ],
    'auto_install': False,
    'installable': True
}
