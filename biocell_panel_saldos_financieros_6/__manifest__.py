# -*- encoding: utf-8 -*-
{
	'name': 'Stock Balance Report Clinica',
	'category': 'stock',
	'author': 'ITGRUPO',
	'depends': ['biocell_panel_saldos_financieros_4','biocell_kardex_movimientos_fisicos'],
	'version': '1.0',
	'description':"""
	Reporte de Saldos
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/biocell_panel_saldos_financieros_4.xml'
	],
	'installable': True
}
