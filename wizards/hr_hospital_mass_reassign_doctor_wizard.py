from odoo import fields, models


class HrHospitalMassReassignDoctorWizard(models.TransientModel):
    _name = 'hr.hospital.mass.reassign.doctor.wizard'
    _description = 'Mass Reassign Personal Doctor'

    new_doctor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='New Doctor',
        required=True,
    )
    change_date = fields.Date(
        string='Change Date',
        default=fields.Date.context_today,
        required=True,
    )

    def action_reassign(self):
        self.ensure_one()
        patient_ids = self.env.context.get('active_ids', [])
        patients = self.env['hr.hospital.patient'].browse(patient_ids)
        history_model = self.env['hr.hospital.doctor.history']

        current_history = history_model.search(
            [
                ('patient_id', 'in', patients.ids),
                ('active', '=', True),
            ]
        )
        current_history.write(
            {
                'change_date': self.change_date,
                'active': False,
            }
        )
        # додамо в історію
        history_model.create(
            [
                {
                    'patient_id': patient.id,
                    'doctor_id': self.new_doctor_id.id,
                    'assignment_date': self.change_date,
                }
                for patient in patients
            ]
        )

        patients.write({'doctor_id': self.new_doctor_id.id})
        return {'type': 'ir.actions.act_window_close'}
