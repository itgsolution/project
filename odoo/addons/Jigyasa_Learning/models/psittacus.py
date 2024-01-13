# -*- coding: utf-8 -*-
# Part of Odoo. Created and Developed by Jigyasa Learning.

import base64
import collections
import datetime
import hashlib
import pytz
import threading
import re
from datetime import date
from dateutil.relativedelta import relativedelta
import requests
from lxml import etree
from werkzeug import urls
import time
from odoo import api, fields, models, tools, SUPERUSER_ID, _
from odoo.modules import get_module_resource
from odoo.osv.expression import get_unaccent_wrapper
from odoo.exceptions import UserError, ValidationError

class psittacus(models.Model):
    _description = 'Student Contact'
    _inherit = "res.partner"

    company_type = fields.Selection(selection_add=[('school', 'School')])
    is_school = fields.Boolean(string='Is a School', default=False)
    birth_date = fields.Date(string='Birth Date',default=time.strftime(''))
    school_name = fields.Char(string='school name',)
    school_coordinator = fields.Many2one('res.partner', string= 'Coordinator Name', domain= [('reg_type', '=', 'guardian')])
    age = fields.Char(string='Age', store=True, compute='_cal_age', required=False)
    gender = fields.Selection(
        string='Gender',
        selection=[('male', 'male'), ('female', 'female'), (' ',' ')], default = ' ')
    
    reg_type = fields.Selection(string='Registration Type', selection=[('student', 'Student'), ('guardian', 'Guardian'), ('principal','Principal'), (' ',' ')], default = ' ')
    religion = fields.Selection(string='Religion', selection=[('Hindism', 'Hindism'), ('Islam', 'Islam'), ('Christianity', 'Christianity'), ('Sikhism', 'Sikhism'), ('Jews','Jews'), ('Buddhism', 'Buddhism'), ('Jainism', 'Jainism'), ('Others', 'Others'), (' ', ' ')], default = ' ')
    nationality = fields.Many2one('res.country', string='Nationality', ondelete='restrict')
    @api.depends('is_company')
    def _compute_company_type(self):
        for partner in self:
            if partner.is_school == True:
                partner.company_type = 'school'
            else:
                partner.company_type = 'company' if partner.is_company else 'person'

    def _write_company_type(self):
        for partner in self:
            if partner.company_type == 'school':
                self.is_school = True
                self.is_company = True
            else:
                partner.is_company = partner.company_type == 'company'

    @api.onchange('company_type')
    def onchange_company_type(self):
        for partner in self:
            if self.company_type == 'school':
                self.is_school = True
                self.is_company = True
            else: 
                self.is_company = (self.company_type == 'company')
    

    @api.onchange('birth_date')
    @api.depends('birth_date')
    def _cal_age(self):
        today = date.today()
        for record in self:
            age = []
            dob = fields.Date.from_string(record.birth_date)
            gap = relativedelta(today, dob)
            if gap.years > 0:
                record.age = str(gap.years) + ' Years'
            else:
                pass
                #raise UserError(_('Warning!'),_('Birth Date must be Low than the Current Date'))
    
