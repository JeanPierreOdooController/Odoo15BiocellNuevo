# -*- encoding: utf-8 -*-
{
	'name': 'Reporte Balances e Inventarios V2',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_herramientas_tributarias','biocell_resumen_existencias_sunat_2','biocell_estado_posicion_financiera','biocell_movimientos_efectivo','biocell_control_capital_patrimonial','biocell_formato_rfun'],
	'version': '1.0',
	'description':"""
		- PLEs Balances e Inventarios 
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'wizards/account_sunat_rep.xml'
	],
	'installable': True
}