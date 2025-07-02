import pytic 
from time import sleep

class cnc:
    def __init__(self):
        #create tic objects
        self.tic_x = pytic.Tic()
        self.tic_y = pytic.Tic()
        self.tic_z = pytic.Tic()
        
        #list connected devices
        serial_nums = self.tic_x.list_connected_device_serial_numbers()

        #connect to tics
        self.tic_x.connect_to_serial_number(serial_nums[0])
        self.tic_y.connect_to_serial_number(serial_nums[1])
        self.tic_z.connect_to_serial_number(serial_nums[2])

        #load config file
        self.tic_x.settings.load_config_file('/Users/banjo/Documents/Python/Okra/config.yml')
        self.tic_y.settings.load_config_file('/Users/banjo/Documents/Python/Okra/config.yml')
        self.tic_z.settings.load_config_file('/Users/banjo/Documents/Python/Okra/config.yml')

        #apply settings
        self.tic_x.settings.apply()
        self.tic_y.settings.apply()
        self.tic_z.settings.apply()

        #stop + set position to 0
        self.tic_x.halt_and_set_position(0)
        self.tic_y.halt_and_set_position(0)
        self.tic_z.halt_and_set_position(0)

        #energize and exit safe start
        self.tic_x.energize()
        self.tic_y.energize()
        self.tic_z.energize()

        self.tic_x.exit_safe_start()
        self.tic_y.exit_safe_start()
        self.tic_z.exit_safe_start()

    def set_x_velocity(self, x_velocity):
        self.tic_x.set_target_velocity(x_velocity)
