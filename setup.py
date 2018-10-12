import setuptools
from setuptools_scm import get_version
from sphinx.setup_command import BuildDoc

cmdclass = {'build_sphinx': BuildDoc}

with open("README.rst", "r") as fh:
    long_description = fh.read()

project = "pyoneering"
release = get_version(root='.', relative_to=__file__)
version = '.'.join(release.split('.')[:2])

setuptools.setup(
    name=project,
    version=release,
    author="Fabian Haase",
    author_email="haase.fabian@gmail.com",
    description="Decorators for deprecating and refactoring",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(exclude=['tests*']),
    install_requires=['packaging'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",

        "License :: OSI Approved :: Apache Software License",

        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    command_options={
        'build_sphinx': {
            'project': ('setup.py', project),
            'version': ('setup.py', version),
            'release': ('setup.py', release),
            'source_dir': ('setup.py', 'docs')}},
)
