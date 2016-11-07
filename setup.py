import os
from os.path import join, dirname, abspath
from pip import req
import platform
from setuptools import setup, find_packages

import cli

# parse_requirements() returns generator of pip.req.InstallRequirement objects
install_reqs = req.parse_requirements('requirements.txt', session=False)

# reqs is a list of requirement
# e.g. ['django==1.5.1', 'mezzanine==1.4.6']
reqs = [str(gitbrancher.req) for gitbrancher in install_reqs]

prj_dir = dirname(abspath(__file__))
setup(
    name='git_brancher',
    version=cli.__VERSION__,
    packages=find_packages(),
    long_description=open(join(prj_dir, 'README.md')).read(),
    entry_points={
        'console_scripts': [ 'gitbrancher = cli.git_brancher:main' ]
    },
    install_requires=reqs,
    author='Michal Pryc',
    author_email='mpryc@redhat.com'
)

if all(platform.linux_distribution(supported_dists="redhat")):
    # For RedHat based systems, get selinux binding
    try:
        import selinux
    except ImportError as e:
        new_error = type(e)(e.message + ". check that 'python-libselinux is "
                                        "installed'")
        import sys
        import shutil
        from distutils import sysconfig

        if hasattr(sys, 'real_prefix'):
            # check for venv
            VENV_SITE = sysconfig.get_python_lib()
            SELINUX_PATH = os.path.join(
                sysconfig.get_python_lib(plat_specific=True,
                                         prefix=sys.real_prefix),
                "selinux")
            if not os.path.exists(SELINUX_PATH):
                raise new_error

            # filter precompiled files
            files = [os.path.join(SELINUX_PATH, f)
                     for f in os.listdir(SELINUX_PATH)
                     if not os.path.splitext(f)[1] in (".pyc", ".pyo")]

            # add extra file for (libselinux-python-2.5-9.fc24.x86_64)
            _selinux_file = os.path.join(
                sysconfig.get_python_lib(plat_specific=True,
                                         prefix=sys.real_prefix),
                "_selinux.so")
            if os.path.exists(_selinux_file):
                files.append(_selinux_file)

            dest = os.path.join(VENV_SITE, "selinux")
            os.makedirs(dest)
            for f in files:
                shutil.copy(f, dest)
        else:
            raise new_error
        import selinux  # noqa
