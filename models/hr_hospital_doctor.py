from odoo import api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialty = fields.Char(string='Specialty')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    is_intern = fields.Boolean(
        string='Is Intern',
        compute='_compute_is_intern',
        store=True,
    )
    category_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.category',
        string='Category',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor',
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        intern_category = self.env.ref('hr_hospital.doctor_category_intern', raise_if_not_found=False)
        for doctor in self:
            doctor.is_intern = bool(intern_category and doctor.category_id == intern_category)

    @api.constrains('mentor_id')
    def _check_mentor_is_not_intern(self):
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError('Ментором не може бути лікар, який є інтерном.')
