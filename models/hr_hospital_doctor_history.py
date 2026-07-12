from odoo import api, fields, models


class HrHospitalDoctorHistory(models.Model):
    _name = 'hr.hospital.doctor.history'
    _description = 'Personal Doctor History'
    _order = 'assignment_date desc'

    patient_id = fields.Many2one(
        comodel_name='hr.hospital.patient',
        string='Patient',
        required=True,
        ondelete='cascade',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Doctor',
        required=True,
        ondelete='restrict',
    )
    assignment_date = fields.Date(
        string='Assignment Date',
        required=True,
        default=fields.Date.context_today,
    )
    change_date = fields.Date(string='Doctor Change Date')
    active = fields.Boolean(default=True)

    @api.onchange('assignment_date', 'change_date')
    def _onchange_check_dates(self):
        self.ensure_one()
        if self.assignment_date and self.change_date and self.change_date < self.assignment_date:
            return {
                'warning': {
                    'title': 'Error',
                    'message': "The doctor's change date cannot be earlier than the assignment date",
                }
            }
        return None

    def _compute_display_name(self):
        for record in self:
            patient_name = record.patient_id.name or ''
            doctor_name = record.doctor_id.name or ''
            category_name = record.doctor_id.category_id.name or ''
            assignment_date = record.assignment_date.strftime('%d.%m.%Y') if record.assignment_date else ''
            record.display_name = f'{patient_name} - {doctor_name} ({category_name}) {assignment_date}'.strip()
