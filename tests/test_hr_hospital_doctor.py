from odoo.exceptions import ValidationError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHrHospitalDoctor(TransactionCase):
    """Tests for the business methods of ``hr.hospital.doctor``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.category_intern = cls.env.ref('hr_hospital.doctor_category_intern')
        cls.category_specialist = cls.env.ref('hr_hospital.doctor_category_specialist')
        cls.mentor = cls.env['hr.hospital.doctor'].create(
            {
                'name': 'Dr. Mentor',
                'category_id': cls.category_specialist.id,
            }
        )
        cls.intern = cls.env['hr.hospital.doctor'].create(
            {
                'name': 'Dr. Intern',
                'category_id': cls.category_intern.id,
                'mentor_id': cls.mentor.id,
            }
        )

    def test_compute_is_intern(self):
        """A doctor with the intern category is flagged as an intern, others are not."""
        self.assertTrue(self.intern.is_intern)
        self.assertFalse(self.mentor.is_intern)

        self.intern.category_id = self.category_specialist
        self.assertFalse(self.intern.is_intern)

    def test_check_mentor_is_not_intern(self):
        """An intern cannot be set as someone else's mentor."""
        with self.assertRaises(ValidationError):
            self.mentor.mentor_id = self.intern

    def test_action_create_quick_visit(self):
        """The quick-visit action returns a window action pre-filled with this doctor."""
        action = self.mentor.action_create_quick_visit()
        self.assertEqual(action['res_model'], 'hr.hospital.visit')
        self.assertEqual(action['context']['default_doctor_id'], self.mentor.id)
