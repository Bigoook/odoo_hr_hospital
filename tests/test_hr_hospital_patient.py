from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHrHospitalPatient(TransactionCase):
    """Tests for the business methods of ``hr.hospital.patient``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doctor = cls.env['hr.hospital.doctor'].create({'name': 'Dr. House'})
        cls.patient = cls.env['hr.hospital.patient'].create(
            {
                'name': 'John Doe',
                'doctor_id': cls.doctor.id,
            }
        )
        cls.env['hr.hospital.visit'].create(
            {
                'patient_id': cls.patient.id,
                'doctor_id': cls.doctor.id,
            }
        )

    def test_action_create_quick_visit(self):
        """The quick-visit action pre-fills both the patient and their personal doctor."""
        action = self.patient.action_create_quick_visit()
        self.assertEqual(action['res_model'], 'hr.hospital.visit')
        self.assertEqual(action['context']['default_patient_id'], self.patient.id)
        self.assertEqual(action['context']['default_doctor_id'], self.doctor.id)

    def test_action_view_visit_history(self):
        """The visit-history action is scoped to this patient's visits only."""
        other_patient = self.env['hr.hospital.patient'].create({'name': 'Jane Roe'})
        self.env['hr.hospital.visit'].create(
            {
                'patient_id': other_patient.id,
                'doctor_id': self.doctor.id,
            }
        )

        action = self.patient.action_view_visit_history()
        visits = self.env['hr.hospital.visit'].search(action['domain'])
        self.assertTrue(visits)
        self.assertTrue(all(visit.patient_id == self.patient for visit in visits))
