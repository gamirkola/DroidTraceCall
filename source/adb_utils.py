"""adb_utils.py:
====================================
"""

from adb_shell.adb_device import AdbDeviceUsb, AdbDeviceTcp
from adb_shell.auth.sign_pythonrsa import PythonRSASigner
import os
from pathlib import Path
from config.get_config import config as cfg


class AdbUtils:

    def __init__(self):
        """
            AdbUtils class:
                This class contains some utils for the adb_shell functions.
        """

    @staticmethod
    def adb_key():
        """
        Set the adb key path for the authentication on the phone,
        asks to the user to specify a custom path for adbkey,
        otherwise the path in linux is set to "/home/<user>/.android/adbkey"

        ----------
        No parameters

        Returns
        ----------
        Return PythonRSASigner istance fi the keys are found
        Returns False if an exception occours
        """
        custom_path = cfg.adb['adbkey_folder_path']
        if custom_path is not None:
            if Path(custom_path).exists():
                adbKey = custom_path
            else:
                print('[*] Path invalid ({}), check the config!'.format(custom_path))
                exit(1)
        else:
            adbKey = str(Path.home()) + '/.android/adbkey'
        print('[*] Adb key path: ' + adbKey)
        if not os.path.exists(adbKey):
            print('[!] Error retrieving the file')
            return False
        try:
            with open(adbKey) as f:
                private = f.read()
            with open(adbKey + '.pub') as f:
                public = f.read()
            return PythonRSASigner(public, private)
        except Exception as e:
            print('Error: {}'.format(e))
            return False

    def tcp(self):
        """
        Set adb connections via TCP

        ----------
        No parameters

        Returns
        ----------
        Device() istance if the selected device is found
        str error, if no device found
        """
        # get adb key
        signer = self.adb_key()
        # Connect
        ip = input('[+] Insert the device IP:')
        device = AdbDeviceTcp(ip, 5555, default_transport_timeout_s=9.)
        device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        # Send a shell command
        if device.available:
            print('[*] Device connected!')
            return device
        else:
            return '[!] Error in connecting the device'

    def usb(self):
        """
        Set adb connection via USB

        ----------
        No parameters

        Returns
        ----------
        Device() istance if the selected device is found
        str error, if no device found
        """
        signer = self.adb_key()
        device = AdbDeviceUsb()
        device.connect(rsa_keys=[signer], auth_timeout_s=0.1)
        if device.available:
            print('[*] Device connected!')
            return device
        else:
            return '[!] Error in connecting the device'

    def connect_device(self):
        """
        Set adb connection via USB, this is the only method that should be called

        No parameters

        Returns:
        Device: adb_shell instance of the selected device
        """
        # connection options
        conn_options = {1: self.tcp, 2: self.usb}
        print("\n[!] Please select \"Always allow from this computer\" in the adb dialog!")
        conn_type = input("[+] Select ADB connection method: \n\t[1] TCP \n\t[2] USB \n>")
        if conn_type:
            connect = conn_options.get(int(conn_type), '[!] Invalid option')
            if isinstance(connect, str):
                print(connect)
                return False
            else:
                device = connect()
                return device
