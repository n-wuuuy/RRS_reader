from setuptools import setup

setup(
    name='rss-reader',
    version='2.0',
    packages=['scripts'],
    python_requires='>=3.10',
    install_requires=[
        'feedparser', 'requests', 'bs4',
    ],
    include_package_data=True,
    entry_points={
        'console_scripts': [
            'rss-reader = scripts.rss_reader:run'
        ]
    }
)