# -*- encoding: utf-8 -*-
{
	'name': 'Hr Payslip Run Move IT',
	'category': 'hr',
	'author': 'ITGRUPO-HR',
	'depends': ['biocell_extensiones_contables_2', 'biocell_motor_reportes', 'biocell_ventanas_emergentes', 'biocell_extensiones_contables'],
	'version': '1.0',
	'description':"""
	Modulo para generar Asiento Contable de Nomina por Lotes
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
			'security/ir.model.access.csv',
			'views/hr_main_parameter.xml',
			'views/hr_payslip_run.xml',
			'views/hr_payslip_run_move.xml',
			'views/hr_salary_rule.xml',
			'wizard/hr_payslip_run_move_wizard.xml',
			'hr_functions.sql'],
	'installable': True,
	'license': 'LGPL-3',
}