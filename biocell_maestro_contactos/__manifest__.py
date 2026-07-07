# -*- encoding: utf-8 -*-
{
	'name': 'Importador De Contactos',
	'category': 'contacts',
	'author': 'ITGRUPO',
	'depends': ['contacts','l10n_latam_base','biocell_ventanas_emergentes','biocell_extensiones_contables'],
	'version': '1.0',
	'description':"""
		Importador De Contactos
	""",
	'auto_install': False,
	'demo': [],
	'data': [
		'security/ir.model.access.csv',
        'security/res_partner_seucirty.xml',
        'data/attachment_sample.xml',
        'views/res_partner_view.xml',
    ],
	'installable': True
}