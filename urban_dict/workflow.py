from urban_dict.core.filter_text import FilterText
from urban_dict.core.urban_dictionary_get import UrbanDictionaryGet
from urban_dict.core.templater import Templater
from urban_dict.core.executor import Executor
from urban_dict.core.twitter_post import TwitterPost
from urban_dict.utils.configurer import config
import json


class Workflow(object):
    def __init__(self, flag="mentions"):
        self.ft = FilterText()
        self.tp = TwitterPost()
        self.flag = flag

    def consume(self, string):
        data = json.loads(string)
        if self.flag == "mentions":
            return self.mentions(data)
        else:
            return self.follows(data)

    def mentions(self, data):
        if 'entities' in data and 'user_mentions' in data['entities']:
            user_mentions = data['entities']['user_mentions']
            status = any(
                int(user_mention['id']) == int(config.get_configuration("twitter_id"))
                for user_mention in user_mentions)
            if status:
                tweet = self.clean(data)
                term = self.parse_mention_term(tweet['text'])
                ss_status = self.create_screenshot(term)
                if not ss_status:
                    return False
                status = self.tp.reply(tweet)
                if not status:
                    print("Mission Failed. Didn't work")
                    return False
                print("Tweeted back successfully.")
                return status
        return False

    def follows(self, data):
        if 'in_reply_to_status_id' in data and data['in_reply_to_status_id'] is not None:
            return False
        if 'retweeted_status' in data and data['retweeted_status'] is not None:
            return False
        if 'in_reply_to_user_id' in data and data['in_reply_to_user_id'] is not None:
            return False

        tweet = self.clean(data)
        known_keywords, unknown_keywords = self.ft.filter(tweet['text'])
        keywords = self.prioritize(known_keywords, unknown_keywords)
        if len(keywords) == 0:
            print("No good keywords found.")
            return False
        print("Keywords: %s" % keywords)
        definitions = self.get_definitions_from_keywords(keywords)
        if len(definitions) == 0:
            print("No definitions found for any keywords.")
            return False
        print("Total Definitions Found: %s" % len(definitions))
        definition = self.find_the_best_definition(definitions)
        content_filename = self.setup_template(definition)
        self.execute_shell_command(content_filename)
        status = self.tp.reply(tweet)
        if not status:
            print("Mission Failed. Didn't work")
            return False
        print("Tweeted back successfully.")
        return status

    def process_status(self, term):
        ss_status = self.create_screenshot(term)
        if not ss_status:
            return False
        status = self.tp.status_update()
        if not status:
            print("Mission Failed. Didn't work")
            return False
        return status

    def create_screenshot(self, term):
        definitions = self.get_definitions_from_keyword(term)
        if len(definitions) == 0:
            print("No definitions found for any keywords.")
            return False
        definition = self.find_the_best_definition(definitions)
        content_filename = self.setup_template(definition)
        self.execute_shell_command(content_filename)
        return True

    @staticmethod
    def clean(data):
        tweet = {
            "id": data['id'],
            "text": data['text'],
            "created_at": data['created_at'],
            "user": {
                "id": data['user']['id'],
                "name": data['user']['name'],
                "screen_name": data['user']['screen_name'],
            }
        }
        print(tweet)
        return tweet

    @staticmethod
    def prioritize(known_keywords, unknown_keywords):
        keywords = []
        for known_keyword in known_keywords:
            if known_keyword[1] > 1000:
                keywords.append(known_keyword[0])
        for index, unknown_keyword in enumerate(unknown_keywords):
            if index < 3:
                keywords.append(unknown_keyword[0])
        return keywords

    @staticmethod
    def get_definitions_from_keywords(keywords):
        ubd = UrbanDictionaryGet()
        all_definitions = []
        for keyword in keywords:
            keyword_definitions = ubd.scrape(keyword)
            if keyword_definitions:
                all_definitions.extend(keyword_definitions)
        return all_definitions

    @staticmethod
    def get_definitions_from_keyword(keyword):
        print("Searching for term: {0}".format(keyword))
        ubd = UrbanDictionaryGet()
        return ubd.scrape(keyword)

    @staticmethod
    def find_the_best_definition(definitions):
        print("The best definition being searched among: %s" % len(definitions))
        sorted_definitions = UrbanDictionaryGet.sort_by_up(definitions)
        return sorted_definitions[0]

    @staticmethod
    def setup_template(definition):
        tp = Templater(definition)
        tp.process()
        return tp.get_content_filename()

    @staticmethod
    def execute_shell_command(content_filename):
        exe = Executor(content_filename)
        return exe.execute()

    @staticmethod
    def parse_mention_term(text):
        if "define" in text.lower():
            return " ".join(text.split(" ")[2:])
        return " ".join(text.split(" ")[1:])
