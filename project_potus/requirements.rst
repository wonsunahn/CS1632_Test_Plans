Requirements
============

This is the requirements specification.  It is organized in 3 levels:
proj->req->spec.  The ``.. proj::`` block describes the project.  The ``..
req::`` block is a requirement linked to a project that describes a user need
in a language intended for users.  The ``.. spec::`` block is a specification
linked to a requirement that details verifiable system behavior for each
equivalence class of the requirement in a language intended for developers and
testers.

.. proj:: Can I be POTUS?
   :id: PROJ_001

   This system allows a user to determine whether he/she/they can be the President Of The United States.

.. req:: Command line argument passing
   :id: REQ_001
   :requiredby: PROJ_001

   The system shall accept one numerical command line argument as the user's age.

.. req:: POTUS eligibility determination
   :id: REQ_002
   :requiredby: PROJ_001

   The system shall display whether the user can be POTUS based on the user's age.

.. spec:: Passing in one integer argument
   :id: SPEC_001
   :specifies: REQ_001

   The system shall determine POTUS eligibility treating the integer argument as the user's age.

.. spec:: Passing in no arguments
   :id: SPEC_002
   :specifies: REQ_001

   The system shall inform the user that a command line argument is needed.

.. spec:: Passing in more than one argument
   :id: SPEC_003
   :specifies: REQ_001

   The system shall inform the user that there needs to be exactly one command line argument.

.. spec:: Passing in one non-integer argument
   :id: SPEC_004
   :specifies: REQ_001

   The system shall inform the user that the command line argument needs to be an integer.

.. spec:: Can be POTUS
   :id: SPEC_005
   :specifies: REQ_002

   If user's age is 35 or more, then the system shall print "[AGE] is old enough to be POTUS" replacing [AGE] with the user's age.

.. spec:: Cannot be POTUS
   :id: SPEC_006
   :specifies: REQ_002

   If user's age is 34 or less, then the system shall print "[AGE] is too young to be POTUS" replacing [AGE] with the user's age.

