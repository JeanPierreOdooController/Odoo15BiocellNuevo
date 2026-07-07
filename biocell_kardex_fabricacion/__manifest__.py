# -*- encoding: utf-8 -*-
{
	'name': 'Kardex Mrp Production',
	'category': 'Kardex',
	'author': 'ITGRUPO-MRP-KARDEX',
	'depends': ['biocell_kardex_costeo_existencias', 'mrp','biocell_kardex_fabricacion_2', 'biocell_panel_saldos_financieros_4','biocell_marcas_articulos'],
	'version': '1.0',
	'description':"""
	Modulo para añadir lineas de OP's en Kardex Fisico
	""",
	'auto_install': False,
	'demo': [],
	'data':	['wizard/make_kardex_view.xml'],
	'installable': True
}
