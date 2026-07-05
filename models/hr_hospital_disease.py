from odoo import fields, models
from odoo.models import Constraint


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'

    name = fields.Char(string='Disease Name', required=True)
    description = fields.Text(string='Description')

    _name_unique = Constraint(
        'UNIQUE(name)',
        'Disease name must be unique.',
    )
