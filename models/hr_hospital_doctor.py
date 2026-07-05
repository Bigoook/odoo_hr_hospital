from odoo import fields, models


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _description = 'Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialty = fields.Char(string='Specialty')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
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
