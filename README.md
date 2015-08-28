RC_TotPow
=========

Overview
--------
Measurement of the total radiated power of an equipement under test in an electromagnetic reverberation chamber.  The programs cover the calibration process and the measurement itself. Instruments are controlled with the PyVisa package. Stirrer is controlled with the MinimalModBus package.


Required packages
-----------------
* Python 2.x
* Numpy
* PyVISA
* MinimalModBus

`RC_calibration.py` performs a calibration using a signal generator and a spectrum analyser.
`Total_radiated_Power.py` measures the total radiated power on the whole frequency range.
