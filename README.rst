===========
HR Hospital
===========

.. |badge1| image:: https://img.shields.io/badge/licence-LGPL--3-blue.svg
    :target: https://www.gnu.org/licenses/lgpl-3.0-standalone.html
    :alt: License: LGPL-3

|badge1|

A hospital management module for Odoo 19: patients, doctors (including
interns and their mentors), diseases classifier, personal-doctor history,
visits, and reporting.

Features
========

* Patient, doctor, and disease classifier records, with a hierarchical
  (tree) classifier for diseases.
* Doctor categories (intern / specialist / top category) with automatic
  detection of intern doctors and mentor assignment.
* Visit scheduling and tracking, with protection against editing or
  deleting a visit once it is marked as done.
* Personal-doctor history per patient, with a wizard to mass-reassign the
  personal doctor of several patients at once.
* Doctor profile PDF/HTML report, and wizards to generate filtered visit
  and monthly disease reports.
* Role-based access control with five inheriting user groups: Patient,
  Intern, Doctor, Manager, and Administrator (see *Security* below).
* Ukrainian translation of the module and of the disease classifier.

Security
========

The module defines five groups. Each group implies (and therefore
automatically includes) the previous one:

Patient -> Intern -> Doctor -> Manager -> Administrator

* **Patient** -- can only view their own visits (and their own patient
  card / doctor-assignment history).
* **Intern** -- can view and edit only the visits where they are the
  assigned doctor.
* **Doctor** -- can view and edit their own visits, as well as the
  visits of the interns they mentor.
* **Manager** -- can view every visit in the system (read-only).
* **Administrator** -- can delete any record in the module, in addition
  to the rights inherited from Manager.

Installation
============

To install this module, you need to:

#. Clone the repository.
#. Add the repository path to the Odoo configuration file.
#. Update the apps list (``Apps > Update Apps List``, or
   ``odoo-helper addons update-list`` from the terminal).
#. Install the *HR Hospital* module from the Apps list.

Configuration
=============

After installation, assign the appropriate security group (Patient,
Intern, Doctor, Manager, or Administrator) to each user under
*Settings > Users & Companies > Users*.

For patients to be able to log in and see only their own visits, link
their portal user account to their patient card via the *System User*
field on the patient form (visible to Managers and Administrators).

Usage
=====

* *Hospital > Patients* / *Doctors* / *Visits* to manage the core records.
* *Hospital > Reporting > Visits Pivot* for a pivot view of visits for
  the current year.
* *Hospital > Configuration* to manage diseases and doctor categories.
* Use the *Generate Report* wizards from the Doctor or Patient list/form
  views to produce filtered visit or monthly disease reports.
* Use *Mass Reassign Personal Doctor* from the Patients list to change
  the personal doctor of several patients at once.

Bug Tracker
===========

Bugs are tracked on the repository's issue tracker. In case of trouble,
please check there if your issue has already been reported.

Credits
=======

Authors
-------

* big_ooo

Maintainers
-----------

This module is maintained by the module's author.
