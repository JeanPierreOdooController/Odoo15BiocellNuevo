# -*- encoding: utf-8 -*-
{
	'name': 'Diferencia Analitica VS Contabilidad',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_distribucion_centros_costo','biocell_motor_reportes'],
	'version': '1.0',
	'description':"""
	- Exportacion de Diferencia Analitica VS Contabilidad
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'views/account_diff_destino_analitica_view.xml',
		'wizards/account_diff_destino_analitica_wizard.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
