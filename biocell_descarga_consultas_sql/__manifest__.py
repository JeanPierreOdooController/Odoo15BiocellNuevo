# Copyright (C) 2015 Akretion (<http://www.akretion.com>)
# @author: Florian da Costa
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).

{
    "name": "SQL Export",
    "version": "14.0.1.1.0",
    "author": "Akretion,Odoo Community Association (OCA),ITGRUPO",
    "website": "https://github.com/OCA/server-tools",
    "license": "AGPL-3",
    "category": "Generic Modules/Others",
    "summary": "Export data in csv file with SQL requests",
    "depends": [
        "biocell_modelo_consultas_sql",
    ],
    "data": [
        "views/biocell_descarga_consultas_sql_view.xml",
        "wizard/wizard_file_view.xml",
        "security/biocell_descarga_consultas_sql_security.xml",
        "security/ir.model.access.csv",
    ],
    "demo": [
        "demo/biocell_descarga_consultas_sql.xml",
    ],
    "installable": True,
}
