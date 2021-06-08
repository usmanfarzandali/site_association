# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request


# class OpenAcademy(http.Controller):

    # @http.route(['/student_webform'], website=True, auth='public', type="http")
    # def student_webform(self):
    #     return http.request.render('openacademy.create_student', {})
    #
    # @http.route(['/create/webstudent'], type="http", auth="public", website=True)
    # def create_webstudent(self, **kw):
    #     print("jjjjjjjjj")
    #     request.env['openacademy_student'].sudo().create(kw)
    #     return request.render("openacademy.student_thanks", {})
