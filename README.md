# Git Brancher

Small project to list repositories that contains specified by regex branch.

The list of repositories needs to be provided as input file - one line per
repository.

Regex is specified as CLI parameter.


# Install
Installation may be done using virtual environment

```
virtualenv git_brancher
. git_brancher/bin/activate
python setup.py install
```


# Run

First, create a file that will include list of repositories (anonymous access)

```
vi /tmp/list_of_repositories


https://github.com/openstack/nova/
git@github.com:openstack/neutron.git
```

Then use gitbrancher from previously created virtualenv:

```
gitbrancher -f /tmp/list_of_repositories -b "my*branc?"
```
