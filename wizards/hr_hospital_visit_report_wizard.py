from odoo import _, api, fields, models


class HrHospitalVisitReportWizard(models.TransientModel):
    _name = 'hr.hospital.visit.report.wizard'
    _description = 'Patient Visits Report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    patient_ids = fields.Many2many(
        comodel_name='hr.hospital.patient',
        string='Patients',
    )
    date_from = fields.Date(string='Period Start')
    date_to = fields.Date(string='Period End')
    only_done = fields.Boolean(string='Only Completed Visits')
    disease_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Disease',
    )

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'hr.hospital.patient' and 'patient_ids' in fields_list:
            res['patient_ids'] = [fields.Command.set(active_ids)]
        elif active_model == 'hr.hospital.doctor' and 'doctor_ids' in fields_list:
            res['doctor_ids'] = [fields.Command.set(active_ids)]
        return res

    def action_generate_report(self):
        self.ensure_one()
        domain = []
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.patient_ids:
            domain.append(('patient_id', 'in', self.patient_ids.ids))
        if self.date_from:
            domain.append(('scheduled_date', '>=', self.date_from))
        if self.date_to:
            domain.append(('scheduled_date', '<=', self.date_to))
        if self.only_done:
            domain.append(('state', '=', 'done'))
        if self.disease_id:
            domain.append(('disease_id', '=', self.disease_id.id))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Visit Report'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
        }
