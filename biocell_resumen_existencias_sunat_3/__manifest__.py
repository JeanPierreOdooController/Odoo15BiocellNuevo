# -*- encoding: utf-8 -*-
{
	'name': 'Reporte PLE Balances e Inventarios',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_resumen_existencias_sunat','biocell_gestion_bienes_empresa_3','biocell_kardex_costeo_por_cuentas','biocell_extensiones_contables_3','biocell_contabilizacion_inventario'],
	'version': '1.0',
	'description':"""
		- PLEs Balances e Inventarios
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'SQL.sql',
		'wizards/biocell_ventanas_emergentes_balance_inventory.xml',
		'wizards/account_sunat_balance_inventory_rep.xml'
	],
	'installable': True
}