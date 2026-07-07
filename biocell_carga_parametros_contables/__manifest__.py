# -*- encoding: utf-8 -*-
{
	'name': 'Cargar Plan Contable LC',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_contabilidad_utilidad_062'],
	'version': '1.0',
	'description':"""
		Cargar Plan Contable para LC13
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'data/attachment_sample.xml',
		'sql_update_main_parameter.sql',
		'wizard/upload_chart_account_it.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
