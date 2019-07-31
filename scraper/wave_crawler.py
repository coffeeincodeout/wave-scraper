from selenium import webdriver

import time

driver = webdriver.Chrome()
url = 'https://www.wavecontactlenses.com/waveioss/'
driver.get(url)
time.sleep(2)
login_element = driver.find_element_by_id("TextBoxUserId").send_keys("wavetestlab")
time.sleep(1)
login_element = driver.find_element_by_id("TextBoxPassword").send_keys("XCEL0009")
time.sleep(2)
driver.find_element_by_id("ButtonLogin").click()

# grab the numbers in the navigation and out put the text
pagination = driver.find_element_by_css_selector(
    '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody > tr:nth-child(1)').text
time.sleep(5)

# number of pages to crawl plus 1 so ensure final page is grabbed
page_depth = len(pagination.split(" ")) + 1
# starting point on the navigation
next_element = 2
# number of elements on a page
element_depth = 3

# pause the script to give the DOM enough time to load the elements
# this can be adjusted just make sure there is enough time for all elements to load
time.sleep(10)
while page_depth >= next_element:
    # get the number of rows on a page
    row = driver.find_elements_by_link_text("More...")
    # get the row length and add 3 since the first row to scrape begins at 3
    row_depth = len(row) + 3
    while row_depth > element_depth:
        # grab the table header
        header = driver.find_elements_by_css_selector(
            '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody '
            '> tr:nth-child(2) > td')
        # grab the entire row
        table_element = driver.find_elements_by_css_selector(
            '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody > tr:nth-child('
            + str(element_depth) + ') > td')
        # loop through the row and get all elements.
        # you can setup some conditional statements to filter out the ones you dont need
        # you can add to database connection to add to collection.
        for c_name, item in zip(header, table_element):
            print(c_name.text, item.text)

        # completes the element loop
        element_depth = element_depth + 1
    # conditional to determine if the crawl is complete
    if page_depth == next_element:
        # break out of loop there is no more pages to crawl
        print("Scraping complete")
        break
    else:
        time.sleep(4)
        # get the next page element and add the value from the next element
        next = driver.find_element_by_css_selector(
            '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody > '
            'tr:nth-child(1) > td > a:nth-child(' + str(next_element) + ')')
        # increment next element
        next_element = next_element + 1
        # resets the element depth
        element_depth = 3
        # click to go to the next page
        next.click()
        # pause the script to allow the DOM to load
        time.sleep(10)

# close chrome driver once crawl is complete.
driver.close()


