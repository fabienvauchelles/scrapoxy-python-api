try:
    from setuptools import setup, find_packages
except ImportError:
    from distutils.core import setup, find_packages


setup(
    name='scrapoxy',
    packages=find_packages(),
    install_requires=['requests'],
    version='1.9',
    description='Use Scrapoxy with Scrapy',
    author='Fabien Vauchelles',
    author_email='fabien@vauchelles.com',
    url='https://github.com/fabienvauchelles/scrapoxy-python-api',
    download_url='https://github.com/fabienvauchelles/scrapoxy-python-api/tarball/1.9',
    keywords=['crawler', 'crawling', 'scrapoxy', 'scrapy', 'scraper', 'scraping'],
    classifiers=[],
)
