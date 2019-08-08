"""
openvpn_control/utils/openvpn.py
"""
import time
import logging

from subprocess import call, Popen, PIPE, TimeoutExpired

from openvpn_control.settings import WHICH_OPENVPN


logger = logging.getLogger(__name__)


def start_nohup(server_name: str, config_path: str, auth_path: str) -> bool:
    """

    :return:
    """
    logger.info(f'VPN [{server_name}]')
    proc = None

    cmd = f'sudo nohup {WHICH_OPENVPN} --config {config_path} --auth-user-pass {auth_path} --auth-nocache &'
    try:
        proc = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
    except OSError:
        pass

    if proc is not None:
        try:
            outs, errs = proc.communicate(timeout=20)
        except TimeoutExpired as e:
            logger.warning(e)
            try:
                proc.kill()
            except OSError:
                pass

    time.sleep(5)
    return True


def killall() -> bool:
    """

    :return:
    """
    cmd = 'sudo killall openvpn'
    results = call(cmd, shell=True)
    if any(['No matching processes were found' in results, 'no process found' in results]):
        return True
    return False
