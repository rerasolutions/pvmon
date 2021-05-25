import minimalmodbus
import serial
from enum import IntEnum


class PvMonRegister(IntEnum):
    IRRADIANCE = 22
    TEMPERATURE = 24
    VOLTAGE = 73
    CURRENT = 75
    POWER = 77
    ENERGY = 89


class PVMON:
    def __init__(self, comport, temperature_node_id, power_node_id):
        self.baudrate = 9600
        self.temperature_node_id = temperature_node_id
        self.power_node_id = power_node_id
        self.comport = comport
        if self.setup_modbus():
            self.show_config()
        else:
            print('cannot configure instrument')

    def show_config(self):
        print('PVMON Settings:')
        print('Port: ', self.comport)
        print('Baudrate: ', self.baudrate)
        print('Temperature Node: ', self.temperature_node_id)
        print('Power Node: ', self.power_node_id)

    def setup_modbus(self):
        try:
            self.mb_power = minimalmodbus.Instrument(self.comport, self.temperature_node_id,
                                                           minimalmodbus.MODE_RTU)
            self.mb_power.serial.baudrate = self.baudrate
            self.mb_power.serial.bytesize = 8
            self.mb_power.serial.parity = serial.PARITY_NONE
            self.mb_power.serial.stopbits = 1
            self.mb_power.serial.timeout = 0.05  # seconds
            self.mb_power.address = self.power_node_id
            self.mb_power.clear_buffers_before_each_transaction = True

            self.mb_temperature = minimalmodbus.Instrument(self.comport, self.temperature_node_id,
                                                           minimalmodbus.MODE_RTU)
            self.mb_temperature.serial.baudrate = self.baudrate
            self.mb_temperature.serial.bytesize = 8
            self.mb_temperature.serial.parity = serial.PARITY_NONE
            self.mb_temperature.serial.stopbits = 2
            self.mb_temperature.serial.timeout = 0.05  # seconds
            self.mb_temperature.address = self.temperature_node_id
            self.mb_temperature.clear_buffers_before_each_transaction = True
        except:
            return False

        return True

    def read_float_value(self, address):
        if address in [PvMonRegister.TEMPERATURE, PvMonRegister.IRRADIANCE]:
            return self.mb_temperature.read_float(address)
        return self.mb_power.read_float(address)

    def read_instrument_float_value(self, instrument, address):
        return instrument.read_float(address)

    def read_instrument_int_value(self, instrument, address):
        return instrument.read_register(address)

    def read_instrument_int_values(self, instrument, address, count):
        return instrument.read_registers(address, count)


pvmon = PVMON('COM1', 33, 48)
pvmon.show_config()

print('Current: ', pvmon.read_float_value(PvMonRegister.CURRENT))
print('Voltage: ', pvmon.read_float_value(PvMonRegister.VOLTAGE))
print('Power: ', pvmon.read_float_value(PvMonRegister.POWER))
print('Energy: ', pvmon.read_float_value(PvMonRegister.ENERGY))
print('Temperature: ', pvmon.read_float_value(PvMonRegister.TEMPERATURE))
print('Irradiance: ', pvmon.read_float_value(PvMonRegister.IRRADIANCE))

