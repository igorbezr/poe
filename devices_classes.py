import pexpect
from pexpect import TIMEOUT, EOF
import re


class POEdevice():

    def __init__(self, ip, username, password):
        self.ip = ip
        self.username = username
        self.password = password
        self.session = None
        self.hostname = None
        self.consumers = 0
        self.used_power = 0
        self.available_power = 0
        self.timeout_message = ' '.join([
            'Connection to the device', self.ip, 'timed out:'])
        self.unexpected_message = ' '.join([
            'Connection to the device', self.ip,
            'received unexpected output :'])

    def initial_connect_ssh(self):
        try:
            credentials = 'ssh ' + self.username + '@' + self.ip
            self.session = pexpect.spawn(credentials, timeout=30)
            new_host = bool(self.session.expect(['rd:', 'no']))
            if new_host is True:
                self.session.sendline('yes')
                self.session.expect('rd:')
            self.session.sendline(self.password)
            self.session.expect(['#', '>'])
            return True
        except TIMEOUT:
            print(self.timeout_message)
            print(self.session.before.decode('utf-8').strip())
            return False
        except EOF:
            print(self.unexpected_message)
            print(self.session.before.decode('utf-8').strip())
            return False

    def initial_connect_telnet(self):
        try:
            credentials = 'telnet ' + self.ip
            self.session = pexpect.spawn(credentials, timeout=30)
            self.session.expect('name:')
            self.session.sendline(self.username)
            self.session.expect('rd:')
            self.session.sendline(self.password)
            self.session.expect(['#', '>'])
            return True
        except TIMEOUT:
            print(self.timeout_message)
            print(self.session.before.decode('utf-8').strip())
            return False
        except EOF:
            print(self.unexpected_message)
            print(self.session.before.decode('utf-8').strip())
            return False

    def send_command(self, command):
        try:
            self.session.sendline(command)
            self.session.expect(['#', '>'])
            return True
        except TIMEOUT:
            print(self.timeout_message)
            return False
        except EOF:
            print(self.unexpected_message)
            print(self.session.before.strip())
            return False

    def search_device_hostname(self):
        self.send_command('show running-config | in hostname')
        config = self.session.before.decode('utf-8').splitlines()
        host = re.compile('^hostname +.*')
        for line in config:
            line = line.strip()
            if host.search(line):
                self.hostname = host.search(line).group(0)[9:]
                break
        return None

    def parsing_show_power_inline_output(self):
        self.send_command('show power inline | in on|Available')
        config = self.session.before.decode('utf-8').splitlines()
        available = re.compile('[0-9]{3}\.[0-9]')
        consumer = re.compile('on         [0-9]{1,2}\.[0-9]')
        if available.search(config[1]):
                available_power = float(available.search(config[1]).group(0))
        for line in config[2:]:
            if consumer.search(line):
                self.consumers += 1
                used_power = float(consumer.search(line).group(0)[11:])
                self.used_power += used_power
        self.available_power = available_power - self.used_power
        self.used_power = round(self.used_power, 2)
        self.available_power = round(self.available_power, 2)
        return None
