# -*- encoding: utf-8 -*-
{
	'name': 'Kardex Save Period IT',
	'category': 'Kardex',
	'author': 'ITGRUPO-KARDEX',
	'depends': ['stock','biocell_extensiones_contables_3','biocell_ventanas_emergentes'],
	'version': '1.0',
	'description':"""
	- Kardex almacenado mensual
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/kardex.xml',
		],
	'installable': True
}