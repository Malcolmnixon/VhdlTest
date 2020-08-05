.. running:

Running
=======

The simplest way to run VHDLTest is:

.. code-block:: console

   > python -m VHDLTest --config <your-config.yaml>
   
Command Line Arguments
----------------------

.. code-block:: console

   > python -m VHDLTest [options]
   
Options
~~~~~~~

.. option:: -c --config your-config.yaml

   Specify the YAML configuration file.

.. option:: -l --log your-log-file

   Specify a log file to create.

.. option:: -j --junit your-junit.xml

   Specify a JUnit report file to create.

.. option:: -v --verbose

   Produce verbose output from simulator.

.. option:: --exit-0

   Exit with code 0 even if tests fail. A non-zero error code will still be
   generated for compile or simulation errors.

.. option:: --version

   Print the version information.
