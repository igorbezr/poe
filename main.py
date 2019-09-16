
import devices_classes as dev
from input_output_function import (
    reading_ip_from_file, keyboard_input,
    output_to_console)

try:
    ip_addresses = reading_ip_from_file('devices.txt')
    credentials = keyboard_input()
    csv_log = open('log.csv', 'w')
    csv_log.write('sep=,' + '\n')
    csv_log.write('IP, hostname, PoE consumer, PoE summary power' + '\n')
    for ip in ip_addresses:
        device = dev.POEconsumer(
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
                str(device.poe_consumers) + ',' +
                str(device.poe_summarypower) + '\n')
            csv_log.write(csv_row)
        device.session.close()
    csv_log.close()
except KeyboardInterrupt:
    print('\n', 'Program is terminated due to user request !')
exit()
