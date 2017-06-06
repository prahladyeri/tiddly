from setuptools import setup, find_packages
setup(
    name="tiddly",
    version='1.0.7',
    packages=["tiddly"],#find_packages(),
	package_dir={'tiddly': ''},
    #scripts=['say_hello.py'],

    # Project uses reStructuredText, so ensure that the docutils get
    # installed or upgraded on the target machine
    install_requires=['flask','sqlalchemy'],

    package_data={
        # If any package contains *.txt or *.rst files, include them:
        #'': ['*.txt', '*.rst'],
        # And include any *.msg files found in the 'hello' package, too:
        # 'hello': ['*.msg'],
    },

    # metadata for upload to PyPI
    author="Prahlad Yeri",
    author_email="prahladyeri14@gmail.com",
    description="Flask-Tiddly is a minimal, prototype RESTful server for basic CRUD transactions.",
    license="MIT",
    keywords="flask rest server sqlalchemy",
    url="https://prahladyeri.github.io/flask-tiddly",  # project home page, if any

    # could also include long_description, download_url, classifiers, etc.
)