#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
    Setup file for pyfdm.

    This file was generated with PyScaffold 2.0.2, a tool that easily
    puts up a scaffold for your new Python project. Learn more under:
    http://pyscaffold.readthedocs.org/
"""

import inspect
import os
import re
import subprocess
import sys
from contextlib import contextmanager
from distutils.cmd import Command
from distutils.command.build import build as _build
from distutils.command.sdist import sdist as _sdist
from glob import glob

import setuptools
from setuptools import setup
from setuptools.command.test import test as TestCommand

# For Python 2/3 compatibility, pity we can't use six.moves here
try:  # try Python 3 imports first
    import configparser
    from io import StringIO
except ImportError:  # then fall back to Python 2
    import ConfigParser as configparser
    from StringIO import StringIO

__location__ = os.path.join(os.getcwd(), os.path.dirname(
    inspect.getfile(inspect.currentframe())))

# general settings
pyscaffold_version = "2.0.2"
package = "pyfdm"
namespace = []
root_pkg = namespace[0] if namespace else package
if namespace:
    pkg_path = os.path.join(*namespace[-1].split('.') + [package])
else:
    pkg_path = package

# Version configuration
versionfile_path = os.path.join(pkg_path, '_version.py')
tag_prefix = 'v'  # tags are like v1.2.0
short_version_py = """
# This file was generated by PyScaffold from the git
# revision-control system data, or from the parent directory name of an
# unpacked source archive. Distribution tarballs contain a pre-generated copy
# of this file.

version_version = '{version}'
version_full = '{full}'
def get_versions(default=dict(), verbose=False):
    return dict(version=version_version, full=version_full)
"""


class PyTest(TestCommand):
    user_options = [("cov=", None, "Run coverage"),
                    ("cov-report=", None, "Generate a coverage report"),
                    ("junitxml=", None, "Generate xml of test results")]

    def initialize_options(self):
        TestCommand.initialize_options(self)
        self.cov = None
        self.cov_report = None
        self.junitxml = None

    def finalize_options(self):
        TestCommand.finalize_options(self)
        if self.cov:
            self.cov = ["--cov", self.cov, "--cov-report", "term-missing"]
            if self.cov_report:
                self.cov.extend(["--cov-report", self.cov_report])
        if self.junitxml:
            self.junitxml = ["--junitxml", self.junitxml]

    def run_tests(self):
        try:
            import pytest
        except:
            raise RuntimeError("py.test is not installed, "
                               "run: pip install pytest")
        params = {"args": self.test_args}
        if self.cov:
            params["args"] += self.cov
            params["plugins"] = ["cov"]
        if self.junitxml:
            params["args"] += self.junitxml
        errno = pytest.main(**params)
        sys.exit(errno)


def sphinx_builder():
    try:
        from sphinx.setup_command import BuildDoc
    except ImportError:
        class NoSphinx(Command):
            user_options = []

            def initialize_options(self):
                raise RuntimeError("Sphinx documentation is not installed, "
                                   "run: pip install sphinx")

        return NoSphinx

    class BuildSphinxDocs(BuildDoc):

        def run(self):
            if self.builder == "doctest":
                import sphinx.ext.doctest as doctest
                # Capture the DocTestBuilder class in order to return the total
                # number of failures when exiting
                ref = capture_objs(doctest.DocTestBuilder)
                BuildDoc.run(self)
                errno = ref[-1].total_failures
                sys.exit(errno)
            else:
                BuildDoc.run(self)

    return BuildSphinxDocs


class ObjKeeper(type):
    instances = {}

    def __init__(cls, name, bases, dct):
        cls.instances[cls] = []

    def __call__(cls, *args, **kwargs):
        cls.instances[cls].append(super(ObjKeeper, cls).__call__(*args,
                                                                 **kwargs))
        return cls.instances[cls][-1]


def capture_objs(cls):
    from six import add_metaclass
    module = inspect.getmodule(cls)
    name = cls.__name__
    keeper_class = add_metaclass(ObjKeeper)(cls)
    setattr(module, name, keeper_class)
    cls = getattr(module, name)
    return keeper_class.instances[cls]


def get_install_requirements(path):
    content = open(os.path.join(__location__, path)).read()
    return [req for req in content.splitlines() if req != '']


def read(fname):
    with open(os.path.join(__location__, fname)) as fh:
        content = fh.read()
    # StringIO seems to expect a unicode object under Windows 7
    if sys.version_info[0] < 3:
        content = content.decode(encoding='utf8')
    return content


def str2bool(val):
    return val.lower() in ("yes", "true")


def read_setup_cfg():
    config = configparser.SafeConfigParser(allow_no_value=True)
    config_file = StringIO(read(os.path.join(__location__, 'setup.cfg')))
    config.readfp(config_file)
    metadata = dict(config.items('metadata'))
    classifiers = metadata.get('classifiers', '')
    metadata['classifiers'] = [item.strip() for item in classifiers.split(',')]
    console_scripts = dict(config.items('console_scripts'))
    console_scripts = prepare_console_scripts(console_scripts)
    include_package_data_bool = metadata.get('include_package_data', 'false')
    metadata['include_package_data'] = str2bool(include_package_data_bool)
    package_data = metadata.get('package_data', '')
    package_data = [item.strip() for item in package_data.split(',') if item]
    metadata['package_data'] = package_data
    data_files = metadata.get('data_files', '')
    data_files = [item.strip() for item in data_files.split(',')]
    data_files = [item for pattern in data_files for item in glob(pattern)]
    metadata['data_files'] = data_files
    return metadata, console_scripts


def prepare_console_scripts(dct):
    return ['{cmd} = {func}'.format(cmd=k, func=v) for k, v in dct.items()]


@contextmanager
def stash(filename):
    with open(filename) as fh:
        old_content = fh.read()
    try:
        yield
    finally:
        with open(filename, 'w') as fh:
            fh.write(old_content)


class ShellCommand(object):
    def __init__(self, command, shell=True, cwd=None):
        self._command = command
        self._shell = shell
        self._cwd = cwd

    def __call__(self, *args):
        command = "{cmd} {args}".format(cmd=self._command,
                                        args=subprocess.list2cmdline(args))
        output = subprocess.check_output(command,
                                         shell=self._shell,
                                         cwd=self._cwd,
                                         stderr=subprocess.STDOUT,
                                         universal_newlines=True)
        return self._yield_output(output)

    def _yield_output(self, msg):
        for line in msg.splitlines():
            yield line


def get_git_cmd(**args):
    if sys.platform == "win32":
        for cmd in ["git.cmd", "git.exe"]:
            git = ShellCommand(cmd, **args)
            try:
                git("--version")
            except (subprocess.CalledProcessError, OSError):
                continue
            return git
        return None
    else:
        git = ShellCommand("git", **args)
        try:
            git("--version")
        except (subprocess.CalledProcessError, OSError):
            return None
        return git


def version_from_git(tag_prefix, root, verbose=False):
    # this runs 'git' from the root of the source tree. This only gets called
    # if the git-archive 'subst' keywords were *not* expanded, and
    # _version.py hasn't already been rewritten with a short version string,
    # meaning we're inside a checked out source tree.
    git = get_git_cmd(cwd=root)
    if not git:
        if verbose:
            print("no git found")
        return None
    tag = next(git("describe", "--tags", "--dirty", "--always"))
    if not tag.startswith(tag_prefix):
        if verbose:
            print("tag '{}' doesn't start with prefix '{}'".format(tag,
                                                                   tag_prefix))
        return None
    tag = tag[len(tag_prefix):]
    sha1 = next(git("rev-parse", "HEAD"))
    full = sha1.strip()
    if tag.endswith("-dirty"):
        full += "-dirty"
    return {"version": tag, "full": full}


def get_keywords(versionfile_abs):
    # the code embedded in _version.py can just fetch the value of these
    # keywords. When used from setup.py, we don't want to import _version.py,
    # so we do it with a regexp instead. This function is not used from
    # _version.py.
    keywords = dict()
    try:
        with open(versionfile_abs, "r") as fh:
            for line in fh.readlines():
                if line.strip().startswith("git_refnames ="):
                    mo = re.search(r'=\s*"(.*)"', line)
                    if mo:
                        keywords["refnames"] = mo.group(1)
                if line.strip().startswith("git_full ="):
                    mo = re.search(r'=\s*"(.*)"', line)
                    if mo:
                        keywords["full"] = mo.group(1)
    except EnvironmentError:
        return None
    return keywords


def version_from_keywords(keywords, tag_prefix, verbose=False):
    if not keywords:
        return None  # keyword-finding function failed to find keywords
    refnames = keywords["refnames"].strip()
    if refnames.startswith("$Format"):
        if verbose:
            print("keywords are unexpanded, not using")
        return None  # unexpanded, so not in an unpacked git-archive tarball
    refs = set([r.strip() for r in refnames.strip("()").split(",")])
    # starting in git-1.8.3, tags are listed as "tag: foo-1.0" instead of
    # just "foo-1.0". If we see a "tag: " prefix, prefer those.
    TAG = "tag: "
    tags = set([r[len(TAG):] for r in refs if r.startswith(TAG)])
    if not tags:
        # Either we're using git < 1.8.3, or there really are no tags. We use
        # a heuristic: assume all version tags have a digit. The old git %d
        # expansion behaves like git log --decorate=short and strips out the
        # refs/heads/ and refs/tags/ prefixes that would let us distinguish
        # between branches and tags. By ignoring refnames without digits, we
        # filter out many common branch names like "release" and
        # "stabilization", as well as "HEAD" and "master".
        tags = set([r for r in refs if re.search(r'\d', r)])
        if verbose:
            print("discarding '%s', no digits" % ",".join(refs-tags))
    if verbose:
        print("likely tags: %s" % ",".join(sorted(tags)))
    for ref in sorted(tags):
        # sorting will prefer e.g. "2.0" over "2.0rc1"
        if ref.startswith(tag_prefix):
            r = ref[len(tag_prefix):]
            if verbose:
                print("picking %s" % r)
            return {"version": r,
                    "full": keywords["full"].strip()}
    else:
        if verbose:
            print("no suitable tags, using full revision id")
        return {"version": keywords["full"].strip(),
                "full": keywords["full"].strip()}


def version_from_file(filename):
    versions = dict()
    try:
        with open(filename) as fh:
            for line in fh.readlines():
                mo = re.match("version_version = '([^']+)'", line)
                if mo:
                    versions["version"] = mo.group(1)
                mo = re.match("version_full = '([^']+)'", line)
                if mo:
                    versions["full"] = mo.group(1)
    except EnvironmentError:
        return None

    return versions


def version_from_parentdir(parentdir_prefix, root, verbose=False):
    # Source tarballs conventionally unpack into a directory that includes
    # both the project name and a version string.
    dirname = os.path.basename(root)
    if not dirname.startswith(parentdir_prefix):
        if verbose:
            print("guessing rootdir is '%s', but '%s' doesn't start with "
                  "prefix '%s'" % (root, dirname, parentdir_prefix))
        return None
    version = dirname[len(parentdir_prefix):].split('-')[0]
    return {"version": version, "full": ""}


def git2pep440(ver_str):
    dash_count = ver_str.count('-')
    if dash_count == 0:
        return ver_str
    elif dash_count == 1:
        return ver_str.split('-')[0] + "+dirty"
    elif dash_count == 2:
        tag, commits, sha1 = ver_str.split('-')
        return "{}.post0.dev{}+{}".format(tag, commits, sha1)
    elif dash_count == 3:
        tag, commits, sha1, _ = ver_str.split('-')
        return "{}.post0.dev{}+{}.dirty".format(tag, commits, sha1)
    else:
        raise RuntimeError("Invalid version string")


def get_versions(verbose=False):
    versionfile_abs = os.path.join(__location__, versionfile_path)
    vcs_kwds = get_keywords(versionfile_abs)
    parentdir = package + '-'
    root = __location__

    # different version retrieval methods as (method, args, comment)
    ver_retrieval = [
        (version_from_keywords, (vcs_kwds, tag_prefix, verbose),
         "expanded keywords"),
        (version_from_file, (versionfile_abs,), "file"),
        (version_from_git, (tag_prefix, root, verbose), "git"),
        (version_from_parentdir, (parentdir, root, verbose), "parentdir")
    ]
    for method, args, comment in ver_retrieval:
        ver = method(*args)
        if ver:
            if verbose:
                print("got version from {}".format(comment))
            break
    else:
        ver = {"version": "unknown", "full": "unknown"}
    ver['version'] = git2pep440(ver['version'])
    return ver


class cmd_version(Command):
    description = "report generated version string"
    user_options = []
    boolean_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        ver = get_versions(verbose=True)["version"]
        print("Version: %s" % ver)


class cmd_build(_build):
    def run(self):
        versions = get_versions(verbose=True)
        _build.run(self)
        # now locate _version.py in the new build/ directory and replace it
        # with an updated value
        target_versionfile = os.path.join(self.build_lib,
                                          versionfile_path)
        print("updating {}...".format(target_versionfile))
        os.unlink(target_versionfile)
        with open(target_versionfile, "w") as fh:
            fh.write(short_version_py.format(**versions))


if 'cx_Freeze' in sys.modules:  # cx_freeze enabled?
    from cx_Freeze.dist import build_exe as _build_exe

    class cmd_build_exe(_build_exe):
        def run(self):
            versions = get_versions(verbose=True)
            with stash(versionfile_path):
                print("updating {}...".format(versionfile_path))
                with open(versionfile_path, 'w') as fh:
                    fh.write(short_version_py.format(**versions))
                _build_exe.run(self)


class cmd_sdist(_sdist):
    def run(self):
        versions = get_versions(verbose=True)
        self._generated_versions = versions
        # unless we update this, the command will keep using the old version
        self.distribution.metadata.version = versions["version"]
        return _sdist.run(self)

    def make_release_tree(self, base_dir, files):
        _sdist.make_release_tree(self, base_dir, files)
        # now locate _version.py in the new base_dir directory (remembering
        # that it may be a hardlink) and replace it with an updated value
        target_versionfile = os.path.join(base_dir, versionfile_path)
        print("updating {}...".format(target_versionfile))
        os.unlink(target_versionfile)
        with open(target_versionfile, "w") as fh:
            fh.write(short_version_py.format(**self._generated_versions))


def setup_package():
    # Assemble additional setup commands
    cmdclass = dict(docs=sphinx_builder(),
                    doctest=sphinx_builder(),
                    test=PyTest,
                    version=cmd_version,
                    sdist=cmd_sdist,
                    build=cmd_build)
    if 'cx_Freeze' in sys.modules:  # cx_freeze enabled?
        cmdclass['build_exe'] = cmd_build_exe
        del cmdclass['build']

    # Some helper variables
    version = get_versions()["version"]
    docs_path = os.path.join(__location__, "docs")
    docs_build_path = os.path.join(docs_path, "_build")
    install_reqs = get_install_requirements("requirements.txt")
    metadata, console_scripts = read_setup_cfg()

    command_options = {
        'docs': {'project': ('setup.py', package),
                 'version': ('setup.py', version.split('-', 1)[0]),
                 'release': ('setup.py', version),
                 'build_dir': ('setup.py', docs_build_path),
                 'config_dir': ('setup.py', docs_path),
                 'source_dir': ('setup.py', docs_path)},
        'doctest': {'project': ('setup.py', package),
                    'version': ('setup.py', version.split('-', 1)[0]),
                    'release': ('setup.py', version),
                    'build_dir': ('setup.py', docs_build_path),
                    'config_dir': ('setup.py', docs_path),
                    'source_dir': ('setup.py', docs_path),
                    'builder': ('setup.py', 'doctest')},
        'test': {'test_suite': ('setup.py', 'tests'),
                 'cov': ('setup.py', root_pkg)}}

    setup(name=package,
          version=version,
          url=metadata['url'],
          description=metadata['description'],
          author=metadata['author'],
          author_email=metadata['author_email'],
          license=metadata['license'],
          long_description=read('README.rst'),
          classifiers=metadata['classifiers'],
          test_suite='tests',
          packages=setuptools.find_packages(exclude=['tests', 'tests.*']),
          namespace_packages=namespace,
          install_requires=install_reqs,
          setup_requires=['six'],
          cmdclass=cmdclass,
          tests_require=['pytest-cov', 'pytest'],
          include_package_data=True,
          package_data={package: metadata['package_data']},
          data_files=[('.', metadata['data_files'])],
          command_options=command_options,
          entry_points={'console_scripts': console_scripts},
          zip_safe=False)  # do not zip egg file after setup.py install


if __name__ == "__main__":
    setup_package()
