# -*- encoding: utf-8 -*-
{
	'name': 'Kardex Save Period IT Updated',
	'category': 'Kardex',
	'author': 'ITGRUPO-KARDEX',
	'depends': ['stock','biocell_kardex_cierre_periodico_2','biocell_kardex_cierre_periodico','biocell_kardex_ajuste_traslados'],
	'version': '1.0',
	'description':"""
	- Kardex almacenado mensual Mejoras
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'views/kardex.xml',
		'views/ir.model.access.csv',
		],
	'installable': True
}