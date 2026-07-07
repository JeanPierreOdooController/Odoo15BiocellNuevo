# -*- encoding: utf-8 -*-
{
	'name': 'Importar Detracciones IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_nucleo_cargas_masivas'],
	'version': '1.0',
	'description':"""
	- Se crea el menú Actualizar Detracciones
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'data/attachment_sample.xml',
		'security/ir.model.access.csv',
		'wizard/import_detrac_wizard.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
