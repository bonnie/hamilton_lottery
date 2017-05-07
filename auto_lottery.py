"""Automated script to enter the hamilton lottery daily."""

import os
import sys
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
PROJECT_HOME = os.environ.get('HAMILTON_LOTTERY_HOME', "~/src/hamilton/")

# where to print logfile
LOGFILE = os.path.join(PROJECT_HOME, "logfile")

# where the magic happens
LOTTERY_URL = "http://www.luckyseat.com/hamilton.html"
THANKYOU_URL = "http://www.luckyseat.com/thankyou.html"

# basic input format
XPATH_FORMAT = "//input[@leadfield='{}']"

# the field identifiers and the values that go with them
# sensitive info is stored in environment. 
values_by_leadfield = {
    'firstname': os.environ['FNAME'],
    'lastname': os.environ['LNAME'],
    'emailaddress1': os.environ['EMAIL'],
    'address1_postalcode': os.environ['ZIP']
}
num_tickets =  os.environ.get('NUMTICKETS', 1), # optional

def print_log(message):
    """Print message to the log file."""

    lfile = open(LOGFILE, 'a')
    lfile.write('{}\n'.format(message))
    lfile.close()


def enter_lottery():
    """Open the web page for the hamilton lottery and enter."""

    # create selenium driver and point to lottery page
    driver = webdriver.Firefox()
    driver.get(LOTTERY_URL)

    # get the performance for which we're entering
    perf = driver.find_element_by_xpath('//h1[2]').text.split('\n')[0]
    print_log(perf)

    # get the iframe source and load it
    fc = driver.find_element_by_id('frame-container')
    iframe = fc.find_element_by_tag_name('iframe')
    iframe_src = iframe.get_attribute('src')
    driver.get(iframe_src)

    # fill out the text inputs
    inputs = driver.find_elements_by_tag_name('input')
    for field in inputs:
        fieldname = field.get_attribute('leadfield')
        if fieldname in values_by_leadfield:
            field.send_keys(values_by_leadfield[fieldname])

    # find the radio buttons. Expecting two: one for 1 ticket, and one for 2 tix
    radios = driver.find_elements_by_xpath("//input[@type='radio']")
    if len(radios) != 2:
        # exit, but don't close driver so it can be inspected
        print_log("ERROR: did not find exactly two radio buttons. Exiting.")
        sys.exit()

    # otherwise, click on a random radio button for 1 or 2 tickets
    if num_tickets == 2:
        radios[1].click()
    else:
        radios[0].click()

    # slide the lock thingy
    lock = driver.find_element_by_id('Slider')

    actions = ActionChains(driver)
    actions.move_to_element(lock)
    actions.drag_and_drop_by_offset(lock, 200, 0)
    actions.perform()

    # submit the form
    sub = driver.find_element_by_id('btnSubmit')
    sub.click()

    # check and see whether it has the thank you form up
    if driver.current_url != THANKYOU_URL:
        print_log('ERROR: did not display thank you page. Exiting.')
        sys.exit()

    # if we got here...
    print_log('Successfully entered lottery!')

    driver.close()


if __name__ == '__main__':

    print_log('*****{}'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
    enter_lottery()