"""
openvpn_control/metadata.py
"""
import logging
import random
import requests

from typing import List
from requests.exceptions import ConnectionError


logger = logging.getLogger(__name__)


def get_metadata(metadata_urls: List[str]) -> dict:
    """
    Gets related information about the machine's location from the ip address.

    :param metadata_urls: List[str]
    :return: dict -
    """
    random.shuffle(metadata_urls)

    response = {}
    for url in metadata_urls:
        retries = 3
        metadata_found = False

        res_json = ''
        while retries and not metadata_found:
            try:
                res = requests.get(url, verify=False)
            except ConnectionError as e:
                logger.warning(e)
                retries -= 1
            else:
                if res.status_code == 200:
                    res_json = res.json()
                    metadata_found = True
                    break
                else:
                    retries -= 1

        if not metadata_found:
            continue

        try:
            res_json['ip']
        except (KeyError, TypeError):
            try:
                ipv4 = res_json['IPv4']
            except (KeyError, TypeError):
                continue
            else:
                res_json['ip'] = ipv4
                res_json.pop('IPv4', None)

        try:
            res_json['zip_code']
        except (KeyError, TypeError):
            try:
                res_json['zip_code'] = res_json['postal']
            except (KeyError, TypeError):
                pass

        response = res_json
        break

    return response


def get_machine_ip(public_ip_urls: List[str]) -> str:
    """

    :param public_ip_urls:
    :return:
    """
    response = ''

    # Randomize the list of urls to use
    random.shuffle(public_ip_urls)
    for url in public_ip_urls:
        retries = 3
        public_ip_found = False

        while retries and not public_ip_found:
            try:
                req = requests.get(url)
            except ConnectionError as e:
                logger.warning(e)
                # Decrease the number of attempts left
                retries -= 1
                continue
            else:
                try:
                    req_status_code = req.status_code
                except AttributeError as e:
                    logger.debug(e)
                    # Decrease the number of attempts left
                    retries -= 1
                    continue
                else:
                    if req_status_code == 200:
                        try:
                            response = req.text.replace('\n', '')
                        except AttributeError as e:
                            logger.debug(e)
                            # Decrease the number of attempts left
                            retries -= 1
                            continue
                        else:
                            public_ip_found = True
                            break
                    else:
                        # Decrease the number of attempts left
                        retries -= 1
                        continue

        # If the ip address has been found, break from the loop
        if public_ip_found:
            break
    return response


def vpn_ip(home_ip: str, public_ip_urls: List[str]) -> bool:
    """

    :param home_ip:
    :param public_ip_urls:
    :return:
    """
    current = get_machine_ip(public_ip_urls)
    if not current:
        logger.exception('Error: vpn_ip|get_ip')
        return False

    logger.info('IP [{0}]'.format(current))
    if all([home_ip, home_ip != current, current != '']):
        logger.info('VPN Connection Success')
        return True
    return False
