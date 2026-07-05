from odoo import api, fields, models
from odoo.exceptions import ValidationError
from odoo.models import Constraint


class HrHospitalDisease(models.Model):
    _name = 'hr.hospital.disease'
    _description = 'Disease'
    _parent_name = 'parent_id'
    _parent_store = True
    _order = 'parent_path'

    name = fields.Char(string='Disease Name', required=True)
    description = fields.Text(string='Description')
    parent_id = fields.Many2one(
        comodel_name='hr.hospital.disease',
        string='Parent Disease',
        index=True,
        ondelete='restrict',
    )
    child_ids = fields.One2many(
        comodel_name='hr.hospital.disease',
        inverse_name='parent_id',
        string='Child Diseases',
    )
    parent_path = fields.Char(index=True)

    _name_unique = Constraint(
        'UNIQUE(name)',
        'Disease name must be unique.',
    )

    @api.constrains('parent_id')
    def _check_parent_recursion(self):
        if self._has_cycle():
            raise ValidationError('Помилка! Не можна створювати циклічну ієрархію хвороб.')

    def _compute_display_name(self):
        for disease in self:
            names = []
            current = disease
            visited = set()
            while current and current.id not in visited:
                names.insert(0, current.name)
                visited.add(current.id)
                current = current.parent_id
            disease.display_name = ' / '.join(names)
