{
    "name": "ORE",
    "category": "Website",
    "version": "12.0.1.0",
    "author": "TechnoLibre",
    "license": "AGPL-3",
    "website": "https://technolibre.ca",
    "application": True,
    "depends": ["accorderie", "muk_branding"],
    "data": [
        "data/ir_attachment.xml",
    ],
    "pre_init_hook": "pre_init_hook",
    "post_init_hook": "post_init_hook",
    "installable": True,
}
