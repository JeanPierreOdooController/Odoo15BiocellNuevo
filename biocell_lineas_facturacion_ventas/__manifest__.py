# -*- encoding: utf-8 -*-
{
	'name': 'Sale Line Invoiced Calcule',
	'category': 'account',
	'author': 'ITGRUPO',
	'depends': ['sale','biocell_pe_facturacion_electronica'],
	'version': '1.0',
	'description':"""
	Agregar información a la factura.
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
			'security/security.xml',
			'views/biocell_kardex_fabricacion_2.xml'],
	'installable': True
}
