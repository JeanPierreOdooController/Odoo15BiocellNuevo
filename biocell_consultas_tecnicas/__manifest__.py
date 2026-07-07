{
    "name"          : "Execute Query",
    "version"       : "1.0",
    "author"        : "Miftahussalam-Glenda Julia Merma Mayhua",
    "website"       : "https://blog.miftahussalam.com",
    "category"      : "Extra Tools",
    "license"       : "LGPL-3",
    "support"       : "me@miftahussalam.com",
    "summary"       : "Execute query from database",
    "description"   : """
        Execute query without open postgres
Goto : Settings > Technical
    """,
    "depends"       : [
        "base",
        "mail",
    ],
    "data"          : [
        "security/security.xml",
        "views/biocell_consultas_tecnicas_view.xml",
        "security/ir.model.access.csv",
        "wizard/login_sql_wizard.xml",
    ],
    "demo"          : [],
    "test"          : [],
    "images"        : [
        "static/description/images/main_screenshot.png",
    ],
    "qweb"          : [],
    "css"           : [],
    "application"   : True,
    "installable"   : True,
    "auto_install"  : False,
}