import requests
from bs4 import BeautifulSoup


class UrbanDictionaryGet(object):
    def __init__(self):
        self.base_url = "https://www.urbandictionary.com/define.php"
        self.definition_div = "def-panel"
        self.meaning_div = "meaning"
        self.tags_div = "tags"
        self.contributor_div = "contributor"
        self.example_div = "example"
        self.term = ""
        self.results = []

    def definition(self, term, page=1):
        params = {
            "term": term,
            "page": page
        }
        r = requests.get(self.base_url, params=params)
        test_results_soup = BeautifulSoup(r.text, 'html.parser')
        if test_results_soup.find("div", "no-results"):
            return False
        if r.ok:
            return r
        return False

    def scrape_definition_divs(self, html):
        soup = BeautifulSoup(html, "html.parser")
        for br in soup.find_all("br"):
            br.replace_with("\n")
        return soup.find_all("div", self.definition_div)

    def scrape_meaning(self, soup):
        return list(filter(None, soup.find("div", self.meaning_div).text.replace("\r", "\n").split("\n")))

    def scrape_tags(self, soup):
        if soup.find("div", self.tags_div):
            return list(filter(None, soup.find("div", self.tags_div).text.replace("\r", "\n").split("\n")))
        return [self.term]

    def scrape_contributor(self, soup):
        return list(filter(None, soup.find("div", self.contributor_div).text.replace("\r", "\n").split("\n")))

    def scrape_example(self, soup):
        return list(filter(None, soup.find("div", self.example_div).text.replace("\r", "\n").split("\n")))

    @staticmethod
    def scrape_votes(soup):
        return {
            "up": int(soup.find("a", "up").text),
            "down": int(soup.find("a", "down").text)
        }

    def scrape_answer(self, soup):
        return {
            "term": self.term,
            "meaning": self.scrape_meaning(soup),
            "example": self.scrape_example(soup),
            "tags": self.scrape_tags(soup),
            "contributor": self.scrape_contributor(soup),
            "votes": self.scrape_votes(soup)
        }

    def get_html_answers(self, term, page=1):
        r = self.definition(term, page)
        if r:
            return self.scrape_definition_divs(r.text)
        return False

    def scrape_all_answers_from_page(self, term, page=1):
        html_list = self.get_html_answers(term, page)
        if not html_list:
            return False
        answers = []
        for index, soup in enumerate(html_list):
            print("definition number: %s" % index)
            try:
                answers.append(self.scrape_answer(soup))
            except Exception as e:
                raise(e)
        return answers

    def scrape_all_answers(self, term, threshold=2):
        self.term = term
        status = True
        page = 1
        print("The term is: %s" % term)
        while status and page < threshold:
            print("page number: %s" % page)
            answers = self.scrape_all_answers_from_page(term, page)
            if not answers:
                status = False
                continue
            self.results.extend(answers)
            page += 1
        return self.results

    @staticmethod
    def sort_by_up(answers):
        # print(answers)
        answers.sort(key=lambda x: x['votes']['up'], reverse=True)
        return answers

    @staticmethod
    def sort_by_down(answers):
        answers.sort(key=lambda x: x['votes']['down'], reverse=True)
        return answers

    @staticmethod
    def sort_by_ratio(answers):
        answers.sort(key=lambda x: (x['votes']['up']) / (x['votes']['down'] + 1), reverse=True)
        return answers

    def scrape(self, term):
        return self.scrape_all_answers(term)
