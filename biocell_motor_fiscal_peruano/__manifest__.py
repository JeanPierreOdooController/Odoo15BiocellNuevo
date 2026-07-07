# -*- encoding: utf-8 -*-
{
	'name': 'Reporte PLE SUNAT',
	'category': 'account_sunat',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_contabilidad_utilidad_083','biocell_tipo_cambio_empresa_3'],
	'version': '1.0',
	'description':"""
		- Nuevo menu SUNAT para generar PLEs
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/account_sunat_menu.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}