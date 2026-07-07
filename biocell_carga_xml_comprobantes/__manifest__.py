# -*- encoding: utf-8 -*-
{
	'name': 'Import XML Invoice',
	'category': 'account',
	'author': 'ITGRUPO,Glenda Julia Merma Mayhua',
	'depends': ['biocell_extensiones_contables','biocell_asistente_llenado_asientos','biocell_nucleo_cargas_masivas','biocell_tipo_cambio_empresa','biocell_reglas_documentos_cliente'],
	'version': '1.0',
	'description':"""
	Modulo para importar Facturas desde XML
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
        'security/security.xml',
		'security/ir.model.access.csv',
		'views/biocell_carga_xml_comprobantes.xml',
		'views/account_tax.xml'
	],
	'installable': True,
	'license': 'LGPL-3'
}