# -*- encoding: utf-8 -*-
{
	'name': 'Importar Rec x Hon de TXT',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_nucleo_cargas_masivas','biocell_tipo_cambio_empresa'],
	'version': '1.0',
	'description':"""
	Importar Rec x Hon de TXT
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
        'security/security.xml',
		'security/ir.model.access.csv',
		'views/import_recxhon_wizard.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}