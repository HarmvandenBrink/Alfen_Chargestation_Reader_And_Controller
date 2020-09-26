#!/usr/bin/env python

"""
A-ChargeStationReaderAndController: A charge station reader for Alfen NG9xx chargers.

MIT License

Copyright (c) 2020 Harm van den Brink

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

__version__ = '0.0.1'
__status__  = 'Beta'

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.compat import iteritems
from collections import OrderedDict
from influxdb import InfluxDBClient
import time
import math
from datetime import datetime, timedelta

chargeStationIP = "192.168.0.0"
minimumCurrent = 0
maximumCurrent = 16

chargeStationModbus = ModbusClient(chargeStationIP, port=502, unit_id=1 , auto_open=True, auto_close=True)
print("Connected: {}".format(chargeStationModbus.connect()))
		
def limitChargeStationCurrent(num, minimum=minimumCurrent, maximum=maximumCurrent):
	return max(min(num, maximum), minimum)

def changeChargeStationCurrent(current):
	builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
	builder.add_32bit_float(limitChargeStationCurrent(current))		
	registers = builder.to_registers()
	chargeStationModbus.write_registers(1210, registers, unit=1)

#changeChargeStationCurrent(15)

def readChargeStationData(address,count, unit):
	result = chargeStationModbus.read_holding_registers(address, count,  unit=unit)
	decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
	return decoder

# Dirty way to add two dicts together
def merge_two_dicts(x, y):
    z = x.copy()   # start with x's keys and values
    z.update(y)    # modifies z with y's keys and values & returns None
    return z

def fetchAllRegisters():
	try:
		decoder = readChargeStationData(300,94,1)

		decodedEnergyMeasurements = OrderedDict([
				('meterstate', decoder.decode_16bit_uint()),
				('meterlastvaluetimestamp', decoder.decode_64bit_uint()),
				('metertype', decoder.decode_16bit_uint()),
				('voltage_l1n', decoder.decode_32bit_float()),
				('voltage_l2n', decoder.decode_32bit_float()),
				('voltage_l3n', decoder.decode_32bit_float()),
				('voltage_l1l2', decoder.decode_32bit_float()),
				('voltage_l2l3', decoder.decode_32bit_float()),
				('voltage_l3l1', decoder.decode_32bit_float()),
				('current_n', decoder.decode_32bit_float()),
				('current_l1', decoder.decode_32bit_float()),
				('current_l2', decoder.decode_32bit_float()),
				('current_l3', decoder.decode_32bit_float()),
				('current_sum', decoder.decode_32bit_float()),
				('powerfactor_l1', decoder.decode_32bit_float()),
				('powerfactor_l2', decoder.decode_32bit_float()),
				('powerfactor_l3', decoder.decode_32bit_float()),
				('powerfactor_sum', decoder.decode_32bit_float()),
				('frequency', decoder.decode_32bit_float()),
				('realpower_l1', decoder.decode_32bit_float()),
				('realpower_l2', decoder.decode_32bit_float()),
				('realpower_l3', decoder.decode_32bit_float()),
				('realpower_sum', decoder.decode_32bit_float()),
				('apparentpower_l1', decoder.decode_32bit_float()),
				('apparentpower_l2', decoder.decode_32bit_float()),
				('apparentpower_l3', decoder.decode_32bit_float()),
				('apparentpower_sum', decoder.decode_32bit_float()),
				('reactivepower_l1', decoder.decode_32bit_float()),
				('reactivepower_l2', decoder.decode_32bit_float()),
				('reactivepower_l3', decoder.decode_32bit_float()),
				('reactivepower_sum', decoder.decode_32bit_float()),
				('realenergydelivered_l1', decoder.decode_64bit_float()),
				('realenergydelivered_l2', decoder.decode_64bit_float()),
				('realenergydelivered_l3', decoder.decode_64bit_float()),
				('realenergydelivered_sum', decoder.decode_64bit_float()),
				('realenergyconsumed_l1', decoder.decode_64bit_float()),
				('realenergyconsumed_l2', decoder.decode_64bit_float()),
				('realenergyconsumed_l3', decoder.decode_64bit_float()),
				('realenergyconsumed_sum', decoder.decode_64bit_float())
			])
			
		# print("-" * 60)
		# print("Energy Measurements")
		# print("-" * 60)
		# for name, value in iteritems(decodedEnergyMeasurements):
			# print("%s" % name, value if isinstance(value, int) else value)

		#print(decodedEnergyMeasurements['voltage_l1n'])
		
		decoder = readChargeStationData(394,32,1)
		decodedEnergyMeasurementsRest = OrderedDict([
				('apparentenergy_l1', decoder.decode_64bit_float()),
				('apparentenergy_l2', decoder.decode_64bit_float()),
				('apparentenergy_l3', decoder.decode_64bit_float()),
				('apparentenergy_sum', decoder.decode_64bit_float()),
				('reactiveenergy_l1', decoder.decode_64bit_float()),
				('reactiveenergy_l2', decoder.decode_64bit_float()),
				('reactiveenergy_l3', decoder.decode_64bit_float()),
				('reactiveenergy_sum', decoder.decode_64bit_float())
			])
		z = merge_two_dicts(decodedEnergyMeasurements, decodedEnergyMeasurementsRest)
		
		# print("-" * 60)
		# print("Energy Measurements")
		# print("-" * 60)
		# for name, value in iteritems(decodedEnergyMeasurementsRest):
			# print("%s" % name, value if isinstance(value, int) else value)

		#print(decodedEnergyMeasurements['voltage_l1n'])

		decoder = readChargeStationData(1200,16,1)

		decodedStatusAndTransactionRegisters = OrderedDict([
				('availability', decoder.decode_16bit_uint()),
				('mode3state', decoder.decode_string(10).decode("utf-8")),
				('actualappliedmaxcurrent', decoder.decode_32bit_float()),
				('modbusslavemaxcurrentvalidtime', decoder.decode_32bit_uint()),
				('modbusslavemaxcurrent', decoder.decode_32bit_float()),
				('activeloadbalancingsafecurrent', decoder.decode_32bit_float()),
				('modbusslavereceivedsetpointaccountedfor', decoder.decode_16bit_uint()),
				('chargeusing1or3phases', decoder.decode_16bit_uint()),
			])
			
		z = merge_two_dicts(z, decodedStatusAndTransactionRegisters)
			
		# print("-" * 60)
		# print("Status and transaction registers")
		# print("-" * 60)
		# for name, value in iteritems(decodedStatusAndTransactionRegisters):
			# print("%s" % name, value if isinstance(value, int) else value)

		#print(decodedStatusAndTransactionRegisters['activeloadbalancingsafecurrent'])

		decoder = readChargeStationData(1100,6,200)

		decodedStationStatusRegisters = OrderedDict([

				('stationactivemaxcurrent', decoder.decode_32bit_float()),
				('temperature', decoder.decode_32bit_float()),
				('ocppstate', decoder.decode_16bit_uint()),
				('nrofsockets', decoder.decode_16bit_uint()),
			])
			
		z = merge_two_dicts(z, decodedStationStatusRegisters)
		# print("-" * 60)
		# print("Status and transaction registers")
		# print("-" * 60)
		# for name, value in iteritems(decodedStationStatusRegisters):
			# print("%s" % name, value if isinstance(value, int) else value)

		#print(decodedStationStatusRegisters['activeloadbalancingsafecurrent'])

		decoder = readChargeStationData(100,79,200)

		decodedProductIdentificationRegisters = OrderedDict([
				('name', decoder.decode_string(34).decode("utf-8")),
				('manufacturer', decoder.decode_string(10).decode("utf-8")),
				('modbustableversion', decoder.decode_16bit_int()),
				('firmwareversion', decoder.decode_string(34).decode("utf-8")),
				('platformtype', decoder.decode_string(34).decode("utf-8")),
				('stationserialnumber', decoder.decode_string(22).decode("utf-8")),
				('year', decoder.decode_16bit_int()),
				('month', decoder.decode_16bit_int()),
				('day', decoder.decode_16bit_int()),
				('hour', decoder.decode_16bit_int()),
				('minute', decoder.decode_16bit_int()),
				('second', decoder.decode_16bit_int()),
				('uptime', decoder.decode_64bit_uint()),
				('timezone', decoder.decode_16bit_int())
			])
			
		z = merge_two_dicts(z, decodedProductIdentificationRegisters)
		# print("-" * 60)
		# print("Status and transaction registers")
		# print("-" * 60)
		# for name, value in iteritems(decodedProductIdentificationRegisters):
			# print("%s" % name, value if isinstance(value, int) else value)

		#print(decodedProductIdentificationRegisters['activeloadbalancingsafecurrent'])
		return z
	except:
		print("Error fetching modbus data")

z = fetchAllRegisters()

print("-" * 60)
print("All registers")
print("-" * 60)
for name, value in iteritems(z):
	print("%s" % name, value if isinstance(value, int) else value)
	
#print(z['actualappliedmaxcurrent'])

chargeStationModbus.close()