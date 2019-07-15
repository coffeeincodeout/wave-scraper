from selenium import webdriver

import time

driver = webdriver.Chrome()
url = 'https://www.wavecontactlenses.com/waveioss/'
driver.get(url)
time.sleep(2)
login_element = driver.find_element_by_id("TextBoxUserId").send_keys("")
time.sleep(1)
login_element = driver.find_element_by_id("TextBoxPassword").send_keys("")
time.sleep(2)
driver.find_element_by_id("ButtonLogin").click()

# used to loop through the number of table elements
n = [num for num in range(3,23)]
# crawk depths and element depth
page_depth = 4
next_element = 2
element_depth = 3
# pause the script to give the DOM enough time to load the elements
time.sleep(15)
while page_depth >= next_element:
    while len(n) > element_depth:
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
        for c_name, item in zip(header, table_element):
            print(c_name.text, item.text)


        # completes the element loop
        element_depth = element_depth + 1
    # get the next page element and add the value from the next element
    # there is a way to make this more dynamic as the pagination grows
    next = driver.find_element_by_css_selector(
                '#ctl00_ContentPlaceHolder1_TabControl1_ViewRecords1_OrderStatus1_DataGrid1 > tbody > '
                'tr:nth-child(1) > td > a:nth-child(' + str(next_element)+ ')')
    next_element = next_element + 1
    element_depth = 3
    # click to go to the next page
    next.click()
    # pause the script to allow the DOM to load
    time.sleep(15)

driver.close()
