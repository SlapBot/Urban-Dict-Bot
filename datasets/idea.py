import requests
from bs4 import BeautifulSoup as BS


def definition(term, page=1):
    base_url = "https://www.urbandictionary.com/define.php"
    params = {
        "term": term,
        "page": page
    }
    r = requests.get(base_url, params=params)
    if r.ok:
        return r
    return False


def scrape_definition_divs(html):
    soup = BS(html, "html.parser")
    return soup.find_all("div", "def-panel")


def scrape_meaning(soup):
    return soup.find("div", "meaning").text.replace("\r", "\n").split("\n")


def scrape_tags(soup):
    return soup.find("div", "tags").text.replace("\r", "\n").split("\n")


def scrape_contributor(soup):
    return soup.find("div", "contributor").text.replace("\r", "\n").split("\n")


def scrape_example(soup):
    return soup.find("div", "example").text.replace("\r", "\n").split("\n")


def scrape_votes(soup):
    return {
        "up": int(soup.find("a", "up").text),
        "down": int(soup.find("a", "down").text)
    }


def scrape_answer(soup):
    return {
        "meaning": scrape_meaning(soup),
        "example": scrape_example(soup),
        "tags": scrape_tags(soup),
        "contributor": scrape_contributor(soup),
        "votes": scrape_votes(soup)
    }


def get_html_answers(term, page=1):
    r = definition(term, page)
    if r:
        return scrape_definition_divs(r.text)
    return False


def scrape_all_answers_from_page(term, page=1):
    html_list = get_html_answers(term, page)
    if not html_list:
        return False
    answers = []
    for index, soup in enumerate(html_list):
        print("definition number: %s" % index)
        try:
            answers.append(scrape_answer(soup))
        except Exception as e:
            print(e)
    return answers


def scrape_all_answers(term, threshold=2):
    everything = []
    status = True
    page = 1
    while status and page < threshold:
        answers = scrape_all_answers_from_page(term, page)
        if not answers:
            status = False
            continue
        everything.extend(answers)
        print("page number: %s" % page)
        page += 1
    return everything


def sort_by_up(answers):
    answers.sort(key=lambda x: x['votes']['up'])
    return answers


def sort_by_down(answers):
    answers.sort(key=lambda x: x['votes']['down'])
    return answers


def sort_by_ratio(answers):
    answers.sort(key=lambda x: (x['votes']['up']) / (x['votes']['down'] + 1))
    return answers


def s():
    return scrape_all_answers("Virginia")

#add heading and url (with tweet) + clean /r/n stuff