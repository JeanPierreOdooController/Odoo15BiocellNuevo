# -*- encoding: utf-8 -*-
{
	'name': 'Invoice Ebill Stock no obligatorio',
	'category': 'account',
	'author': 'ITGRUPO',
	'depends': ['sale_stock','account','stock','biocell_importaciones_costos_adicionales'],
	'version': '1.0',
	'description':"""
	Agregar información a la factura.
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
			'views/biocell_kardex_fabricacion_2.xml'],
	'installable': True
}
