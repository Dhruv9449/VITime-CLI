from setuptools import setup
from VITimeCLI.initialize import __version__


with open("README.md") as r:
    Long_desc = "\n" + r.read()



setup(
    name = 'vitime',
    version = __version__,
    description = 'VITime app for storing and displaying VIT timetabe',
    long_description_content_type = "text/markdown",
    long_description = Long_desc,
    author = 'Dhruv Shah',
    author_email = 'dhruvshahrds@gmail.com',
    url = "https://github.com/Dhruv9449/VITime-CLI",
    project_urls = {
                    'Source' : 'https://github.com/Dhruv9449/VITime-CLI',
                    'Bug Tracker': 'https://github.com/Dhruv9449/VITime-CLI/issues'
                    },
    packages = ['VITimeCLI'],
    include_package_data = True,
    install_requires = ['click','pyperclip'],
    classifiers = [
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Education',
            'Programming Language :: Python :: 3',
            'Operating System :: OS Independent',
            'License :: OSI Approved :: MIT License'
            ],
    license = 'MIT',
    entry_points = '''
    [console_scripts]
    vitime = VITimeCLI.main:vitime
    '''
)
