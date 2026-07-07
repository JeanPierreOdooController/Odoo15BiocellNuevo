# -*- encoding: utf-8 -*-
{
	'name': 'Actualizar cuentas predeterminadas',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['account','biocell_contabilidad_utilidad_062','biocell_ventanas_emergentes'],
	'version': '1.0',
	'description':"""
		Actualizar cuentas predeterminadas por compañía
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'wizard/update_default_accounts_wizard.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
