"""
openvpn_control/vpn.py
"""
import os
import logging

from openvpn_control.utils import fileio, metadata, openvpn
from openvpn_control.settings import \
    AUTH_FILE_NAME, \
    CONF_FILE_NAME, \
    PUBLIC_IP_URLS
from openvpn_control import NAME


logger = logging.getLogger(NAME)


class OpenVpnControl:
    """
    OpenVpnControl
    """
    # Full file paths of auth and configuration files
    tmp_auth_path = None
    tmp_config_path = None

    name = None
    config = None
    auth = None
    home_ip = None
    config_dir = None

    server_name = None

    def __init__(self, app_name: str):
        """

        Args:
            app_name:
        """
        assert app_name, 'app_name cannot be blank'
        assert isinstance(app_name, str), 'app_name must be a string'

        # Set the configuration directory for the initialized app
        conf_dir = os.path.join(os.path.expanduser('~'), f'.{NAME}')
        self.config_dir = os.path.join(conf_dir, app_name)

        # Create the directory if it doesn't exist
        fileio.ensure_directory_exists(conf_dir)
        fileio.ensure_directory_exists(self.config_dir)

        # Cache the internal attributes
        self.tmp_auth = os.path.join(self.config_dir, AUTH_FILE_NAME)
        self.tmp_config = os.path.join(self.config_dir, CONF_FILE_NAME)

        # Close any current OpenVPN connection
        self.close_connection()

        # Cache the home ip address
        self.home_ip = metadata.get_machine_ip(PUBLIC_IP_URLS)
        logger.info('OpenVpnControl Initialized: Base IP [{}]'.format(self.home_ip))

    def open_connection(self, config: dict) -> bool:
        """

        :param config:
        :return:
        """
        assert isinstance(config, dict), 'config must be a dict'

        try:
            server_name = config['server_name']
            vpn_conf_lines = config['configuration']
        except KeyError as e:
            logger.exception(e)
            raise

        fileio.write_configuration(self.config_dir,
                                   self.tmp_auth, '{}\n{}\n'.format(config['user'], config['pw']),
                                   self.tmp_config, vpn_conf_lines)

        # Close any active connections
        self.close_connection()

        connected = False
        retries = 3
        while retries and not connected:
            # Make a new VPN connection
            openvpn.start_nohup(server_name, self.tmp_config, self.tmp_auth)

            if metadata.vpn_ip(self.home_ip, PUBLIC_IP_URLS):
                connected = True
                break

            logger.warning('Could not connect to VPN server')
            retries -= 1

        if retries == 0:
            raise Exception('VPN Failure, retries limit reached.')

        return connected

    def close_connection(self) -> bool:
        """

        :return:
        """
        disconnected = False
        retries = 3
        while retries and not disconnected:
            # Make a new VPN connection
            if openvpn.killall():
                disconnected = True
                break
            retries -= 1

        fileio.remove_directory_contents(self.config_dir)
        return disconnected
