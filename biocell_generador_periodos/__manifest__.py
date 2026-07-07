# -*- encoding: utf-8 -*-
{
	'name': 'Period Generator',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['account','biocell_nucleo_contable_operativo_2','biocell_contabilidad_utilidad_062'],
	'version': '1.0',
	'description':"""
	Generador de Periodos Automatico en base a un Año Fiscal
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'wizard/wizard_biocell_generador_periodos.xml',
		'views/account_fiscal_year.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
