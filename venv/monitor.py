from lxml import html
import requests
from .telegram import bot_send
import time

class CovidCaseMonitor:

    URL = 'https://www.worldometers.info/coronavirus/country/us/'
    STATE_NAME = 'MASSACHUSETTS'
    PERCENTAGE_CHANGE = 0.1
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36'
    }
    total_cases = 0

    def __init__(self):
        self.total_cases = int(self.get_total_cases())

    def get_total_cases(self):
        page = requests.get(self.URL, headers=self.headers)
        html_content = html.fromstring(page.content)

        # from bs4 import BeautifulSoup
        # soup = BeautifulSoup(full_page.content, 'html.parser')
        # result = soup.findAll("span", {"class": "my_span_class_name_1"})[0].text

        table = html_content.xpath("//table[@id='usa_table_countries_today']")[0]
        for tr in table.xpath(".//tr"):
            for td in tr.iterchildren():
                if self.STATE_NAME in td.text_content().upper():
                    total_cases = td.getnext().text_content()
                    total_cases = total_cases.strip().replace(',', '')
                    return int(total_cases)

        return None



    def update_total_cases(self):
        new_total_cases = self.get_total_cases()
        if new_total_cases is not None:
            self.total_cases = new_total_cases


    def report_total_case_change(self):
        prev_total_cases = self.total_cases
        self.update_total_cases()
        new_total_cases = self.total_cases

        if new_total_cases >= prev_total_cases + self.PERCENTAGE_CHANGE * prev_total_cases:
            message = "Significant increase in the number of positive tests for COVID-19 in {0}.\n" \
                      "The total number of cases: {1}. \n" \
                      "(Previous value: {2}) \n" \
                      "Checked at: {3}".format(self.STATE_NAME.capitalize(),
                                               new_total_cases,
                                               prev_total_cases,
                                               time.ctime())

            bot_send(message)
