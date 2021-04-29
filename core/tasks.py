from celery import shared_task
from newsscraper.celery import app

from .scrapers import scrape

URL = 'https://dev.to/search?q=django'

@app.task
def scrape_dev_to():
    scrape(URL)
    return


@shared_task
def scrape_async():
    scrape(URL)
    return