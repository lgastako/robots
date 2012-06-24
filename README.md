Easy robots.txt management (inspired by Kenneth Reitz's requests et al)

    >>> import robots
    >>> robots.allow("SomeBot/1.0", "http://www.google.com/search")
    False
    >>> robots.allow("SomeBot/1.0", "http://www.google.com/about")
    True

Or, if you want to be able to check relative resources on specific domains:

    >>> google = robots.site("http://www.google.com/")  # or...
    >>> google = robots.site("www.google.com")

    and then

    >>> google.allow("SomeBot/1.0", "/search")
    False
    >>> google.allow("SomeBot/1.0", "/about")
    True

Note that the robots.txt for google.com and www.google.com may not be
the same.

Or, if you want to be able to check many domains for the same user agent:

    >>> somebot = robots.bot("SomeBot/1.0")
    >>> somebot.allow("http://www.google.com/search")
    False
    >>> somebot.allow("http://www.google.com/about")
    True

And last but not least if you need to check a lot of URLs for one site for
on specific user-agent and you want to do it by path, you can make a site_bot:

    >>> google_somebot = robots.site_bot("www.google.com", "SomeBot/1.0")
    >>> google_somebot.allow("/search")
    False
    >>> google_somebot.allow("/about")
    True

The "allow" function/method(s) are actually implemented as the negation of
the "disallow" method which sticks closer to the style of the robots.txt
semantics but generally leads to a lot of double negatives in code.

The alias "ok" also exists for the "allow" function to save typing in
interactive sessions.

All robots.txt files are kept parsed in memory (in python RobotsFileParser
objects).  If you need to, you can cause them to be refreshed via calls
to the refresh function/method(s).

By default refreshes are eager.  This means that when you request a refresh
any old parsers are dumped and a new RobotsFileParser is created which
immediately reads the robots.txt and is ready to process new requests.  In
the case where you specify lazy=True in your refresh call the old parser
will be dumped (if one exists), but no new parser will be created (nor will
any robots.txt file be fetched) until a query is made against that domain.

If you pass no positional arguments all parsers will be refreshed.  If you
pass positional arguments they will be treated as hosts or URLs of parsers
to be dropped.
