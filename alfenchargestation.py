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
__name__    = 'Alfen NG9x Control Class'

from collections import OrderedDict
from pymodbus.constants import Endian
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.payload import BinaryPayloadDecoder
import time

class AlfenCharger:
    def __init__(self, id, ip, minimumCurrent, maximumCurrent):
        self.id = id
        self.ip = ip
        self.minimumCurrent = minimumCurrent
        self.maximumCurrent = maximumCurrent

    def changeCurrent(self, current):
        
        def limitChargeStationCurrent(num, minimum=self.minimumCurrent, maximum=self.maximumCurrent):
            return max(min(num, maximum), minimum)

        chargeStationModbus = ModbusClient(self.ip, port=502, unit_id=1 , auto_open=True, auto_close=True)
        time.sleep(0.1)
        builder = BinaryPayloadBuilder(byteorder=Endian.Big, wordorder=Endian.Big)
        builder.add_32bit_float(limitChargeStationCurrent(current))        
        registers = builder.to_registers()
        chargeStationModbus.write_registers(1210, registers, unit=1)

        chargeStationModbus.close()

    def readMeasurements(self):

        def readChargeStationData(address,count, unit):
            result = chargeStationModbus.read_holding_registers(address, count,  unit=unit)
            decoder = BinaryPayloadDecoder.fromRegisters(result.registers, byteorder=Endian.Big, wordorder=Endian.Big)
            return decoder

        chargeStationModbus = ModbusClient(self.ip, port=502, unit_id=1 , auto_open=True, auto_close=True)
        time.sleep(0.1)

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

        self.meterstate = decodedEnergyMeasurements['meterstate']
        self.meterlastvaluetimestamp = decodedEnergyMeasurements['meterlastvaluetimestamp']
        self.metertype = decodedEnergyMeasurements['metertype']
        self.voltage_l1n = decodedEnergyMeasurements['voltage_l1n']
        self.voltage_l2n = decodedEnergyMeasurements['voltage_l2n']
        self.voltage_l3n = decodedEnergyMeasurements['voltage_l3n']
        self.voltage_l1l2 = decodedEnergyMeasurements['voltage_l1l2']
        self.voltage_l2l3 = decodedEnergyMeasurements['voltage_l2l3']
        self.voltage_l3l1 = decodedEnergyMeasurements['voltage_l3l1']
        self.current_n = decodedEnergyMeasurements['current_n']
        self.current_l1 = decodedEnergyMeasurements['current_l1']
        self.current_l2 = decodedEnergyMeasurements['current_l2']
        self.current_l3 = decodedEnergyMeasurements['current_l3']
        self.current_sum = decodedEnergyMeasurements['current_sum']
        self.powerfactor_l1 = decodedEnergyMeasurements['powerfactor_l1']
        self.powerfactor_l2 = decodedEnergyMeasurements['powerfactor_l2']
        self.powerfactor_l3 = decodedEnergyMeasurements['powerfactor_l3']
        self.powerfactor_sum = decodedEnergyMeasurements['powerfactor_sum']
        self.frequency = decodedEnergyMeasurements['frequency']
        self.realpower_l1 = decodedEnergyMeasurements['realpower_l1']
        self.realpower_l2 = decodedEnergyMeasurements['realpower_l2']
        self.realpower_l3 = decodedEnergyMeasurements['realpower_l3']
        self.realpower_sum = decodedEnergyMeasurements['realpower_sum']
        self.apparentpower_l1 = decodedEnergyMeasurements['apparentpower_l1']
        self.apparentpower_l2 = decodedEnergyMeasurements['apparentpower_l2']
        self.apparentpower_l3 = decodedEnergyMeasurements['apparentpower_l3']
        self.apparentpower_sum = decodedEnergyMeasurements['apparentpower_sum']
        self.reactivepower_l1 = decodedEnergyMeasurements['reactivepower_l1']
        self.reactivepower_l2 = decodedEnergyMeasurements['reactivepower_l2']
        self.reactivepower_l3 = decodedEnergyMeasurements['reactivepower_l3']
        self.reactivepower_sum = decodedEnergyMeasurements['reactivepower_sum']
        self.realenergydelivered_l1 = decodedEnergyMeasurements['realenergydelivered_l1']
        self.realenergydelivered_l2 = decodedEnergyMeasurements['realenergydelivered_l2']
        self.realenergydelivered_l3 = decodedEnergyMeasurements['realenergydelivered_l3']
        self.realenergydelivered_sum = decodedEnergyMeasurements['realenergydelivered_sum']
        self.realenergyconsumed_l1 = decodedEnergyMeasurements['realenergyconsumed_l1']
        self.realenergyconsumed_l2 = decodedEnergyMeasurements['realenergyconsumed_l2']
        self.realenergyconsumed_l3 = decodedEnergyMeasurements['realenergyconsumed_l3']
        self.realenergyconsumed_sum = decodedEnergyMeasurements['realenergyconsumed_sum']
        
        time.sleep(0.1)
        
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

        self.apparentenergy_l1 = decodedEnergyMeasurementsRest['apparentenergy_l1']
        self.apparentenergy_l2 = decodedEnergyMeasurementsRest['apparentenergy_l2']
        self.apparentenergy_l3 = decodedEnergyMeasurementsRest['apparentenergy_l3']
        self.apparentenergy_sum = decodedEnergyMeasurementsRest['apparentenergy_sum']
        self.reactiveenergy_l1 = decodedEnergyMeasurementsRest['reactiveenergy_l1']
        self.reactiveenergy_l2 = decodedEnergyMeasurementsRest['reactiveenergy_l2']
        self.reactiveenergy_l3 = decodedEnergyMeasurementsRest['reactiveenergy_l3']
        self.reactiveenergy_sum = decodedEnergyMeasurementsRest['reactiveenergy_sum']
        
        time.sleep(0.1)
        
        decoder = readChargeStationData(1200,16,1)
        decodedStatusAndTransactionRegisters = OrderedDict([
                ('availability', decoder.decode_16bit_uint()),
                ('mode3state', decoder.decode_string(10).decode("utf-8").replace('\x00','')),
                ('actualappliedmaxcurrent', decoder.decode_32bit_float()),
                ('modbusslavemaxcurrentvalidtime', decoder.decode_32bit_uint()),
                ('modbusslavemaxcurrent', decoder.decode_32bit_float()),
                ('activeloadbalancingsafecurrent', decoder.decode_32bit_float()),
                ('modbusslavereceivedsetpointaccountedfor', decoder.decode_16bit_uint()),
                ('chargeusing1or3phases', decoder.decode_16bit_uint()),
            ])

        self.availability = decodedStatusAndTransactionRegisters['availability']
        self.mode3state = decodedStatusAndTransactionRegisters['mode3state']
        self.actualappliedmaxcurrent = decodedStatusAndTransactionRegisters['actualappliedmaxcurrent']
        self.modbusslavemaxcurrentvalidtime = decodedStatusAndTransactionRegisters['modbusslavemaxcurrentvalidtime']
        self.modbusslavemaxcurrent = decodedStatusAndTransactionRegisters['modbusslavemaxcurrent']
        self.activeloadbalancingsafecurrent = decodedStatusAndTransactionRegisters['activeloadbalancingsafecurrent']
        self.modbusslavereceivedsetpointaccountedfor = decodedStatusAndTransactionRegisters['modbusslavereceivedsetpointaccountedfor']
        self.chargeusing1or3phases = decodedStatusAndTransactionRegisters['chargeusing1or3phases']

        time.sleep(0.1)
        
        decoder = readChargeStationData(1100,6,200)
        decodedStationStatusRegisters = OrderedDict([
                ('stationactivemaxcurrent', decoder.decode_32bit_float()),
                ('temperature', decoder.decode_32bit_float()),
                ('ocppstate', decoder.decode_16bit_uint()),
                ('nrofsockets', decoder.decode_16bit_uint()),
            ])

        self.stationactivemaxcurrent = decodedStationStatusRegisters['stationactivemaxcurrent']
        self.temperature = decodedStationStatusRegisters['temperature']
        self.ocppstate = decodedStationStatusRegisters['ocppstate']
        self.nrofsockets = decodedStationStatusRegisters['nrofsockets']
            
        time.sleep(0.1)
            
        decoder = readChargeStationData(100,79,200)
        decodedProductIdentificationRegisters = OrderedDict([
                ('name', decoder.decode_string(34).decode("utf-8").replace('\x00','')),
                ('manufacturer', decoder.decode_string(10).decode("utf-8").replace('\x00','')),
                ('modbustableversion', decoder.decode_16bit_int()),
                ('firmwareversion', decoder.decode_string(34).decode("utf-8").replace('\x00','')),
                ('platformtype', decoder.decode_string(34).decode("utf-8").replace('\x00','')),
                ('stationserialnumber', decoder.decode_string(22).decode("utf-8").replace('\x00','')),
                ('year', decoder.decode_16bit_int()),
                ('month', decoder.decode_16bit_int()),
                ('day', decoder.decode_16bit_int()),
                ('hour', decoder.decode_16bit_int()),
                ('minute', decoder.decode_16bit_int()),
                ('second', decoder.decode_16bit_int()),
                ('uptime', decoder.decode_64bit_uint()),
                ('timezone', decoder.decode_16bit_int())
            ])

        self.name = decodedProductIdentificationRegisters['name']
        self.manufacturer = decodedProductIdentificationRegisters['manufacturer']
        self.modbustableversion = decodedProductIdentificationRegisters['modbustableversion']
        self.firmwareversion = decodedProductIdentificationRegisters['firmwareversion']
        self.platformtype = decodedProductIdentificationRegisters['platformtype']
        self.stationserialnumber = decodedProductIdentificationRegisters['stationserialnumber']
        self.year = decodedProductIdentificationRegisters['year']
        self.month = decodedProductIdentificationRegisters['month']
        self.day = decodedProductIdentificationRegisters['day']
        self.hour = decodedProductIdentificationRegisters['hour']
        self.minute = decodedProductIdentificationRegisters['minute']
        self.second = decodedProductIdentificationRegisters['second']
        self.uptime = decodedProductIdentificationRegisters['uptime']
        self.timezone = decodedProductIdentificationRegisters['timezone']

        chargeStationModbus.close()
