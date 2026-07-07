# -*- encoding: utf-8 -*-
{
	'name': 'Menu Rendiciones',
	'category': 'account',
	'author': 'ITGRUPO, Glenda Julia Merma Mayhua',
	'depends': ['account_accountant','biocell_extensiones_contables','biocell_gestion_tesoreria','biocell_carga_comprobantes'],
	'version': '1.0',
	'description':"""
        MENU DE REPORTES PARA LOCALIZACION CONTABLE
	""",
	'auto_install': False,
	'demo': [],
	'data':	[
		'security/security.xml',
		'security/ir.model.access.csv',
        'views/product_product.xml',
        'views/account_bank_statement.xml',
        'views/biocell_carga_comprobantes_it.xml',
        'views/menu_views.xml'
    ],
	'installable': True
}
