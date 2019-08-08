"""
openvpn_control/utils/fileio.py
"""
import os
import logging
import shutil

from subprocess import call


logger = logging.getLogger(__name__)


def ensure_directory_exists(directory_path: str) -> True:
    """

    :param directory_path: str -
    :return: bool -
    :raises: OSError - Exception from os.mkdir
    """
    assert directory_path, 'directory_path cannot be blank'
    assert isinstance(directory_path, str), 'directory_path must be a string'

    if not os.path.isdir(directory_path):
        try:
            os.mkdir(directory_path)
        except OSError as e:
            logger.exception(e)
            raise
        else:
            logger.debug(f'Created directory: {directory_path}')
    return True


def remove_directory_contents(directory_path: str) -> True:
    """

    :param directory_path: str -
    :return: bool -
    :raises: OSError - Exception from os.mkdir
    """
    assert directory_path, 'directory_path cannot be blank'
    assert isinstance(directory_path, str), 'directory_path must be a string'

    try:
        if os.path.isdir(directory_path):
            for f in os.listdir(directory_path):
                os.remove(os.path.join(directory_path, f))

            shutil.rmtree(directory_path)

    except OSError as e:
        logger.exception(e)
        raise

    return True


def write_configuration(config_dir: str, auth_file: str, auth: str, conf_file: str, vpn_conf_lines: str) -> bool:
    """

    :param config_dir:
    :param auth_file:
    :param auth:
    :param conf_file:
    :param vpn_conf_lines:
    :return:
    """
    assert config_dir, 'config_dir cannot be blank'
    assert isinstance(config_dir, str), 'config_dir must be a string'

    assert auth_file, 'auth_file cannot be blank'
    assert isinstance(auth_file, str), 'auth_file must be a string'

    assert auth, 'auth cannot be blank'
    assert isinstance(auth, str), 'auth must be a string'

    assert conf_file, 'conf_file cannot be blank'
    assert isinstance(conf_file, str), 'conf_file must be a string'

    # Create the directory if it doesn't exist
    ensure_directory_exists(config_dir)

    try:
        with open(auth_file, 'w') as _f:
            _f.write(auth)
    except IOError as e:
        logger.exception(e)
        raise

    cmd = f'chmod 0600 {auth_file}'
    results = call(cmd, shell=True)
    logger.debug(results)

    try:
        with open(conf_file, 'w') as _f:
            for line in vpn_conf_lines:
                _f.write(line + '\n')
    except IOError as e:
        logger.exception(e)
        raise

    return True