class GitBrancherException(Exception):
    """Base GitBrancher Exception

    To use this class, inherit from it and define a
    a 'msg_fmt' property. That msg_fmt will get printf'd
    with the keyword arguments provided to the constructor.

    """

    msg_fmt = "An unknown exception occurred."

    def __init__(self, message=None, **kwargs):
        self.kwargs = kwargs
        self.message = message
        if not self.message:
            try:
                self.message = msg_fmt % kwargs
            except:
                # arguments in kwargs doesn't match variables in msg_fmt
                import six
                for name, value in six.iteritems(kwargs):
                    LOG.error("%s: %s" % (name, value))
                self.message = self.msg_fmt

class NotValidGitRepoException(GitBrancherException):
    def __init__(self, repo_path):
        msg = \
            "Git Repository not found under:  '{}'".format(
                repo_path)
        super(self.__class__, self).__init__(msg)

class CommandError(GitBrancherException):
    def __init__(self,msg):
        super(self.__class__, self).__init__(msg)
