import pytest

import robots

# NOTE: These tests currently hit the internet.  I'm not sure if there's
# enough value in mocking it all out.  If you can't hit the internet is this
# library really that useful to you?


class RobotsTxtTests(object):
    USER_AGENT = "SomeBot/1.0"
    BASE_URL = "http://www.google.com"
    DISALLOWED_PATH = "/search"
    DISALLOWED_URL = BASE_URL + DISALLOWED_PATH
    ALLOWED_PATH = "/about"
    ALLOWED_URL = BASE_URL + ALLOWED_PATH
    ALLOWED_URL2 = "http://www.yahoo.com/search"
    ALLOWED_URL3 = "http://www.bing.com/search"


class TestUnwrappedAccess(RobotsTxtTests):

    def test_allow_yes(self):
        assert robots.allow(self.USER_AGENT, self.ALLOWED_URL) is True

    def test_allow_no(self):
        assert robots.allow(self.USER_AGENT, self.DISALLOWED_URL) is False

    def test_disallow_yes(self):
        assert robots.disallow(self.USER_AGENT, self.DISALLOWED_URL) is True

    def test_disallow_no(self):
        assert robots.disallow(self.USER_AGENT, self.ALLOWED_URL) is False

    def test_refresh_all_eager(self):
        # Ensure exactly one cached parser
        robots._RFPS = {}
        robots.allow(self.USER_AGENT, self.ALLOWED_URL)

        old_rfp = robots._RFPS.values()[0]
        assert len(robots._RFPS) == 1

        robots.refresh()

        assert len(robots._RFPS) == 1
        new_rfp = robots._RFPS.values()[0]
        assert new_rfp != old_rfp

    def test_refresh_all_lazy(self):
        # Ensure exactly one cached parser
        robots._RFPS = {}
        robots.allow(self.USER_AGENT, self.ALLOWED_URL)

        old_rfp = robots._RFPS.values()[0]
        assert len(robots._RFPS) == 1

        robots.refresh(lazy=True)

        assert len(robots._RFPS) == 0

    def test_refresh_some_eager(self):
        robots._RFPS = {}
        robots.allow(self.USER_AGENT, self.ALLOWED_URL)
        robots.allow(self.USER_AGENT, self.ALLOWED_URL2)
        robots.allow(self.USER_AGENT, self.ALLOWED_URL3)

        old_rfps = robots._RFPS.values()
        assert len(robots._RFPS) == 3

        robots.refresh("www.google.com", "www.yahoo.com")

        assert len(robots._RFPS) == 3
        new_rfps = robots._RFPS.values()
        assert sum([1 if rfp in new_rfps else 0 for rfp in old_rfps]) == 1

    def test_refresh_some_lazy(self):
        robots._RFPS = {}
        robots.allow(self.USER_AGENT, self.ALLOWED_URL)
        robots.allow(self.USER_AGENT, self.ALLOWED_URL2)
        robots.allow(self.USER_AGENT, self.ALLOWED_URL3)

        old_rfps = robots._RFPS.values()
        assert len(robots._RFPS) == 3

        robots.refresh("www.google.com", "www.yahoo.com", lazy=True)

        assert len(robots._RFPS) == 1


class TestSite(RobotsTxtTests):

    def test_allow_by_full_url(self):
        google = robots.site("http://www.google.com/")
        assert google.allow(self.USER_AGENT, self.DISALLOWED_PATH) is False

    def test_disallow_by_full_url(self):
        google = robots.site("http://www.google.com/")
        assert google.disallow(self.USER_AGENT, self.DISALLOWED_PATH) is True

    def test_allow_by_hostname(self):
        google = robots.site("www.google.com")
        assert google.allow(self.USER_AGENT, self.DISALLOWED_PATH) is False

    def test_disallow_by_hostname(self):
        google = robots.site("www.google.com")
        assert google.disallow(self.USER_AGENT, self.DISALLOWED_PATH) is True

    def test_refresh_eager(self):
        robots._RFPS = {}
        google = robots.site("www.google.com")
        google.allow(self.USER_AGENT, "/")
        assert len(robots._RFPS) == 1
        old_rfp = robots._RFPS.values()[0]
        google.refresh()
        assert len(robots._RFPS) == 1
        new_rfp = robots._RFPS.values()[0]
        assert new_rfp != old_rfp

    def test_refresh_lazy(self):
        robots._RFPS = {}
        google = robots.site("www.google.com")
        google.allow(self.USER_AGENT, "/")
        assert len(robots._RFPS) == 1
        google.refresh(lazy=True)
        assert len(robots._RFPS) == 0


class TestBot(RobotsTxtTests):

    def setup_method(self, method):
        self.some_bot = robots.bot("SomeBot/1.0")

    def test_basics(self):
        assert not self.some_bot.allow(self.DISALLOWED_URL)
        assert self.some_bot.allow(self.ALLOWED_URL)


class TestSiteBot(RobotsTxtTests):

    def setup_method(self, method):
        self.google_somebot = robots.site_bot("www.google.com", "SomeBot/1.0")

    def test_basics(self):
        assert self.google_somebot.allow(self.DISALLOWED_PATH) is False
        assert self.google_somebot.allow(self.ALLOWED_PATH) is True

    def test_refresh_eager(self):
        robots._RFPS = {}
        self.google_somebot.allow("/")
        assert len(robots._RFPS) == 1
        old_rfp = robots._RFPS.values()[0]
        self.google_somebot.refresh()
        assert len(robots._RFPS) == 1
        new_rfp = robots._RFPS.values()[0]
        assert new_rfp != old_rfp

    def test_refresh_lazy(self):
        robots._RFPS = {}
        self.google_somebot.allow("/")
        assert len(robots._RFPS) == 1
        self.google_somebot.refresh(lazy=True)
        assert len(robots._RFPS) == 0
