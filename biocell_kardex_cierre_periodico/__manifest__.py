# -*- encoding: utf-8 -*-
{
	'name': 'Kardex Save Period IT',
	'category': 'Kardex',
	'author': 'ITGRUPO-KARDEX',
	'depends': ['biocell_kardex_cierre_periodico_2','biocell_kardex_costeo_por_cuentas','biocell_bloqueo_inventario_valorizado'],
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