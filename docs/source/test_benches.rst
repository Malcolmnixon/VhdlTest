.. test_benches:

Test Benches
============

There are numerous techniques VHDL test-benches can use to relay results:
- Writing result files *(ignored by VHDLTest)*
- Report statements
- Assert statements

Report and Assert statements can have different severities, and cause different behavior in VHDLTest:

+------------+----------+------------+-------------------------+
|Severity    |Display   |Test Status |Additional               |
+============+==========+============+=========================+
|Note        |Bold      |Pass        |                         |
+------------+----------+------------+-------------------------+
|Warning     |Yellow    |Pass        |Displays all test output |
+------------+----------+------------+-------------------------+
|Error       |Red       |Fail        |Displays all test output |
+------------+----------+------------+-------------------------+
|Failure     |Red       |Fail        |Displays all test output |
+------------+----------+------------+-------------------------+

Example Configuration
---------------------

The 'examples' folder on the `Github <https://github.com/Malcolmnixon/VhdlTest/>`_ repository demonstrates writing
simple test benches which use Note Reports to show test progress and Error Asserts to capture failures.
    