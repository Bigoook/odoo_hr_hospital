from odoo import _, fields, models


class HrHospitalPatient(models.Model):
    _name = 'hr.hospital.patient'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Patient'

    name = fields.Char(string='Full Name', required=True)
    phone = fields.Char()
    email = fields.Char()
    insurance_number = fields.Char(string='Insurance Policy Number', size=20)
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
        help='Portal user linked to this patient, used to restrict the patient to viewing only their own visits.',
    )
    doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Personal Doctor',
    )
    history_ids = fields.One2many(
        comodel_name='hr.hospital.doctor.history',
        inverse_name='patient_id',
        string='Doctor History',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='patient_id',
        string='Visits',
    )

    def action_view_visit_history(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('Visit History'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form,calendar',
            'domain': [('patient_id', '=', self.id)],
            'context': {'default_patient_id': self.id},
        }

    def action_create_quick_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Visit'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }
