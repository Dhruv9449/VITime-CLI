from setuptools import setup

setup(
    name = 'vitime',
    version = '0.0.1',
    description = 'VITime app for storing and displaying VIT timetabe',
    author = 'Dhruv Shah',
    author_email = 'dhruvshahrds@gmail.com',
    packages = ['VITimeCLI'],
    include_package_data = True,
    install_requires = ['click'],
    entry_points = '''
    [console_scripts]
    vitime = VITimeCLI.main:vitime
    '''
)
