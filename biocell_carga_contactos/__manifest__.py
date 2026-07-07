# -*- coding: utf-8 -*-

{
	'name': 'Importar Partner IT',
	'category': 'Base',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['contacts','biocell_extensiones_contables','biocell_ventanas_emergentes','biocell_nucleo_cargas_masivas'],
	'version': '1.0',
	'description':"""
	- Importar Partner
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'data/attachment_sample.xml',
		'security/ir.model.access.csv',
		'views/biocell_carga_contactos.xml',
	],
	'installable': True,
	'license': 'LGPL-3'
}
