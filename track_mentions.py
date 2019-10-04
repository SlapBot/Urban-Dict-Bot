from urban_dict.twitter_get import TwitterGet


tg = TwitterGet(flag="mentions")
tg.stream_track(tg.handle)
