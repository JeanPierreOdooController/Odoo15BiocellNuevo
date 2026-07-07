# -*- encoding: utf-8 -*-
{
	'name': 'Plantilla de presupuesto personalizada',
	'category': 'sale',
	'author': 'ITGRUPO,berth',
	'depends': ['sale','sale_management','biocell_pedidos_plantillas','account','stock'],
	'version': '1.0',
	
	'auto_install': False,
	'demo': [],
	'data':	[
		'views/sale_order_template.xml'
		],
	'installable': True,
	'license': 'LGPL-3'
}
