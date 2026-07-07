# -*- encoding: utf-8 -*-
{
	'name': 'Invoice Ebill Stock',
	'category': 'account',
	'author': 'ITGRUPO',
	'depends': ['sale_stock','biocell_emision_electronica_almacen_2','account','stock'],
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
