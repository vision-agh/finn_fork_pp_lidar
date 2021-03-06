.. _getting_started:

***************
Getting Started
***************

.. note:: **This website is currently under construction.**

How to use the FINN compiler
============================
The FINN compiler should not be thought of a single pushbutton tool that does everything for you, but rather as a collection of scripts/tools that will help you convert a QNN into a custom FPGA accelerator that performs high-performance inference. We do provide several examples of taking trained networks all the way down to FPGA bitfiles, but if you are trying to do this for custom networks you will have to write your own Python scripts that call the appropriate FINN Compiler functions that process your design correctly, or adding new functions as required.

Requirements
============

* Ubuntu 18.04
* Docker
* A working Vivado 2019.1 installation
* A `VIVADO_PATH` environment variable pointing to the Vivado installation directory (e.g. the directory where settings64.sh is located)
* (optional) A PYNQ board with a network connection
   * the ``bitstring`` package must be installed on the PYNQ: ``sudo pip3 install bitstring``

Running FINN in Docker
======================
We use Docker extensively for developing and deploying FINN. If you are not familiar with Docker, there are many excellent `online resources <https://docker-curriculum.com/>`_ to get started. There is a Dockerfile in the root of the repository, as well as a `run-docker.sh` script that can be launched in the following modes:

Getting an interactive shell for development or experimentation
***************************************************************
::

  sh run_docker.sh

Simply running sh run-docker.sh without any additional arguments will clone the dependency repos, create a Docker container and give you a terminal with you can use for development for experimentation.

.. warning:: The Docker container is spawned with the `--rm` option, so make sure that any important files you created inside the container are either in the /workspace/finn folder (which is mounted from the host computer) or otherwise backed up.

.. note:: **Develop from host, run inside container:** The FINN repository directory will be mounted from the host, so that you can use a text editor on your host computer to develop and the changes will be reflected directly inside the container.

Running the Jupyter notebooks
*****************************
::

  sh run-docker.sh notebook

This will launch the `Jupyter notebook <https://jupyter.org/>`_ server inside a Docker container, and print a link on the terminal that you can open in your browser to run the FINN notebooks or create new ones.
.. note:: The link will look something like this (the token you get will be different):
http://127.0.0.1:8888/?token=f5c6bd32ae93ec103a88152214baedff4ce1850d81065bfc

The run-docker.sh script forwards ports 8888 for Jupyter and 8081 for Netron, and launches the notebook server with appropriate arguments.

Running the test suite directly
*******************************
FINN comes with a set of tests to check for regressions. The full test suite
(which will take several hours to run and require a PYNQ board) can be executed
by:

::

  sh run-docker.sh test

There is a quicker variant of the test suite that skips the tests marked as
requiring Vivado or as slow-running tests:

::

  sh run-docker.sh quicktest

If you want to run individual tests, you can do this *inside the Docker container
from the FINN root directory* as follows:

::

  python setup.py test --addopts "-k test_end2end_tfc_w1a2"

Please see the pytest documentation for more about picking tests by marks or
by name.

Environment variables
**********************

Prior to running the `run-docker.sh` script, there are several environment variables you can set to configure certain aspects of FINN.
These are summarized below:

* `VIVADO_PATH` points to your Vivado installation on the host
* `JUPYTER_PORT` (default 8888) changes the port for Jupyter inside Docker
* `NETRON_PORT` (default 8081) changes the port for Netron inside Docker
* `NUM_DEFAULT_WORKERS` (default 1) specifies the degree of parallelization for the transformations that can be run in parallel
* `PYNQ_BOARD` specifies the type of PYNQ board used (Pynq-Z1, Pynq-Z2, Ultra96, ZCU104) for the test suite
* `PYNQ_IP` and `PYNQ_PORT` specify ip address and port number to access the PYNQ board
* `PYNQ_USERNAME` and `PYNQ_PASSWORD` specify the PYNQ board access credentials for the test suite
* `PYNQ_TARGET_DIR` specifies the target dir on the PYNQ board for the test suite
