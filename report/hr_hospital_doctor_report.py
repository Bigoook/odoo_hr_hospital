from odoo import fields, models


class ReportHrHospitalDoctor(models.AbstractModel):
    _name = 'report.hr_hospital.report_hr_hospital_doctor'
    _description = 'Doctor Profile Report'

    def _get_report_values(self, docids, data=None):
        docs = self.env['hr.hospital.doctor'].browse(docids)
        print_datetime = fields.Datetime.context_timestamp(self, fields.Datetime.now())
        return {
            'doc_ids': docids,
            'doc_model': 'hr.hospital.doctor',
            'docs': docs,
            'print_datetime': print_datetime.strftime('%d.%m.%Y %H:%M'),
        }
