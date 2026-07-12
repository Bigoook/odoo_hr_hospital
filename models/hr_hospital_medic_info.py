from dateutil.relativedelta import relativedelta

from odoo import api, fields, models


class HrHospitalMedicInfo(models.AbstractModel):
    _name = 'hr.hospital.medic.info'
    _description = 'Medical Information'

    blood_type = fields.Selection(
        selection=[
            ('o_pos', 'O(I) Rh+'),
            ('o_neg', 'O(I) Rh-'),
            ('a_pos', 'A(II) Rh+'),
            ('a_neg', 'A(II) Rh-'),
            ('b_pos', 'B(III) Rh+'),
            ('b_neg', 'B(III) Rh-'),
            ('ab_pos', 'AB(IV) Rh+'),
            ('ab_neg', 'AB(IV) Rh-'),
        ],
        string='Blood Type',
    )
    gender = fields.Selection(
        selection=[
            ('male', 'Male'),
            ('female', 'Female'),
        ],
    )
    birth_date = fields.Date(string='Date of Birth')
    age = fields.Integer(
        compute='_compute_age',
    )

    @api.depends('birth_date')
    def _compute_age(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.birth_date:
                record.age = relativedelta(today, record.birth_date).years
            else:
                record.age = 0
