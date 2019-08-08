"""
openvpn_control/settings.py
"""

PUBLIC_IP_URLS = [
    'https://api.ipify.org/',
    'https://icanhazip.com/json/'
]

LOCATION_METADATA_URLS = [
    'https://geoip-db.com/json/'
]

# Default settings for openvpn configuration files
AUTH_FILE_NAME = 'auth.conf'
CONF_FILE_NAME = 'vpnconf.ovpn'

WHICH_OPENVPN = '/usr/local/sbin/openvpn'
