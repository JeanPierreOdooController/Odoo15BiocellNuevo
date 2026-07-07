# -*- encoding: utf-8 -*-
{
	'name': 'Reporte Balances e Inventarios V2',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_resumen_existencias_sunat'],
	'version': '1.0',
	'description':"""
		- PLEs Balances e Inventarios
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/sunat_table_data.xml',
		'views/menu_views.xml'
	],
	'installable': True
}