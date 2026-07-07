# -*- encoding: utf-8 -*-
{
	'name': 'Importador de Asientos Contables IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables'],
	'version': '1.0',
	'description':"""
	Importador de Asientos Contables
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'data/attachment_sample.xml',
		'views/biocell_carga_operaciones_contables.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
