import os


class Templater(object):
    def __init__(self, data=None):
        if data is None:
            data = {}
        self.data = data
        self.template_file = self.get_static_file_path("template.html")
        self.content_file = self.get_static_file_path("content.html")
        self.html_text = ""

    def set_data(self, data):
        self.data = data
        return self

    def get_content_filename(self):
        return self.content_file

    def process(self):
        content = self.create_content(self.data)
        self.get_template_html_file().replace_html_text(content).save_content_html_file(self.content_file)

    def replace_html_text(self, content):
        self.html_text = self.html_text.replace(
            "{heading}", content['heading'],
        ).replace(
            "{meaning}", content['meaning'],
        ).replace(
            "{example}", content['example'],
        ).replace(
            "{tags}", content['tags'],
        ).replace(
            "{contributor}", content['contributor'],
        )
        return self

    def get_template_html_file(self):
        with open(self.template_file, "r") as html:
            self.html_text = html.read()
        html.close()
        return self

    def save_content_html_file(self, content_file):
        with open(content_file, "w") as html:
            html.write(self.html_text)
        html.close()

    def create_content(self, data):
        return {
            "heading": self.data['term'],
            "meaning": self.create_meaning(data['meaning']),
            "example": self.create_example(data['example']),
            "tags": self.create_tags(data['tags']),
            "contributor": self.create_contributor(data['contributor']),
        }

    @staticmethod
    def create_meaning(param):
        param.insert(0, "<p>")
        param.append("</p>")
        return "</p><p>".join(param)

    @staticmethod
    def create_example(param):
        if len(param) == 0:
            return "Reply with an example to this tweet."
        param.insert(0, "<p>")
        param.append("</p>")
        return "</p><p>".join(param)

    def create_tags(self, param):
        if len(param) == 0:
            return "<a href='#'>#{0}</a".format(self.data['term'])
        param.insert(0, "<a href='#'> ")
        param.append("</a>")
        return "</a><a href='#'> ".join(param)

    @staticmethod
    def create_contributor(param):
        name = param[0].split("by ")[1]
        output = ["by ", "<a href='#'>", name, "</a> ", param[-1]]
        return "".join(output)

    @staticmethod
    def get_static_file_path(filename):
        return os.path.dirname(os.path.join(os.path.dirname(__file__),
                                            os.pardir, os.pardir, os.pardir)) + '/static/' + filename
