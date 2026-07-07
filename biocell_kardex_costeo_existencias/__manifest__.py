# -*- encoding: utf-8 -*-
{
    'name': 'Kardex Valorado',
    'version': '1.0',
    'author': 'ITGRUPO-KARDEX',
    'website': '',
    'category': 'Kardex',
    'depends': ['biocell_kardex_cierre_periodico_2','biocell_kardex_movimientos_fisicos','biocell_extensiones_contables_3','purchase_stock','account'],
    'description': """KARDEX""",
    'demo': [],
    'data': [
        'security/ir.model.access.csv',
        'wizard/make_kardex_view.xml',
    ],
    'auto_install': False,
    'installable': True
}
