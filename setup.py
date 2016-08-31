from setuptools import setup

setup(
    name='luck',
    version='1.0',
    py_modules=['luck'],
    install_requires=[
        'Click',
        'yahoo_oauth',
        'lxml',
        'BeautifulSoup4'
    ],
    entry_points='''
        [console_scripts]
        luck=luck:luck
    ''',
)
