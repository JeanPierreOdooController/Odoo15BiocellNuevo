# -*- encoding: utf-8 -*-
{
	'name': 'Aprobaciones IT',
	'category': 'account',
	'author': 'ITGRUPO-OBSOLETO',
	'depends': ['biocell_importaciones_costos_adicionales','biocell_kardex_costeo_existencias','stock'],
	'version': '1.0',
	'description':"""
		Permisos para Aprobar en los modulos contables y de gestion
	""",
	'auto_install': False,
	'demo': [],
	'data':	['security/ir.model.access.csv','security/purchase_national_security.xml','account_journal_view.xml'],
	'installable': True
}
