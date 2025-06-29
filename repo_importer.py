import sys #exit
import os
from pathlib import Path

try:
    from git import Repo  # pip install gitpython
except:
    print("Module 'gitpython' is not installed. Please install it via:")
    print("pip install gitpython")
    sys.exit()


class RepoImporter:
    def __init__(self, working_dir, repo_url, repo_name):
        self._repo_dir = f"{Path(working_dir).parent.absolute()}/{repo_name}"
        if not os.path.isdir(self._repo_dir):
            Repo.clone_from(repo_url, self._repo_dir)
        else:
            Repo(self._repo_dir).remotes.origin.pull()
        

