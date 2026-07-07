# -*- encoding: utf-8 -*-
{
	'name': 'Cierre Contable It',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables'],
	'version': '1.0',
	'description':"""
	Sub-menu para creacion de Cierres Contables
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/biocell_proceso_cierre_periodo.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
