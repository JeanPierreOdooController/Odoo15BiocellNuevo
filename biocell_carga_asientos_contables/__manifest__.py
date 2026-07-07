# -*- encoding: utf-8 -*-
{
	'name': 'Importador de Apuntes Contables',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables'],
	'version': '1.0',
	'description':"""
	Modulo para importar Apuntes Contables
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'data/attachment_sample.xml',
		'views/account_move.xml',
        'wizard/import_move_line_wizard.xml',
		],
	'installable': True,
	'license': 'LGPL-3'
}
