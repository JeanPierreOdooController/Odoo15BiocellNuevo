# -*- encoding: utf-8 -*-
{
	'name': 'Kardex Fields',
	'category': 'Kardex',
	'author': 'ITGRUPO-KARDEX',
	'depends': ['analytic','stock','biocell_nucleo_contable_operativo_2'],
	'version': '1.0',
	'description':"""
	- Agregar campos para Cuentas Analiticas en Albaranes
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
			'views/stock_picking.xml','assets.xml'
		],
	'installable': True
}
