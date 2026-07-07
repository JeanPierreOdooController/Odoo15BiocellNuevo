# -*- encoding: utf-8 -*-
{
	'name': 'Account Bank Statement Reconcile IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_ventanas_emergentes'],
	'version': '1.0',
	'description':"""
		Modulo para agregar Tipo de Documento y Numero de Comprobante a las lineas de Asiento Generadas por extractos
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'views/account_bank_statement.xml',
	],
	'installable': True,
	'license': 'LGPL-3'
}
