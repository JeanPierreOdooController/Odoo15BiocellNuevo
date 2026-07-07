# -*- encoding: utf-8 -*-
{
	'name': 'Sale Stock Return',
	'category': 'stock,sale',
	'author': 'ITGRUPO',
	'depends': ['sale_stock','biocell_logistica_operativa','biocell_asignacion_deposito_defecto','biocell_meta_comercial','product_expiry'],
	'version': '1.0',
	'description':"""
	Stock Venta
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
			'security/ir.model.access.csv',
			'views/menu_items.xml',
			],
	'installable': True,
	'license': 'LGPL-3'
}
