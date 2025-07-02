import json
import os
import yaml

class RepoParser:
    def __init__(self, repo_path):
        self._yml_root = os.path.join(repo_path, "yml")
        self._commands = []
        for root, dirs, files in os.walk(self._yml_root):
            for file in files:
                if file.endswith(".yml") or file.endswith(".yaml"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = yaml.safe_load(f)

                        if isinstance(content, list):
                            for technique in content:
                                commands = technique.get("Commands", [])
                                for command in commands:
                                    self._commands.append((file.replace(".yml", ""), command))

                    except Exception as e:
                        print(f"[!] Failed to parse {file_path}: {e}")
        
        print(self._commands)