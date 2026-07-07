# -*- encoding: utf-8 -*-
{
	'name': 'Detalle de Movimientos en Asientos Contables',
	'category': 'stock',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_extensiones_contables_3','biocell_kardex_movimientos_fisicos','biocell_kardex_costeo_por_cuentas','biocell_kardex_contabilizacion_existencias'],
	'version': '1.0',
	'description':"""
	- Detalle de Movimientos en Asientos Contables
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'SQL.sql',
		'security/ir.model.access.csv',
		'wizards/kardex_entry_income_wizard.xml',
		'wizards/kardex_entry_outcome_wizard.xml',
		'views/account_main_parameter.xml',
		'views/kardex_entry_income_book.xml',
		'views/kardex_entry_outcome_book.xml',
		'views/type_operation_kardex.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
