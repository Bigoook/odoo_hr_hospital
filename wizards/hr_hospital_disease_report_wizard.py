from datetime import datetime, time

from odoo import _, api, fields, models
from odoo.tools import date_utils


class HrHospitalDiseaseReportWizard(models.TransientModel):
    _name = 'hr.hospital.disease.report.wizard'
    _description = 'Monthly Disease Report'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hospital.doctor',
        string='Doctors',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hospital.disease',
        string='Diseases',
    )
    date_from = fields.Date(string='Period Start', required=True)
    date_to = fields.Date(string='Period End', required=True)

    @api.model
    def default_get(self, fields_list):
        res = super().default_get(fields_list)
        active_model = self.env.context.get('active_model')
        active_ids = self.env.context.get('active_ids', [])
        if active_model == 'hr.hospital.doctor' and 'doctor_ids' in fields_list:
            res['doctor_ids'] = [fields.Command.set(active_ids)]

        month_start, month_end = date_utils.get_month(fields.Date.context_today(self))
        if 'date_from' in fields_list:
            res.setdefault('date_from', month_start)
        if 'date_to' in fields_list:
            res.setdefault('date_to', month_end)
        return res

    def action_generate_report(self):
        self.ensure_one()
        date_from = datetime.combine(self.date_from, time.min)
        date_to = datetime.combine(self.date_to, time.max)

        domain = [
            ('scheduled_date', '>=', date_from),
            ('scheduled_date', '<=', date_to),
        ]
        if self.doctor_ids:
            domain.append(('doctor_id', 'in', self.doctor_ids.ids))
        if self.disease_ids:
            domain.append(('disease_id', 'in', self.disease_ids.ids))
        return {
            'type': 'ir.actions.act_window',
            'name': _('Disease Report'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'list,form',
            'domain': domain,
            'context': {'group_by': ['disease_id']},
        }
