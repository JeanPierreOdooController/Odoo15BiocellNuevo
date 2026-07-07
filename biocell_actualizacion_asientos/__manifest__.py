# -*- encoding: utf-8 -*-
{
	'name': 'Actualizador Datos Adicionales IT',
	'category': 'account',
	'author': 'ITGRUPO',
	'depends': ['biocell_extensiones_contables','biocell_nucleo_cargas_masivas'],
	'version': '1.0',
	'description':"""
	- Se crea el menú Actualizar datos adicionales
	- Se crea el menú Añadir documentos relacionados 
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/ir.model.access.csv',
		'data/attachment_sample.xml',
		'wizard/update_journal_entry_it.xml',
		'wizard/add_doc_invoice_relac_wizard.xml'
		],
	'installable': True
}
