# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import base64
import logging

from odoo import SUPERUSER_ID, _, api, tools

_logger = logging.getLogger(__name__)


def pre_init_hook(cr):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        company_id = env["res.partner"].browse(env.ref("base.main_company").id)
        company_id.website = "https://ore.nuagelibre.ca"
        company_id.name = "ORE"
        company_id.email = "info@cimarlab.ca"
        company_id.city = "Québec"
        company_id.country_id = env.ref("base.ca")
        company_id.state_id = env["res.country.state"].search(
            [("code", "ilike", "QC")], limit=1
        )

        company_id = env["res.company"].browse(1)
        # Force sequence 1, the warehouse will be first will multi-company
        company_id.sequence = 1

        user_admin_id = env["res.partner"].browse(
            env.ref("base.partner_admin").id
        )
        user_admin_id.website = "https://technolibre.ca"
        user_admin_id.name = "Mathieu Benoit"
        user_admin_id.email = "mathieu.benoit@technolibre.ca"
        user_admin_id.country_id = env.ref("base.ca")
        user_admin_id.state_id = env["res.country.state"].search(
            [("code", "ilike", "QC")], limit=1
        )


def post_init_hook(cr, e):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})

        partner_id = env["res.partner"].browse(env.ref("base.main_company").id)

        partner_img_attachment = env.ref(
            "ore.ir_attachment_logo_ore_transparent_svg"
        )
        with tools.file_open(
            partner_img_attachment.local_url[1:], "rb"
        ) as desc_file:
            image_data = base64.b64encode(desc_file.read())
            partner_id.image = image_data
            # Update favicon web
            env["res.company"].browse(1).favicon = image_data

            # Update all data
            for item in env["ir.ui.menu"].search(
                [("name", "=", "Accorderie")]
            ):
                if item.web_icon:
                    item.web_icon = (
                        "ore,static/src/img/logo_ORE_background.png"
                    )
                item.name = "Réseau"
            for item in env["ir.actions.act_window"].search(
                [("name", "=", "Accorderie")]
            ):
                item.name = "Réseau"
            for item in env["accorderie.accorderie"].search(
                [("nom", "=", "Accorderie de Laval")]
            ):
                item.nom = "Municipalité de Sainte-Rose-Du-Nord"
            for item in env["accorderie.membre"].search(
                [("nom", "=", "Accorderie Laval")]
            ):
                item.nom = "Municipalité de Sainte-Rose-Du-Nord"

            for item in env["accorderie.type.service"].search([]):
                item.description = update_accorderie(item.description)
                item.nom = update_accorderie(item.nom)
            for item in env["accorderie.type.service.categorie"].search([]):
                item.nom = update_accorderie(item.nom)
            for item in env["accorderie.type.service.sous.categorie"].search(
                []
            ):
                item.nom = update_accorderie(item.nom)
            for item in env["accorderie.workflow.state"].search([]):
                if item.submit_response_description is not False:
                    item.submit_response_description = update_accorderie(
                        item.submit_response_description
                    )
            for item in env["accorderie.workflow.relation"].search([]):
                if item.body_html is not False:
                    item.body_html = update_accorderie(item.body_html)


def update_accorderie(txt):
    txt = txt.replace(
        "UnE AccordeurE (ou L'Accorderie) transfère des heures à unE autre"
        " AccordeurE",
        "Transfert d'heure",
    )
    txt = txt.replace("de L'Accorderie", "du réseau")
    txt = txt.replace("L'accordeur", "Le membre")
    txt = txt.replace("L'Accordeur", "Le membre")
    txt = txt.replace("d'Accorderie", "")  # Ignore
    txt = txt.replace("du Réseau Accorderie", "du Réseau")
    txt = txt.replace("pour le Réseau Accorderie", "pour le Réseau")
    txt = txt.replace("par le Réseau Accorderie", "par le Réseau")
    txt = txt.replace("Réseau Accorderie", "Réseau")
    txt = txt.replace("unE autre AccordeurE", "un autre membre")
    txt = txt.replace("par l'AccordeurE", "par le membre")
    txt = txt.replace("que l'AccordeurE", "que le membre")
    txt = txt.replace("AccordeurE inscritE", "Membre inscrit")
    txt = txt.replace("des Accordeurs", "des membres")
    txt = txt.replace("des AccordeurEs", "des membres")
    txt = txt.replace("d'une Accorderie", "d'un membre")
    txt = txt.replace("d'une nouvelle Accorderie", "d'un nouveau réseau")
    txt = txt.replace("à l'Accorderie", "au réseau")
    txt = txt.replace("l'Accorderie", "réseau")
    txt = txt.replace("aux AccordeurEs", "aux membres")
    txt = txt.replace("Accorderie", "réseau")
    txt = txt.replace("AccordeurEs", "membre")
    txt = txt.replace("accordeur", "membre")
    txt = txt.replace("AccOrdi", "ProjetOrdi")
    return txt
