# -*- encoding: utf-8 -*-
{
	'name': 'Importar Facturas IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_nucleo_cargas_masivas','biocell_tipo_cambio_empresa'],
	'version': '1.0',
	'description':"""
	Sub-menu para importar Facturas Cliente/Proveedor
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'data/attachment_sample.xml',
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/biocell_carga_comprobantes_it.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}