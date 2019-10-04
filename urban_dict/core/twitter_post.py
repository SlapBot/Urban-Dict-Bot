from urban_dict.utils.configurer import config
from tweepy import API, OAuthHandler
import os


class TwitterPost(object):
    def __init__(self):
        self.config = config
        self.consumer_key = config.get_configuration("consumer_key")
        self.consumer_secret = config.get_configuration("consumer_secret")
        self.access_token = config.get_configuration("access_token")
        self.access_token_secret = config.get_configuration("access_token_secret")
        self.auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        self.auth.set_access_token(self.access_token, self.access_token_secret)
        self.api = API(self.auth)
        self.media_filename = self.get_media_filepath(self.config.get_configuration("media_filename", "SYSTEM"))

    def reply(self, parent_tweet):
        try:
            upload_status = self.upload_media(self.media_filename)
        except Exception:
            print("Problem in uploading media")
            return False
        print(upload_status)
        return self.reply_with_media(upload_status, parent_tweet)

    def get_media_filepath(self, filename):
        return self.get_project_file_path() + '/' + filename

    @staticmethod
    def get_project_file_path():
        return os.path.dirname(os.path.join(os.path.dirname(__file__),
                                            os.pardir, os.pardir, os.pardir))

    def upload_media(self, media_filename):
        return self.api.media_upload(media_filename)

    def reply_with_media(self, upload_status, parent_tweet):
        text = "@" + parent_tweet['user']['screen_name']
        try:
            status = self.api.update_status(
                status=text,
                in_reply_to_status_id=parent_tweet['id'],
                media_ids=[upload_status.media_id]
            )
            return status
        except Exception:
            print("Error in posting a reply")
            return False

    def status_update(self):
        try:
            upload_status = self.upload_media(self.media_filename)
        except Exception:
            print("Problem in uploading media")
            return False
        print(upload_status)
        return self.post_timeline(upload_status)

    def post_timeline(self, upload_status):
        status = self.config.get_configuration("status_title")
        try:
            status = self.api.update_status(
                status=status,
                media_ids=[upload_status.media_id]
            )
            return status
        except Exception:
            print("Error in posting a status_update")
            return False
