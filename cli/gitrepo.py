class GitRepo():
    '''Base class for git repository metadata'''

    def __init__(self, url):
        self.url = url
        self.branches = {}

    def add_branch(self, branch_name, commit_hash):
        if not branch_name in self.branches:
            self.branches[branch_name] = commit_hash
