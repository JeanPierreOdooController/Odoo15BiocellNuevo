# -*- encoding: utf-8 -*-
{
	'name': 'Hr Provisions',
	'category': 'hr',
	'author': 'ITGRUPO-HR',
	'depends': ['biocell_rrhh_beneficios_personal'],
	'version': '1.0',
	'description':"""
	Modulo de Provisiones	
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
		'views/hr_main_parameter.xml',
		'views/biocell_rrhh_provisiones_laborales.xml',
		'wizard/biocell_rrhh_provisiones_laborales_wizard.xml'
	],
	'installable': True,
	'license': 'LGPL-3',
}
