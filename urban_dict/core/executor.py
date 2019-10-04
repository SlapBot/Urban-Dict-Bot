import os
from urban_dict.utils.configurer import config


class Executor(object):
    def __init__(self, input_filename="", output_filename=""):
        self.config = config
        self.input_filename = input_filename,
        self.output_filename = output_filename
        self.application = ""
        self.script_name = ""
        self.command = ""
        self.create_command()

    def execute(self):
        os.system(self.command)

    def create_command(self):
        phantom_js_path = self.config.get_configuration("phantom_js_path", "SYSTEM")
        js_script_filename = self.config.get_configuration("js_script_filename", "SYSTEM")
        self.application = self.get_project_file_path() + "/" + phantom_js_path
        self.script_name = self.get_project_file_path() + "/" + js_script_filename
        self.output_filename = self.get_project_file_path() + "/" + 'static/export.png'
        self.command = self.application + " " + self.script_name + " " + self.input_filename[0] + " " + self.output_filename

    @staticmethod
    def get_project_file_path():
        return os.path.dirname(os.path.join(os.path.dirname(__file__),
                                            os.pardir, os.pardir, os.pardir))
