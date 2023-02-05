# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        website_page = env["website.page"].browse(
            env.ref("website_accorderie.website_page_home").id
        )
        website_id = website_page.website_id.id
        website_page.view_id = env.ref("website_ore.ir_ui_view_home").id
        website_page.website_id = website_id
