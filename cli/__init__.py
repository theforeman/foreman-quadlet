#!/usr/bin/env python3
# PYTHON_ARGCOMPLETE_OK

"""
An installer for Foreman.
"""
import os
import obsah
import sys


class ApplicationConfig(obsah.ApplicationConfig):
    """
    A class describing the where to find various files
    """

    @staticmethod
    def name():
        """
        Return the name as shown to the user in the ArgumentParser
        """
        return 'rop'

    @staticmethod
    def data_path():
        """
        Return the data path. Houses playbooks and configs.
        """
        path = os.environ.get('ROP_DATA')
        if path is None:
            path = os.getcwd()

        return path

    @classmethod
    def ansible_config_path(cls):
        """
        Return the ansible.cfg path
        """
        return os.environ.get('OBSAH_ANSIBLE_CFG', os.path.join(cls.data_path(), 'ansible.cfg'))

    @staticmethod
    def inventory_path():
        """
        Return the inventory path
        """
        return os.environ.get('OBSAH_INVENTORY', os.path.join(os.getcwd(), 'inventories'))


def main(cliargs=['--help'], application_config=ApplicationConfig):  # pylint: disable=R0914
    """
    Main command
    """
    if len(sys.argv) > 1:
        cliargs = sys.argv[1:]

    obsah.main(cliargs=cliargs, application_config=application_config)


if __name__ == '__main__':
    main()
