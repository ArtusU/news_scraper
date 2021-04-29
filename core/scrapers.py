import datetime
from dateutil.relativedelta import relativedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from django.utils import timezone
from .models import NewsItem, ScrapeRecord

def scrape(url):
    options = webdriver.ChromeOptions()
    options.add_argument(" - incognito")
    
    browser = webdriver.Chrome(
        executable_path='./chromedriver', chrome_options=options)

    browser.get(url)

    timeout = 10

    try:
        WebDriverWait(browser, timeout).until(
            EC.visibility_of_element_located(
                (By.XPATH,
                 "//div[@class='crayons-story__body']")
            )
        )
    except TimeoutException:
        print("Timed out waiting for page to load")
        browser.quit()

    
    try:

        record = ScrapeRecord.objects.create(
            finish_time=timezone.now()
        )
        article_elements = browser.find_elements_by_xpath(
        "//div[@class='crayons-story__body']")

        for article in article_elements:
            if article.get_attribute('data-content-user-id') != "undefined":

                # try get the anchor tag and href
                result = article.find_element_by_xpath(
                    ".//a[@class='crayons-story__tertiary fs-xs']")
                news_item_link = result.get_attribute('href')

                # try get title
                title_result = article.find_element_by_xpath(
                    ".//h3[@class='crayons-story__title']")
                news_item_title = title_result.text

                # # try get timestamp
                two_years_ago = datetime.date.today() - relativedelta(year=2)
                timestamp_result = article.find_element_by_tag_name('time')
                news_item_time = timestamp_result.text

                # convert the news_item_time into python date object
                if "'" in news_item_time:
                    # parse the year
                    new_item_date = datetime.datetime.strptime(
                        news_item_time, "%b %d '%y").date()

                else:
                    # the year is the current year
                    new_item_date = datetime.datetime.strptime(
                        news_item_time, "%b %d")
                    today = datetime.date.today()
                    new_item_date = new_item_date.replace(
                        year=today.year).date()

                if new_item_date > two_years_ago:
                    NewsItem.objects.get_or_create(
                            title=news_item_title,
                            link=news_item_link,
                            source='Dev.to',
                            publish_date=new_item_date
                        )
                        
        record.finish_time = timezone.now()
        record.finished = True
        record.save()


    except:
        pass
        