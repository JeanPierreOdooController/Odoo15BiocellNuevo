# -*- encoding: utf-8 -*-
{
	'name': 'Hr Importers IT',
	'category': 'hr',
	'author': 'ITGRUPO-HR',
	'depends': ['biocell_extensiones_contables_2','biocell_rrhh_impuesto_quinta'],
	'version': '1.0',
	'description':"""
	Módulo para importar datos de empleados y contratos
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'views/hr_payslip.xml',
		'wizard/hr_import_wizard.xml',
		'wizard/hr_import_wd_wizard.xml',
		'views/hr_menus.xml',
			],
	'installable': True,
	'license': 'LGPL-3',
}