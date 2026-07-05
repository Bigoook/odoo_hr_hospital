from odoo import fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _description = 'Patient'

    name = fields.Char(string='Full Name', required=True)
    birth_date = fields.Date(string='Date of Birth')
    gender = fields.Selection(
        selection=[('male', 'Male'), ('female', 'Female'), ('other', 'Other')],
        string='Gender',
    )
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )
