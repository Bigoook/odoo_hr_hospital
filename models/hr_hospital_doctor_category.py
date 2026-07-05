from odoo import fields, models
from odoo.models import Constraint


class HrHospitalDoctorCategory(models.Model):
    _name = 'hr.hospital.doctor.category'
    _description = 'Doctor Category'
    _order = 'sequence, name'

    name = fields.Char(string='Name', required=True)
    sequence = fields.Integer(string='Sequence', default=10)
    doctor_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='category_id',
        string='Doctors',
    )

    _name_unique = Constraint(
        'UNIQUE(name)',
        'Doctor category name must be unique.',
    )
