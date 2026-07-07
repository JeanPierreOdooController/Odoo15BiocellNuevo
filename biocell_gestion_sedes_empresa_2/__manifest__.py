# -*- coding: utf-8 -*-
{
    'name': 'Company Branch Address in Account',
    'version': '14.0.1.0.0',
    'category': 'Account',
    'author': 'Conflux',
    'description': "",
    'depends': ['biocell_gestion_sedes_empresa','account'],
    'data': [
        'security/res_biocell_gestion_sedes_empresa_security.xml',
        'views/account_move_view.xml',
    ],
    'installable': True,
    'application': False,
    'license': 'OPL-1',
}