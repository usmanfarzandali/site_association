# -*- coding: utf-8 -*-

from datetime import datetime
from odoo import models, fields, api, _


class site_association(models.Model):
    # inherited the model name
    _inherit = "res.partner"

    avg_no_of_employees = fields.Char(string='Average Number Of Employees',
                                      tracking=True)

    date_of_establishment = fields.Date(string="Date Of Establishment Of Company", default=datetime.now())
