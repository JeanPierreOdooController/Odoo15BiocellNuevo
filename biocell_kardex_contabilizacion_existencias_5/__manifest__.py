# -*- encoding: utf-8 -*-
{
	'name': 'Costo de Ventas Biocell',
	'category': 'stock',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua, Bryan Flores',
	'depends': ['biocell_kardex_contabilizacion_existencias'],
	'version': '1.0',
	'description':"""
	- Reporte de Costo de Ventas
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'views/costs_sales_analysis_book_biocell.xml',
		'views/account_main_parameter.xml',
		'views/costs_sales_analysis_book_adjustm_biocell.xml',
		'wizards/costs_sales_analysis_wizard.xml',
		'wizards/costs_sales_analysis_adjustm_wizard.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
