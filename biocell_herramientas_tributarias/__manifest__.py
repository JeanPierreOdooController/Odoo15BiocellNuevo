# -*- encoding: utf-8 -*-
{
	'name': 'Reporte PLE SUNAT',
	'category': 'account_sunat',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_motor_fiscal_peruano','biocell_ventanas_emergentes','biocell_motor_reportes'],
	'version': '1.0',
	'description':"""
		- Nuevo menu SUNAT para generar PLEs
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'wizards/account_sunat_wizard.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}