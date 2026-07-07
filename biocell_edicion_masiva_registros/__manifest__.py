# Copyright 2016 Serpent Consulting Services Pvt. Ltd. (support@serpentcs.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
{
    "name": "Mass Editing",
    "version": "15.0.1.0.0",
    "author": "Serpent Consulting Services Pvt. Ltd., "
    "Tecnativa, "
    "GRAP, "
    "Iván Todorovich, "
    "Odoo Community Association (OCA)",
    "category": "Tools",
    "website": "https://github.com/OCA/server-ux",
    "license": "AGPL-3",
    "summary": "Mass Editing",
    "depends": [
        "base",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/ir_actions_server.xml",
        "wizard/biocell_edicion_masiva_registros_wizard.xml",
    ],
    "demo": ["demo/biocell_edicion_masiva_registros.xml"],
}
