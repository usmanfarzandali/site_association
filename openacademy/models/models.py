#  -*- coding: utf-8 -*-

from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


# class for inheriting student name in sales order form
class SaleOrderInherit(models.Model):
    # inherited the model name
    _inherit = "sale.order"

    student_name = fields.Char(string='Student Name')


# class for student
class OpenAcademyStudent(models.Model):
    _name = "openacademy_student"
    _description = "openacademy_student"
    _rec_name = "student_name"

    # inherit field for chatter box
    _inherit = ['mail.thread', 'mail.activity.mixin']

    student_name = fields.Char(string='Name', required=True)
    # for tracking of fields, add tracking attribute
    student_age = fields.Integer('Age', tracking=True)
    notes = fields.Text(string='Notes')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male')
    student_email = fields.Char(string='Email', tracking=True)
    name_seq = fields.Char(string='Student ID', required=True, copy=False, readonly=True, default=_('New'))
    image = fields.Binary(attachment="True")
    student_stages = fields.Selection([
        ('registered', 'Registered'),
        ('undergraduate', 'Undergraduate'),
        ('graduate', 'Graduate'),
        ('masters', 'Masters'),
        ('phd', 'PHD'),
    ], string='Status', default='registered')

    # get count of teachers on smart buttons
    teacher_count = fields.Integer(string='Teachers', compute='get_teacher_count')

    # age group for compute purpose. Based on age, we will set the age group. For that
    # we will define compute field and give the function name in it.
    age_group = fields.Selection([
        ('major', 'Major'),
        ('minor', 'Minor'),
    ], string='Age Group', compute='set_age_group')

    # relation between teachers and students
    teacher_ids = fields.Many2many("openacademy_teacher", string="Teachers Assigned")

    # relation between courses and students
    course_ids = fields.Many2many("openacademy.course", string="Courses Assigned")

    # def for overriding create method and generating sequence
    @api.model
    def create(self, vals):
        if vals.get('name_seq', ('New')) == ('New'):
            vals['name_seq'] = self.env['ir.sequence'].next_by_code('openacademy_student.sequence') or _('New Create')
            result = super(OpenAcademyStudent, self).create(vals)
            return result

    # function for changing the state of students

    def action_registered(self):
        self.student_stages = 'registered'

    def action_undergraduate(self):
        self.student_stages = 'undergraduate'

    def action_graduate(self):
        self.student_stages = 'graduate'

    def action_masters(self):
        self.student_stages = 'masters'

    # function for sending student card by email
    def action_sendbyemail(self):
        # template_id = self.env.ref('openacademy.student_card_email_template').id
        # template = self.env['mail.template'].browse(template_id)
        # template.send_mail(self.id, force_send=True)
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('openacademy', 'student_card_email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'openacademy_student',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'views_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    # function for computing age group based on age
    @api.depends('student_age')
    def set_age_group(self):
        for rec in self:
            if rec.student_age < 18:
                rec.age_group = 'minor'
            else:
                rec.age_group = 'major'

    # function for adding constrains to the field age.
    # for that we will import odoo.exceptions validationerror
    @api.constrains('student_age')
    def check_age(self):
        for rec in self:
            if rec.student_age < 5:
                raise ValidationError(_('The Age must be greater than 5'))

    # def for smart button action
    def open_student_teachers(self):
        return {
            'name': _('Teachers'),
            'type': 'ir.actions.act_window',
            'res_model': 'openacademy_teacher',
            'view_mode': 'tree,form',
            'domain': [('student_ids', '=', self.student_name)],
        }

    # def for getting teacher count on smart buttons
    def get_teacher_count(self):
        count = self.env['openacademy_teacher'].search_count([('student_ids', '=', self.student_name)])
        self.teacher_count = count


# class for teacher
class OpenAcademyTeacher(models.Model):
    _name = "openacademy_teacher"
    _description = "openacademy_teacher"
    _rec_name = "teacher_name"

    # inherit field for chatter box
    _inherit = ['mail.thread', 'mail.activity.mixin']

    teacher_image = fields.Binary()
    teacher_name = fields.Char(string='Name', required=True, tracking=True)
    teacher_age = fields.Integer(string='Age')
    teacher_seq = fields.Char(string='Teacher ID', required=True, copy=False, readonly=True, default=_('New'))
    teacher_gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other'),
    ], required=True, default='male')
    teacher_email = fields.Char(string='Email')
    teacher_qualification = fields.Char(string='Qualification')
    teacher_dob = fields.Date(string='Date Of Birth')

    # fields for pages and notebook
    teacher_note = fields.Text(string='Note')
    teacher_description = fields.Text(string='Description')

    # relation between students and teachers
    student_ids = fields.Many2many("openacademy_student", string="Students Assigned")

    # relation between courses and teachers
    course_ids = fields.Many2many("openacademy.course", string="Courses Assigned")

    # get count of teachers on smart buttons
    course_count = fields.Integer(string='Courses', compute='get_course_count')

    # function for sending teacher card
    def action_sendbyemail(self):
        self.ensure_one()
        ir_model_data = self.env['ir.model.data']
        try:
            template_id = ir_model_data.get_object_reference('openacademy', 'teacher_card_email_template')[1]
        except ValueError:
            template_id = False
        try:
            compose_form_id = ir_model_data.get_object_reference('mail', 'email_compose_message_wizard_form')[1]
        except ValueError:
            compose_form_id = False
        ctx = {
            'default_model': 'openacademy_teacher',
            'default_res_id': self.ids[0],
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
            'force_email': True
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'mail.compose.message',
            'views': [(compose_form_id, 'form')],
            'views_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }

    # def for overriding create method and generating sequence
    @api.model
    def create(self, vals):
        if vals.get('teacher_seq', ('New')) == ('New'):
            vals['teacher_seq'] = self.env['ir.sequence'].next_by_code('openacademy_teacher.sequence') or _(
                'New Create')
            result = super(OpenAcademyTeacher, self).create(vals)
            return result

    # def for smart button action
    def open_teacher_courses(self):
        return {
            'name': _('Courses'),
            'type': 'ir.actions.act_window',
            'res_model': 'openacademy.course',
            'view_mode': 'tree,form',
            'domain': [('course_id', '=', self.teacher_name)],
        }

    # def for getting course count on smart buttons
    def get_course_count(self):
        count = self.env['openacademy.course'].search_count([('course_id', '=', self.teacher_name)])
        self.course_count = count

    # compute teacher age based on date of birth
    @api.onchange('teacher_dob')
    def get_teacher_age(self):
        for rec in self:
            if rec.teacher_dob:
                dt = rec.teacher_dob
                dt = str(dt)
                d1 = datetime.strptime(dt, "%Y-%m-%d").date()
                d2 = date.today()
                rd = relativedelta(d2, d1)
                rec.teacher_age = rd.years


# class for course
class OpenAcademyCourse(models.Model):
    _name = "openacademy.course"
    _description = "openacademy.course"
    _rec_name = "course_name"

    # inherit field for chatter box
    _inherit = ['mail.thread', 'mail.activity.mixin']

    course_name = fields.Char(string='Course Name', required=True)
    course_timings = fields.Float(string='Course Timing')
    course_description = fields.Text(string='Course Description')

    # get count of teachers on smart buttons
    teacher_count = fields.Integer(string='Teachers', compute='get_teacher_count')

    # relation between courses and teachers
    course_id = fields.Many2many("openacademy_teacher", string="Teachers Assigned")

    # def for smart button action
    def open_course_teachers(self):
        return {
            'name': _('Teachers'),
            'type': 'ir.actions.act_window',
            'res_model': 'openacademy_teacher',
            'view_mode': 'tree,form',
            'domain': [('course_ids', '=', self.course_name)],
        }

    # def for getting teacher count on smart buttons
    def get_teacher_count(self):
        count = self.env['openacademy_teacher'].search_count([('course_ids', '=', self.course_name)])
        self.teacher_count = count
