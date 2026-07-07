# -*- encoding: utf-8 -*-
{
	'name': 'Tipo de Cambio de Cierre',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_tipo_cambio_empresa_3','biocell_contabilidad_utilidad_083'],
	'version': '1.0',
	'description':"""
	Sub-menu con Tabla de Tipos de Cambio de Cierre
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'wizards/account_exchange_rep.xml',
		'wizards/account_exchange_document_rep.xml',
		'wizards/account_exchange_document_usd_rep.xml',
		'views/account_main_parameter.xml',
		'views/exchange_diff_config.xml',
		'views/account_exchange_book.xml',
		'views/account_exchange_document_book.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
