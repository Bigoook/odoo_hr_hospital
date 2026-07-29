from odoo.exceptions import UserError
from odoo.tests import TransactionCase, tagged


@tagged('post_install', '-at_install')
class TestHrHospitalVisit(TransactionCase):
    """Tests for the business methods of ``hr.hospital.visit``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.doctor = cls.env['hr.hospital.doctor'].create({'name': 'Dr. House'})
        cls.patient = cls.env['hr.hospital.patient'].create({'name': 'John Doe'})
        cls.disease = cls.env.ref('hr_hospital.disease_flu')
        cls.visit = cls.env['hr.hospital.visit'].create(
            {
                'patient_id': cls.patient.id,
                'doctor_id': cls.doctor.id,
                'disease_id': cls.disease.id,
            }
        )

    def test_compute_same_disease_visit_count(self):
        """The same-diagnosis counter includes every visit sharing the diagnosis."""
        self.assertEqual(self.visit.same_disease_visit_count, 1)

        self.env['hr.hospital.visit'].create(
            {
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
                'disease_id': self.disease.id,
            }
        )
        self.visit.invalidate_recordset(['same_disease_visit_count'])
        self.assertEqual(self.visit.same_disease_visit_count, 2)

    def test_write_protected_fields_once_done(self):
        """A done visit can no longer be rescheduled, reassigned, or archived."""
        self.visit.state = 'done'

        with self.assertRaises(UserError):
            self.visit.doctor_id = self.env['hr.hospital.doctor'].create({'name': 'Dr. Wilson'})

        with self.assertRaises(UserError):
            self.visit.active = False

        # Fields that are not protected can still be edited.
        self.visit.notes = 'Follow-up in two weeks.'
        self.assertEqual(self.visit.notes, 'Follow-up in two weeks.')

    def test_unlink_done_visit_forbidden(self):
        """A done visit cannot be deleted, but a scheduled one can."""
        self.visit.state = 'done'
        with self.assertRaises(UserError):
            self.visit.unlink()

        scheduled_visit = self.env['hr.hospital.visit'].create(
            {
                'patient_id': self.patient.id,
                'doctor_id': self.doctor.id,
            }
        )
        scheduled_visit.unlink()
        self.assertFalse(scheduled_visit.exists())
