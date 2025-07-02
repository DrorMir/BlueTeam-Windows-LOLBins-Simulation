import os #path

import repo_parser
import repo_importer

class CommandUpdater:
    def __init__(self):
        self._curr_dir = os.path.dirname(os.path.abspath(__file__))
        self._commands_json = f"{self._curr_dir}/commands.json"
        if not os.path.isfile(self._commands_json):
            self._commands_json = open(f"{self._curr_dir}/commands.json", "x")

    def import_repo(self, repo_url, repo_name):
        repo_importer.RepoImporter(self._curr_dir, repo_url, repo_name)

    def parse_repo(self, repo_name):
        repo_parser.RepoParser(f"{self._curr_dir}/{repo_name}")

                
