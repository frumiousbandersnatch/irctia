from setuptools import setup, find_packages

setup(
    name = 'irctia',
    version = '0.0',
    packages = find_packages(),
    install_requires = [
        'Click',
        'sqlalchemy',
    ],
    entry_points = '''
    [console_scripts]
    irctia-weechat = irctia.weechatlog:backfill
    irctia-joins = irctia.queries:joins
    irctia-trail = irctia.queries:trail
    ''',
)
# fixme: turn these single-command entries into one grouped main
