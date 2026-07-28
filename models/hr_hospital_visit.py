from odoo import api, fields, models
from odoo.exceptions import UserError


class HrHospitalVisit(models.Model):
    _name = 'hr.hospital.visit'
    _description = 'Patient Visit'
    _order = 'scheduled_date desc'

    _PROTECTED_FIELDS = ('scheduled_date', 'actual_date', 'doctor_id')

    actual_date = fields.Datetime(string='Actual Visit Date')
    epicrisis = fields.Html(string='Epicrisis / Summary')
    notes = fields.Text()
    state = fields.Selection(
        selection=[
            ('scheduled', 'Scheduled'),
            ('done', 'Done'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='scheduled',
    )
    active = fields.Boolean(default=True)
    same_disease_visit_count = fields.Integer(
        string='Visits with the Same Diagnosis',
        compute='_compute_same_disease_visit_count',
    )

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

    @api.depends('disease_id')
    def _compute_same_disease_visit_count(self):
        for visit in self:
            if visit.disease_id:
                visit.same_disease_visit_count = self.search_count([('disease_id', '=', visit.disease_id.id)])
            else:
                visit.same_disease_visit_count = 0

    def action_view_same_disease_visits(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visits with the Same Diagnosis',
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': [('disease_id', '=', self.disease_id.id)],
        }

    def write(self, vals):
        touches_protected = any(field_name in vals for field_name in self._PROTECTED_FIELDS)
        archiving = vals.get('active') is False
        if touches_protected or archiving:
            for visit in self:
                if visit.state == 'done':
                    if touches_protected:
                        raise UserError(
                            'You cannot change the date, time, or doctor of a visit that has already taken place.'
                        )
                    if archiving:
                        raise UserError('You cannot archive a visit that has already taken place.')
        return super().write(vals)

    def unlink(self):
        for visit in self:
            if visit.state == 'done':
                raise UserError('You cannot delete a visit that has already taken place.')
        return super().unlink()
