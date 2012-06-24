import urlparse
import robotparser

_RFPS = {}


def _host_from_url(url):
    return urlparse.urlparse(url).netloc.split(":", 1)[0]


def _create_rfp_for_host(host):
    robots_txt_url = "http://%s/robots.txt" % host
    rfp = robotparser.RobotFileParser()
    rfp.set_url(robots_txt_url)
    rfp.read()
    return rfp


def _parser_for_url(url):
    host = _host_from_url(url)
    rfp = _RFPS.get(host)
    if not rfp:
        rfp = _create_rfp_for_host(host)
        _RFPS[host] = rfp
    return rfp


def disallow(ua, url):
    parser = _parser_for_url(url)
    return not parser.can_fetch(ua, url)


def allow(ua, url):
    return not disallow(ua, url)

ok = allow


def refresh(*args, **kwargs):
    lazy = kwargs.pop("lazy", False)
    if args:
        for host in args:
            if lazy:
                del _RFPS[host]
            else:
                _RFPS[host] = _create_rfp_for_host(host)
    else:
        global _RFPS
        if lazy:
            _RFPS = {}
        else:
            _RFPS = {host:_create_rfp_for_host(host) for host in _RFPS}


class SiteFocusedRoboMan(object):

    def __init__(self, url_or_host):
        if "://" in url_or_host:
            host = _host_from_url(url_or_host)
        else:
            host = url_or_host
        self.host = host
        prefix = host
        if "://" not in prefix:
            prefix = "http://%s" % prefix
        self.prefix = prefix

    def _make_url(self, path):
        return self.prefix + path

    def allow(self, ua, path):
        url = self._make_url(path)
        return allow(ua, url)

    def disallow(self, ua, path):
        url = self._make_url(path)
        return disallow(ua, url)

    ok = allow

    def refresh(self, lazy=False):
        refresh(self.host, lazy=lazy)


site = SiteFocusedRoboMan


class UserAgentFocusedRoboMan(object):

    def __init__(self, user_agent):
        self.user_agent = user_agent

    def allow(self, url):
        return allow(self.user_agent, url)

    def disallow(self, url):
        return disallow(self.user_agent, url)

    ok = allow


bot = UserAgentFocusedRoboMan


class DualFocusedRoboMan(object):

    def __init__(self, url_or_host, user_agent):
        self.site = site(url_or_host)
        self.user_agent = user_agent

    def allow(self, path):
        return self.site.allow(self.user_agent, path)

    def disallow(self, path):
        return self.site.disallow(self.user_agent, path)

    ok = allow

    def refresh(self, lazy=False, *args):
        self.site.refresh(lazy=lazy)


site_bot = DualFocusedRoboMan
