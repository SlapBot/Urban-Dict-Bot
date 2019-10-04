import requests
from bs4 import BeautifulSoup
from urban_dict.workflow import Workflow
from urban_dict.utils.logger import logger
from urllib import parse


class StatusUpdater(object):
    def __init__(self):
        self.base_url = "https://www.urbandictionary.com"
        self.trending_definitions_div = "trending-words-panel"
        self.wf = Workflow()

    def make_status(self):
        definitions = self.get_trending_definitions()
        posted_ids = logger.ids
        if definitions:
            valid_definitions = [parse.unquote(definition) for definition in definitions if
                                 not parse.unquote(definition) in posted_ids]
            if valid_definitions:
                status = self.wf.process_status(valid_definitions[0])
                if status:
                    logger.log({
                        'term': valid_definitions[0],
                        'id': status.id
                    })

    def get_trending_definitions(self):
        r = self.make_request()
        if not r:
            return False
        definitions_div = self.scrape_trending_definitions(r.text)
        if not definitions_div:
            return False
        return self.scrape_definitions(definitions_div)

    def make_request(self):
        r = requests.get(self.base_url)
        if r.ok:
            return r
        return False

    def scrape_trending_definitions(self, html):
        soup = BeautifulSoup(html, "html.parser")
        return soup.find("div", self.trending_definitions_div)

    @staticmethod
    def scrape_definitions(soup):
        links = soup.find_all("a", "trending-link")
        links = [l['href'] for l in links]
        return [link.split("term=")[-1] for link in links]
