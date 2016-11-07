#!/usr/bin/env python

import logging
from cli import logger
from cli import gitrepo
from cli import exceptions

import argparse
import git
import re
import sys

from urlparse import urlparse

LOG = logger.LOG

# prefix to distinguish branch from other refs
BRANCH_PREFIX='refs/heads/'

def _git_get_branches(url, regex='*'):
    '''Gets repositories with branches that matches regex.

    :param url: git url 
    :param regex: regex used to filter out branches for a given url
                  if no regex is specified all branches are returned

    :returns: GitRepo object with branches, only if git repo contains regex
              branch(es)
    '''

    git_repo = None

    branch_regex = BRANCH_PREFIX + regex

    # gitpython does not support ls-remote, we need to fall back to
    # ls_remote from git.cmd.Git()
    try:
        branches = git.cmd.Git().ls_remote(url, branch_regex)
        git_repo = gitrepo.GitRepo(url)
        if branches and len(branches) > 0:
            for branch in git.cmd.Git().ls_remote(url, branch_regex).split('\n'):
                hash_branch = branch.split('\t')
                git_repo.add_branch(hash_branch[1][len(BRANCH_PREFIX):],
                  hash_branch[0])
        else:
            return None
    except Exception as err:
        LOG.error("Could not read from git repository: %s" % url.strip())
        LOG.error(str(err))
        pass

    return git_repo


class GitBrancherShell(object):

    def __init__(self):
        pass

    def get_base_parser(self):
        parser = argparse.ArgumentParser(
                                         prog='gitbrancher',
                                         description='Git Brancher CLI.',
                                         add_help=False
        )


        parser.add_argument('-?', '-h' , '--help',
                            action='help',
                            help='show this help message and exit',
        )


        parser.add_argument('-v', '--verbose',
                            action='store_true',
                            help='increase output verbosity',
        )


        parser.add_argument('-f', '--file',
                            help='file path argument',
        )

        parser.add_argument('-b', '--branch',
                            help='branch regex',
        )

        return parser

    def parse_args(self, argv):
        parser = self.get_base_parser()
        args = parser.parse_args(argv)

        if args.verbose:
            LOG.setLevel(level=logging.DEBUG)
            LOG.debug('GitBrancherShell running in debug mode')

        if not args.file:
            raise exceptions.CommandError("You must provide file path, "
                                   "via -f or via --file argument ")
        else:
            LOG.debug('File path: %s' % args.file)

        if not args.branch:
            raise exceptions.CommandError("You must provide branch regex, "
                                   "via -b or via --branch argument ")
        else:
            LOG.debug('Branch regex: %s' % args.branch)

        return args


    def main(self, argv):
        args = self.parse_args(argv)

        repos = []
        repos_from_file = []

        with open(args.file) as f:
            for line in f:
                repos_from_file.append(line)

        for repo_url in repos_from_file:
            repo_url = repo_url.strip()
            if repo_url and len(repo_url) > 1:
                LOG.debug("Checking git repository: %s" % repo_url)
                gitrepo = _git_get_branches(repo_url, regex=args.branch)
                if gitrepo:
                    repos.append(gitrepo)

        for repo in repos:
            print repo.url

def main(args=None):
    try:
        if args is None:
            args = sys.argv[1:]

        GitBrancherShell().main(args)

    except Exception as e:
        raise
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)

if __name__ == "__main__":
    main()

