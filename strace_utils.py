"""strace_utils.py:
====================================
"""

import subprocess


class StraceUtils:

    def __init__(self):
        """
        StraceUtils class:
            Thsi class contains the main function used to build and eventually push strace to the phone

            -device: Instance of the device you want to work on
        """

    @staticmethod
    def compile_strace():
        """
        Compile strace for aarm64 using the script in
        "/scripts/strace/compile_strace_aarch64.sh"

        ----------
        No parameters

        Returns
        ----------
        Return True if the build is successful
        Return False otherwise
        """
        try:
            # launch strace compile script
            subprocess.run('./compile_strace_aarch64.sh', shell=True, cwd='./scripts/strace/')
            return True
        except Exception as e:
            print('Error: {}'.format(e))
            return False

    @staticmethod
    def push_strace(device):
        """
        Push strace bin to the phone inside "/data/DroidTraceCall/"

        ----------
        No parameters

        Returns
        ----------
        Return True if the bin is pushed correctly
        Return False otherwise
        """
        try:
            print('[*] Pushing strace to /data/DroidTraceCall/')
            device.push('./tools/strace/strace', '/data/DroidTraceCall/strace')
            print('[*] Making strace bin executable...')
            device.shell('chmod +x /data/DroidTraceCall/strace')
            return True
        except Exception as e:
            print('Error: {}'.format(e))
            return False