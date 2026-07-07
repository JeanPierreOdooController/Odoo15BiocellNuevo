# -*- encoding: utf-8 -*-
{
	'name': 'Menu Reportes de Localizacion Contable',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_motor_reportes'],
	'version': '1.0',
	'description':"""
	- MENU DE REPORTES PARA LOCALIZACION CONTABLE
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'libro_contables_peruanos.sql',
		'cuentas_corrientes.sql',
		'estados_financieros.sql',
		'views/biocell_contabilidad_utilidad_083.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}
