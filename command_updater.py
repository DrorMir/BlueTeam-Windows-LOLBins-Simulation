import os
import json
from repo_parser import RepoParser
import repo_importer

class CommandUpdater:
    def __init__(self):
        self._curr_dir = os.path.dirname(os.path.abspath(__file__))
        self._commands_json_path = os.path.join(self._curr_dir, "commands.json")

    def import_repo(self, repo_url, repo_name):
        repo_importer.RepoImporter(self._curr_dir, repo_url, repo_name)

    def parse_repo(self, repo_name):
        parser = RepoParser(os.path.join(self._curr_dir, repo_name))
        commands = parser.get_commands()
        with open(self._commands_json_path, "w", encoding="utf-8") as f:
            json.dump(commands, f, indent=4)
        print(f"Successfully parsed commands and saved to {self._commands_json_path}")


