{
    "name": "Website ORE",
    "category": "Website",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "application": True,
    "depends": ["website", "website_accorderie"],
    "data": [
        "views/website_page.xml",
        "data/ir_attachment.xml",
        "views/ir_ui_view.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
}
