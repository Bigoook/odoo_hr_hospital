from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HrHospitalDoctor(models.Model):
    _name = 'hr.hospital.doctor'
    _inherit = ['hr.hospital.medic.info']
    _description = 'Doctor'

    name = fields.Char(string='Full Name', required=True)
    specialty = fields.Char()
    phone = fields.Char()
    email = fields.Char()
    is_intern = fields.Boolean(
        compute='_compute_is_intern',
        store=True,
    )
    category_id = fields.Many2one(
        comodel_name='hr.hospital.doctor.category',
        string='Category',
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='System User',
    )
    mentor_id = fields.Many2one(
        comodel_name='hr.hospital.doctor',
        string='Mentor',
    )
    patient_ids = fields.One2many(
        comodel_name='hr.hospital.patient',
        inverse_name='doctor_id',
        string='Patients',
    )
    visit_ids = fields.One2many(
        comodel_name='hr.hospital.visit',
        inverse_name='doctor_id',
        string='Visits',
    )
    intern_ids = fields.One2many(
        comodel_name='hr.hospital.doctor',
        inverse_name='mentor_id',
        string='Interns',
    )

    @api.depends('category_id')
    def _compute_is_intern(self):
        """Flag the doctor as an intern when their category is the reference intern category."""
        intern_category = self.env.ref('hr_hospital.doctor_category_intern', raise_if_not_found=False)
        for doctor in self:
            doctor.is_intern = bool(intern_category and doctor.category_id == intern_category)

    @api.constrains('mentor_id')
    def _check_mentor_is_not_intern(self):
        """Ensure an intern is never assigned as a mentor for another doctor."""
        for doctor in self:
            if doctor.mentor_id and doctor.mentor_id.is_intern:
                raise ValidationError(_('A mentor cannot be a doctor who is an intern.'))

    def action_create_quick_visit(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': _('New Visit'),
            'res_model': 'hr.hospital.visit',
            'view_mode': 'form',
            'target': 'new',
            'context': {
                'default_doctor_id': self.id,
            },
        }
