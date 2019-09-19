
import devices_classes as dev
from input_output_function import (
    reading_ip_from_file, keyboard_input,
    output_to_console)

try:
    ip_addresses = reading_ip_from_file('devices.txt')
    credentials = keyboard_input()
    csv_log = open('log.csv', 'w')
    csv_log.write('sep=,' + '\n')
    columns_headers = (
        'IP,' +
        'hostname,' +
        'PoE consumers,' +
        'Total used power,' +
        'Remaining available power' + '\n')
    csv_log.write(columns_headers)
    for ip in ip_addresses:
        device = dev.POEdevice(
            ip,
            credentials['username'],
            credentials['password'])
        if device.initial_connect_ssh() or device.initial_connect_telnet():
            device.send_command('terminal length 0')
            device.search_device_hostname()
            device.parsing_show_power_inline_output()
            output_to_console(device)
            csv_row = (
                str(device.ip) + ',' +
                str(device.hostname) + ',' +
                str(device.consumers) + ',' +
                str(device.used_power) + ',' +
                str(device.available_power) + '\n')
            csv_log.write(csv_row)
        device.session.close()
    csv_log.close()
except KeyboardInterrupt:
    print('\n', 'Program is terminated due to user request !')
exit()
