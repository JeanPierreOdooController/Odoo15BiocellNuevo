# -*- encoding: utf-8 -*-
{
	'name': 'Solicitudes de Entrega IT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_control_entregas_rendir','biocell_cruce_movimientos_bancarios'],
	'version': '1.0',
	'description':"""
	- Solicitudes de Entrega
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/render_type_document.xml',
		'views/render_main_parameter.xml',
		'views/account_bank_statement.xml',
		'views/biocell_contabilidad_utilidad_093.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}