# -*- encoding: utf-8 -*-
{
	'name': 'Apertura Contable It',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_contabilidad_utilidad_083','biocell_cruces_contables_especiales'],
	'version': '1.0',
	'description':"""
	Sub-menu para creacion de Aperturas Contables
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/biocell_arranque_periodo_contable.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
