from ..common.config import AppConfigReader


class MotdConstants(object):
    MODULE = "motd"


class MotdConfig(object):
    _config = AppConfigReader.read(MotdConstants.MODULE)

    MOTD_ICAL_URL = _config['preferences']['ical_url']
    REQUEST_TIMEOUT = int(_config['preferences'].get('request_timeout_seconds', '15'))
