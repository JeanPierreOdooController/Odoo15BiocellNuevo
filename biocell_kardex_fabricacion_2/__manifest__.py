# -*- encoding: utf-8 -*-
{
	'name': 'Control en Ordenes de Produccion',
	'category': 'account',
	'author': 'ITGRUPO',
	'depends': ['mrp', 'biocell_kardex_movimientos_fisicos','biocell_extensiones_contables_3'],
	'version': '1.0',
	'description':"""
	Modulo para agregar Raise en Ordenes de Produccion y algunos campos.
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
			'security/security.xml',
			'views/biocell_kardex_fabricacion_2.xml'],
	'installable': True
}
