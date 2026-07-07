# -*- encoding: utf-8 -*-
{
	'name': 'Importador de Saldos Iniciales IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_nucleo_cargas_masivas'],
	'version': '1.0',
	'description':"""
	Sub-menu para importar saldos de Cliente y Proveedores
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'data/attachment_sample.xml',
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/account_move.xml',
		'views/import_move_apertura_it.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
