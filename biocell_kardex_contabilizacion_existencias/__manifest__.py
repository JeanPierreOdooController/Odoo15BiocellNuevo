# -*- encoding: utf-8 -*-
{
	'name': 'Analisis de Consumo, Costo de Ventas',
	'category': 'stock',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_extensiones_contables_3','biocell_kardex_movimientos_fisicos','biocell_kardex_costeo_por_cuentas'],
	'version': '1.0',
	'description':"""
	- Reporte de Analisis de Consumo
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'SQL.sql',
		'security/ir.model.access.csv',
		'wizards/consumption_analysis_wizard.xml',
		'wizards/costs_sales_analysis_wizard.xml',
		'wizards/production_income_wizard.xml',
		'views/account_main_parameter.xml',
		'views/consumption_analysis_book.xml',
		'views/costs_sales_analysis_book.xml',
		'views/production_income_book.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
