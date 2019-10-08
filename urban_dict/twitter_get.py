# Import the necessary methods from tweepy library
from tweepy import API, OAuthHandler, Stream
from tweepy.streaming import StreamListener

from urban_dict.utils.configurer import config
from urban_dict.workflow import Workflow


class TwitterGet(object):
    def __init__(self, flag):
        # Variables that contains the user credentials to access Twitter API
        self.config = config
        self.consumer_key = config.get_configuration("consumer_key")
        self.consumer_secret = config.get_configuration("consumer_secret")
        self.access_token = config.get_configuration("access_token")
        self.access_token_secret = config.get_configuration("access_token_secret")
        self.stdOL = StdOutListener(flag)
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = API(self.auth)
        self.stream = Stream(self.auth, self.stdOL)
        follow_ids_string = config.get_configuration("follow_ids")
        if follow_ids_string:
            self.follow_ids = follow_ids_string.split(",")
        else:
            self.follow_ids = []
        self.handle = config.get_configuration("twitter_handle").split(",")

    # array of user_ids in string separated by comma
    def stream_follow(self, follow):
        # This line filter Twitter Streams to capture data by the follows: '396469661'
        self.stream.filter(follow=follow)

    # array of tracking keywords in string separated by comma.
    def stream_track(self, track):
        # This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby' or handles
        self.stream.filter(track=track)

    # array of tracking keywords in string
    def stream(self, track, follow):
        # This line filter Twitter Streams to capture data by the keywords and user_ids
        self.stream.filter(track=track, follow=follow)


# This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):
    def __init__(self, flag):
        self.wf = Workflow(flag=flag)

    def on_data(self, data):
        try:
            self.wf.consume(data)
            return True
        except Exception as e:
            print("Some issue occured %s:" % e)

    def on_error(self, status):
        print("Error Status: " + str(status))
        return False
