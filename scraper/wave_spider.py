from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

import pymongo
import time


class WaveSpider:

    def __init__(self):
        # launch the web browser
        self.url = ''
        # headless chrome and chrome options
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.set_headless()
        self.driver = webdriver.Chrome(options=self.chrome_options)
        self.driver.get(self.url)
        # login to the wave contact lens website
        self.login_element = self.driver.find_element_by_id("TextBoxUserId").send_keys("")
        self.login_element = self.driver.find_element_by_id("TextBoxPassword").send_keys("")
        time.sleep(2)
        self.driver.find_element_by_id("ButtonLogin").click()

    def data_extraction(self):
        """
        extracts data and returns it as a dict
        :return: collect dict
        """
        n = [num for num in range(3, 23)]
        # crawk depths and element depth
        page_depth = 4
        next_element = 2
        element_depth = 3
        # pause the script to give the DOM enough time to load the elements
        time.sleep(15)
        while page_depth >= next_element:
            while len(n) > element_depth:
                # grab the table header
                header = self.driver.find_elements_by_css_selector(
                    '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody '
                    '> tr:nth-child(2) > td')
                # grab the entire row
                table_element = self.driver.find_elements_by_css_selector(
                    '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody > tr:nth-child('
                    + str(element_depth) + ') > td')
                # loop through the row and get all elements.
                # you can setup some conditional statements to filter out the ones you dont need
                for c_name, item in zip(header, table_element):
                    print(c_name.text, item.text)

                # completes the element loop
                element_depth = element_depth + 1
            # get the next page element and add the value from the next element
            # there is a way to make this more dynamic as the pagination grows
            next = self.driver.find_element_by_css_selector(
                '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody > '
                'tr:nth-child(1) > td > a:nth-child(' + str(next_element) + ')')
            next_element = next_element + 1
            element_depth = 3
            # click to go to the next page
            next.click()
            # pause the script to allow the DOM to load
            time.sleep(20)

        self.driver.close()


    def mongo_connection(self):
        """
        connect to mongo db and select database and collections

        """
        try:
            self.myclient = pymongo.MongoClient("mongodb://localhost:27017")
        except Exception as e:
            print(e)

        #set database and collection
        self.mydb = self.myclient["waveOrderData"]
        self.mycol = self.mydb["waveOrders"]


    def update_collection(self, collect):
        """
        updates the mondo collection
        :param collect: dict
        """
        self.mycol.replace_one(
            {"order_id": collect.get('Order ID')},
            collect,
            True
        )

    def mongo_close(self):
        """
        close mongodb connection
        """
        self.myclient.close()



def main():

    crawler = WaveSpider()
    crawler.data_extraction()
    # crawler.mongo_connection()
    # crawler.update_collection(data)
    # crawler.mongo_close()

if __name__=='__main__':
    main()