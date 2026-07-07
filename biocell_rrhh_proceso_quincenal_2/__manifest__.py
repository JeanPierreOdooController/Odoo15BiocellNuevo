# -*- encoding: utf-8 -*-
{
	'name': 'Hr Pagos Quincenales Biocells',
	'category': 'hr',
	'author': 'ITGRUPO-HR',
	'depends': ['biocell_rrhh_proceso_quincenal'],
	'version': '1.0',
	'description':"""
	Personalizacion para calculo de AF en pagos quincenales
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		# 'security/ir.model.access.csv',
		# 'security/security.xml',
		'views/hr_main_parameter.xml'
			],
	'installable': True,
	'license': 'LGPL-3',
}