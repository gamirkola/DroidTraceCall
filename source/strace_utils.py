"""strace_utils.py:
====================================
"""

import subprocess
from config.get_config import config as cfg

class StraceUtils:

    def __init__(self):
        """
        StraceUtils class:
            This class contains the main function used to build and eventually push strace to the phone

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
            strace_push = input("[+] Do you want to push the strace executable to the phone? (Y/n): ") or 'y'
            if strace_push == 'y':
                if cfg.probe['intermediary_folder_path'] is None:
                    print('[*] Pushing strace to /{}/DroidTraceCall'.format(cfg.probe['probe_folder_path']))
                    device.push('../tools/strace/strace', '/{}/DroidTraceCall/strace'.format(cfg.probe['probe_folder_path']))
                    print('[*] Making strace bin executable...')
                    device.shell('chmod +x /{}/DroidTraceCall/strace'.format(cfg.probe['probe_folder_path']))
                    return True
                else:
                    print('[*] Pushing strace to /{}/DroidTraceCall'.format(cfg.probe['intermediary_folder_path']))
                    device.push('../tools/strace/strace', '/{}/DroidTraceCall/strace'.format(cfg.probe['intermediary_folder_path']))
                    print('[*] Making strace bin executable...')
                    device.shell('chmod +x /{}/DroidTraceCall/strace'.format(cfg.probe['intermediary_folder_path']))
                    return True

        except Exception as e:
            print('Error: {}'.format(e))
            return False
