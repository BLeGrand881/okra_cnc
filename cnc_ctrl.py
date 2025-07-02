import pytic 
from subprocess import run
from os import path

def extract_serial_number(symlink_path):
    device_path = path.realpath(symlink_path)

    result = run(['udevadm', 'info', '--query=all', '--name={}'.format(device_path)], capture_output=True, text=True)

    for line in result.stdout.split('\n'):
        if 'ID_SERIAL_SHORT=' in line:
            serial_number = line.split('=')[1]
            return serial_number
        
    print(f"Serial number not found for {symlink_path}")

class cnc:
    def __init__(self, x_symlink = None, y_symlink = None, z_symlink = None):
        #create tic objects
        if not (x_symlink and y_symlink and z_symlink):
            serial_nums = self.tic_x.list_connected_device_serial_numbers()
        else:
            serial_nums = [extract_serial_number(x_symlink), extract_serial_number(y_symlink), extract_serial_number(z_symlink)]
        
        self.tic_x = pytic.Tic()
        self.tic_y = pytic.Tic()
        self.tic_z = pytic.Tic()

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

    def set_y_velocity(self, y_velocity):
        self.tic_y.set_target_velocity(y_velocity)  
    
    def set_z_velocity(self, z_velocity):
        self.tic_z.set_target_velocity(z_velocity)

class pid