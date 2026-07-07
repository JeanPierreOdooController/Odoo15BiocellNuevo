# -*- encoding: utf-8 -*-
{
    'name': 'Kardex Valorizado Cuentas Contables',
    'version': '1.0',
    'author': 'ITGRUPO-KARDEX',
    'website': '',
    'category': 'Kardex',
    'depends': ['biocell_kardex_costeo_existencias','biocell_extensiones_contables_3'],
    'description': """KARDEX""",
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/make_kardex_view.xml',
    ],
    'auto_install': False,
    'installable': True
}
