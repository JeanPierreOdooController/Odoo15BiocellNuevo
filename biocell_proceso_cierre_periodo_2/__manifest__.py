# -*- encoding: utf-8 -*-
{
	'name': 'Cierre Gastos Vinculados IT',
	'category': 'Kardex',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_importaciones_costos_adicionales'],
	'version': '1.0',
	'description':"""
	- Cierre Gastos Vinculados
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/biocell_proceso_cierre_periodo_2.xml',
		'views/biocell_importaciones_costos_adicionales.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}