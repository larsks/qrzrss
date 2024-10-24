# qrzrss

I just want to read the gear-for-sale forum in my RSS reader.

After providing the appropriate credentials, if you run `qrzrss` on `localhost:8000`, you can request:

    http://localhost:8000/feed/index.php?forums/ham-radio-gear-for-sale.7/index.rss

And `qrzrss` will make an authenticated request to:

    https://forums.qrz.com/index.php?forums/ham-radio-gear-for-sale.7/index.rss

And then return the results. This allows you to subscribe to the authenticated RSS feed in a local RSS reader.
