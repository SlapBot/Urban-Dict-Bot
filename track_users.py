from urban_dict.twitter_get import TwitterGet


tg = TwitterGet(flag="follows")
tg.stream_follow(tg.follow_ids)
