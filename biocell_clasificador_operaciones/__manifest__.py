# -*- encoding: utf-8 -*-
{
	'name': 'Cuenta personalizada',
	'category': 'account',
	'author': 'ITGRUPO, Sebastian Moises Loraico Lopez',
	'depends': ['account','biocell_ventanas_emergentes'],
	'version': '1.0',
	'description':"""
	- Cuenta personalizada
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
        'security/ir.model.access.csv',
		'views/account_move.xml',
        'views/account_personalizadas.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
