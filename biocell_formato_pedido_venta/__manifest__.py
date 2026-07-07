# -*- encoding: utf-8 -*-
{
	'name': 'Reporte de ventas',
	'category': 'sale',
	'author': 'ITGRUPO,berth',
	'depends': ['sale','biocell_pedidos_comerciales_2','biocell_nucleo_contable_operativo','biocell_tipo_cambio_empresa_3','biocell_parametros_ajuste_cambiario','biocell_generador_excel'],
	'version': '1.0',
	'auto_install': False,
	'demo': [],
	'data':	[
        'reports/report_sale_order.xml',
        'views/sale_order_button_excel.xml'
        ],
	'installable': True,
	'license': 'LGPL-3'
}
