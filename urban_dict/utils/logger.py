import os
import json
import time


class Logger:
    def __init__(self, name="log.json"):
        self.filename = self.retrieve_filename(name)
        self.ids = self.get_already_posted_ids(self.filename)

    @staticmethod
    def retrieve_filename(name):
        filename = os.path.abspath(os.path.join(os.path.dirname(__file__),
                                                os.pardir, os.pardir, name))
        return filename

    @staticmethod
    def get_json_data(filename):
        with open(filename, "r") as j:
            json_data = json.load(j)
        return json_data

    @staticmethod
    def get_already_posted_ids(data):
        return data

    def log(self, tweet):
        self.ids[tweet['term']] = {
            "id": tweet['id'],
            "tweeted_at": time.ctime()
        }

        with open(self.filename, "w") as j:
            json.dump(self.ids, j)

        self.ids = self.get_json_data(self.filename)
        return True


logger = Logger()
