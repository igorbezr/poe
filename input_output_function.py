from getpass import getpass


def reading_ip_from_file(devices):
    ip_addresses = list()
    file = open(devices, 'r')
    ip_addresses = [line.strip() for line in file]
    file.close()
    return ip_addresses


def keyboard_input():
    print('Good day to you !' + '\n' + 'Welcome to checking PoE script !')
    credentials = dict()
    while True:
        try:
            credentials['username'] = input(
                'Enter username (or Ctrl-C to exit) > ')
            credentials['password'] = getpass(
                'Enter password (or Ctrl-C to exit) > ')
            return credentials
        except KeyboardInterrupt:
            print('\n', 'Program is terminated due to user request !')
            exit()


def output_to_console(dev):
    print('')
    print('Device IP address is', str(dev.ip))
    print('Device hostname is', str(dev.hostname))
    print('Device PoE consumers =', str(dev.poe_consumers))
    print('Device summary PoE power =', str(dev.poe_summarypower))
    return None
