# -*- encoding: utf-8 -*-
{
	'name': 'Reportes DESTINOS',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_contabilidad_utilidad_083','biocell_auditoria_integridad_datos'],
	'version': '1.0',
	'description':"""
		Generar Reportes para CONSISTENCIA DE DESTINOS, DETALLE DESTINOS, RESUMEN DESTINOS, GENERAR ASIENTOS
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'wizards/account_destinos_rep.xml',
		'views/account_des_detail_book.xml',
		'views/account_des_consistency_book.xml',
		'views/account_des_summary_book.xml',
		'views/account_des_generate_book.xml',
		'views/account_move.xml',
		'views/account_des_move.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
