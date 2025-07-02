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

class Axis:
    def __init__(self, symlink = None):
        #create tic object
        self.tic = pytic.Tic()
        
        #get serial number
        serial_num = extract_serial_number(symlink)

        #connect to tic
        self.tic.connect_to_serial_number(serial_num)

        #load config file and apply settings
        self.tic.settings.load_config_file('/Users/banjo/Documents/Python/Okra/config.yml')
        self.tic.settings.apply()

        #stop + set position to 0
        self.tic.halt_and_set_position(0)

        #energize and exit safe start
        self.tic.energize()
        self.tic.exit_safe_start()

    def set_velocity(self, velocity):
        self.tic.set_target_velocity(velocity)

class Pd:
    def __init__(self, axis, kp=0, kd=0):
        self.kp = kp
        self.kd = kd
        self.axis = axis
        self.previous_error = 0

    def update_velocity(self, error):
        p = error*self.kp
        
        d= (error-self.previous_error)*self.kd

        self.axis.set_velocity(p + d)

        self.previous_error = error        

class Okra_tracker:
    def __init__(self, symlinks, kps, kds):
        self.x_axis = Axis(symlinks[0])
        self.y_axis = Axis(symlinks[1])

        self.pd_x = Pd(self.x_axis, kps[0], kds[0])
        self.pd_y = Pd(self.y_axis, kps[1], kds[1])

    def update_error(self):
        self.pd_x.update_velocity(#error x)
        self.pd_y.update_velocity(#error y)