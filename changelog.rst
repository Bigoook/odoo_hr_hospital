Changelog
=========

19.0.2.0.0
----------

* Added a role-based security hierarchy with five inheriting groups:
  Patient, Intern, Doctor, Manager, and Administrator.
* Patients can now be linked to a system user (``user_id`` on
  ``hr.hospital.patient``) so that record rules can restrict them to
  their own visits.
* Added record rules so that:

  - Patients only view their own visits.
  - Interns view and edit only their own visits.
  - Doctors view and edit their own visits and their interns' visits.
  - Managers view all visits (read-only).
  - Administrators can delete any record in the module.

* Made the disease name/description and the doctor category name
  translatable, and added a Ukrainian translation for the module and
  for the disease classifier (``i18n/uk.po``).
* Added a module description page (``static/description/index.html``).
* Added unit tests covering the doctor, patient, and visit business
  methods.
* Documented ``README.rst``.

19.0.1.1.0
----------

* Initial version: patients, doctors, doctor categories, diseases
  classifier, doctor-assignment history, visits, doctor profile report,
  and reporting/reassignment wizards.
