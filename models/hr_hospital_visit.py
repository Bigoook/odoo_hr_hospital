from odoo import fields, models
from odoo.exceptions import UserError


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'scheduled_date desc'

    _PROTECTED_FIELDS = ('scheduled_date', 'actual_date', 'doctor_id')

    actual_date = fields.Datetime(string='Actual Visit Date')
    epicrisis = fields.Html(string='Epicrisis / Summary')
    notes = fields.Text(string='Notes')
    state = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='scheduled',
    )
    active = fields.Boolean(string='Active', default=True)

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Diagnosis',
    )
    scheduled_date = fields.Datetime(
        string='Scheduled Date',
        default=fields.Datetime.now,
        required=True,
    )

    def write(self, vals):
        touches_protected = any(field_name in vals for field_name in self._PROTECTED_FIELDS)
        archiving = vals.get('active') is False
        if touches_protected or archiving:
            for visit in self:
                if visit.state == 'done':
                    if touches_protected:
                        raise UserError('Не можна змінювати дату, час або лікаря візиту, що вже відбувся.')
                    if archiving:
                        raise UserError('Не можна архівувати візит, що вже відбувся.')
        return super().write(vals)

    def unlink(self):
        for visit in self:
            if visit.state == 'done':
                raise UserError('Не можна видаляти візит, що вже відбувся.')
        return super().unlink()
