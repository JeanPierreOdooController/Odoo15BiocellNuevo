# -*- encoding: utf-8 -*-
{
	'name': 'Verificar si hay saltos de numeracion Voucher',
	'category': 'account',
	'author': 'ITGRUPO-Glenda Julia',
	'depends': ['biocell_auditoria_integridad_datos','biocell_motor_reportes'],
	'version': '1.0',
	'description':"""
	- Reporte para verificar saltos de numeración en cheques
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'wizard/check_voucher_skip_detection_wizard.xml'
	],
	'installable': True
}