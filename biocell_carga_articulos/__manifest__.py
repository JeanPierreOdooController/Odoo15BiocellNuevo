# -*- coding: utf-8 -*-

{
	'name': 'Importar Productos IT',
	'category': 'Stock',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_ventanas_emergentes','biocell_nucleo_contable_operativo_2','biocell_nucleo_cargas_masivas'],
	'version': '1.0',
	'description':"""
	- Importar producto
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'data/attachment_sample.xml',
		'security/ir.model.access.csv',
        'security/product_import_security.xml',
		'views/import_product.xml',
	],
	'installable': True,
	'license': 'LGPL-3'
}