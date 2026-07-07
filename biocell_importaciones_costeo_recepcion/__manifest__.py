# -*- encoding: utf-8 -*-
{
	'name': 'Existencias por Recibir IT',
	'category': 'Kardex',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_importaciones_costos_adicionales'],
	'version': '1.0',
	'description':"""
	- Existencias por Recibir
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'views/account_main_parameter.xml',
		'views/biocell_importaciones_costos_adicionales.xml',
		'views/product_category.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}