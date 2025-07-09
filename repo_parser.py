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

                        if isinstance(content, dict) and "Commands" in content:
                            for command in content["Commands"]:
                                mitre_id = command.get("MitreID", "N/A")
                                if isinstance(mitre_id, list):
                                    mitre_id = mitre_id[0]

                                # Check for 'Severity' field, if not present, assign a default or skip
                                severity = command.get("Severity", "Informational") # Default to Informational

                                if all(k in command for k in ["Command", "Description"]):
                                    self._commands.append({
                                        "Command": command["Command"],
                                        "Description": command["Description"],
                                        "Severity": severity,
                                        "MitreAttackTag": mitre_id
                                    })
                                else:
                                    print(f"[!] Skipping malformed command in {file_path}: {command}")

                    except Exception as e:
                        print(f"[!] Failed to parse {file_path}: {e}")
        
    def get_commands(self):
        return self._commands