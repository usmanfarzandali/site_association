# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


class SiteAssociation(http.Controller):
    @http.route('/member_webform', type='http', auth='public', website=True)
    def member_webform(self, **post):
        countries = request.env['res.country'].sudo().search([])
        states = request.env['res.country.state'].sudo().search([])
        titles = request.env['res.partner.title'].sudo().search([])
        values = {
            'countries': countries,
            'states': states,
            'titles': titles,
        }
        return request.render('site_association.create_member', values)

    @http.route(['/create/webmember'], type="http", auth="public", website=True)
    def create_webstudent(self, **post):
        vals = {
            'name': post.get('name', ''),
            'type': post.get('type', ''),
            'country_id': int(post.get('country_id', False)),
            'state_id': int(post.get('state_id', False)) if post.get('state_id') else None,
            'street': post.get('street', ''),
            'street2': post.get('street2', ''),
            'zip': post.get('zip', ''),
            'vat': post.get('vat', ''),
            'avg_no_of_employees': post.get('avg_no_of_employees', ''),
            'function': post.get('function', ''),
            'phone': post.get('phone', ''),
            'mobile': post.get('mobile', ''),
            'email': post.get('email', ''),
            'website': post.get('website', ''),
            'title': post.get('title', ''),
        }
        # return request.render("site_association.member_thanks", vals)
        child3_id = request.env['res.partner'].sudo().create(vals)
        return request.render("site_association.member_thanks")
