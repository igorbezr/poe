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
        self.poe_consumers = 0
        self.poe_summarypower = 0
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
        self.send_command('show power inline | in on')
        config = self.session.before.decode('utf-8').splitlines()
        output = re.compile('on         [0-9]\.[0-9]')
        for line in config:
            if output.search(line):
                self.poe_consumers += 1
                poe_power = float(output.search(line).group(0)[11:])
                self.poe_summarypower += poe_power
        return None
