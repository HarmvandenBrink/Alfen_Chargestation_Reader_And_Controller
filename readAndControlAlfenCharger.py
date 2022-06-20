#!/usr/bin/env python

"""
A-ChargeStationReaderAndController: A charge station reader for Alfen NG9xx chargers.

MIT License

Copyright (c) 2022 Harm van den Brink

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

__author__  = 'Harm van den Brink'
__email__   = 'harmvandenbrink@gmail.com'
__license__ = 'MIT License'

__version__ = '1.42'
__status__  = 'Production'

####### Imports #######

from alfenchargestation import AlfenCharger

               #AlfenCharger('ID, 'IP', minCurrent, maxCurrent)
chargestation = AlfenCharger('XYZ', '192.168.1.X', 0, 20)

chargestation.readMeasurements()
print(chargestation.platformtype)
print(chargestation.meterstate)
print(chargestation.meterlastvaluetimestamp)
print(chargestation.metertype)
print(chargestation.voltage_l1n)
print(chargestation.voltage_l2n)
print(chargestation.voltage_l3n)
print(chargestation.voltage_l1l2)
print(chargestation.voltage_l2l3)
print(chargestation.voltage_l3l1)
print(chargestation.current_n)
print(chargestation.current_l1)
print(chargestation.current_l2)
print(chargestation.current_l3)
print(chargestation.current_sum)
print(chargestation.powerfactor_l1)
print(chargestation.powerfactor_l2)
print(chargestation.powerfactor_l3)
print(chargestation.powerfactor_sum)
print(chargestation.frequency)
print(chargestation.realpower_l1)
print(chargestation.realpower_l2)
print(chargestation.realpower_l3)
print(chargestation.realpower_sum)
print(chargestation.apparentpower_l1)
print(chargestation.apparentpower_l2)
print(chargestation.apparentpower_l3)
print(chargestation.apparentpower_sum)
print(chargestation.reactivepower_l1)
print(chargestation.reactivepower_l2)
print(chargestation.reactivepower_l3)
print(chargestation.reactivepower_sum)
print(chargestation.realenergydelivered_l1)
print(chargestation.realenergydelivered_l2)
print(chargestation.realenergydelivered_l3)
print(chargestation.realenergydelivered_sum)
print(chargestation.realenergyconsumed_l1)
print(chargestation.realenergyconsumed_l2)
print(chargestation.realenergyconsumed_l3)
print(chargestation.realenergyconsumed_sum)

#chargestation.changeCurrent(10)
