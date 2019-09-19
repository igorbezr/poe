from getpass import getpass


def reading_ip_from_file(devices):
    ip_addresses = list()
    with open(devices, 'r') as file:
        ip_addresses = [line.strip() for line in file]
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
    print('PoE consumers =', str(dev.consumers), '(devices)')
    print('Total used power =', str(dev.used_power), '(w)')
    print('Remaining available power =', str(dev.available_power), '(w)')
    return None
