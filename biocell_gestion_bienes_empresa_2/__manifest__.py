# -*- encoding: utf-8 -*-
{
	'name': 'Importar Activos IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_nucleo_cargas_masivas','biocell_gestion_bienes_empresa_3'],
	'version': '1.0',
	'description':"""
	- Se crea el menú Importar Activos
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'data/attachment_sample.xml',
		'security/ir.model.access.csv',
		'wizard/import_asset_wizard.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
