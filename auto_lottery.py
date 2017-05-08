"""Automated script to enter the hamilton lottery daily."""

import os
import sys
import time
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
CURRENT_HOME = os.path.dirname(os.path.realpath(__file__))
CHROME_DRIVER_LOCATION =  os.environ.get("CHROME_DRIVER", '~/.virtualenvs/hammy/bin/chromedriver')

PHANTOM_JS_PATH = os.path.join(CURRENT_HOME, 'phantomjs')
sys.path.append(PHANTOM_JS_PATH)
os.environ['PATH'] =  PHANTOM_JS_PATH + ":" + os.environ['PATH']

# where to print logfile
LOGFILE = "/tmp/logfile"

# where the magic happens
LOTTERY_URL = "http://www.luckyseat.com/hamilton.html"
THANKYOU_URL = "http://www.luckyseat.com/thankyou.html"
THANKYOU_URL_2 ="http://www.luckyseat.com/hamilton-thankyou.html"

# basic input format
XPATH_FORMAT = "//input[@leadfield='{}']"

DEBUG_MODE = False
SLEEP_DELAY = 10

# the field identifiers and the values that go with them
# sensitive info is stored in environment. 
values_by_leadfield = {
    'firstname': os.environ['FNAME'],
    'lastname': os.environ['LNAME'],
    'emailaddress1': os.environ['EMAIL'],
    'address1_postalcode': os.environ['ZIPCODE']
}
age = os.environ['AGE']
phone_number = os.environ.get('PHONE', None) # optional
if phone_number:
    values_by_leadfield['mobilephone'] = phone_number
num_tickets =  os.environ.get('NUMTICKETS', 1) # optional


def print_log(message):
    """Print message to the log file."""

    lfile = open(LOGFILE, 'a')
    lfile.write('{}\n'.format(message))
    lfile.close()

def lambda_handler(event, context):
    try:
        return enter_lottery()
    except Exception as e:
        return e

def enter_lottery():
    """Open the web page for the hamilton lottery and enter."""

    # create selenium driver and point to lottery page
    if not DEBUG_MODE:
        print "USING PHANTOMJS"
        driver = webdriver.PhantomJS(executable_path=PHANTOM_JS_PATH, service_log_path='/tmp/output.log')
        driver.set_window_size(1120, 600)
    else:
        driver = webdriver.Chrome(CHROME_DRIVER_LOCATION)
    driver.get(LOTTERY_URL)
    if DEBUG_MODE:
        time.sleep(SLEEP_DELAY)

    # get the performance for which we're entering
    perf = driver.find_element_by_xpath('//h1[2]').text.split('\n')[0]
    if DEBUG_MODE:
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
        contactname = field.get_attribute('contactfield')
        if fieldname in values_by_leadfield:
            field.send_keys(values_by_leadfield[fieldname])
        elif contactname in values_by_leadfield:
            field.send_keys(values_by_leadfield[contactname])


    # find the radio buttons. Expecting two: one for 1 ticket, and one for 2 tix
    radios = driver.find_elements_by_xpath("//input[@type='radio']")
    if len(radios) != 2:
        # exit, but don't close driver so it can be inspected
        print_log("ERROR: did not find exactly two radio buttons. Exiting.")
        return False

    # otherwise, click on a random radio button for 1 or 2 tickets
    if num_tickets == '2':
        radios[1].click()
    else:
        radios[0].click()

    # age is now required and uses this unique id
    age_field = driver.find_elements_by_xpath("//input[@id='f_4faa5fcc8903e71181005065f38a5961']")[0]
    age_field.send_keys(age)

    # check both social media share check boxes to increase odds
    checkboxes = driver.find_elements_by_xpath("//input[@type='checkbox']")
    for checkbox in checkboxes:
        checkbox.click()

    # slide the lock thingy
    lock = driver.find_element_by_id('Slider')

    actions = ActionChains(driver)
    actions.move_to_element(lock)
    actions.drag_and_drop_by_offset(lock, 200, 0)
    actions.perform()

    if DEBUG_MODE:
        time.sleep(SLEEP_DELAY)

    if not DEBUG_MODE:
        # submit the form
        sub = driver.find_element_by_id('btnSubmit')
        sub.click()

    # check and see whether it has the thank you form up
    if driver.current_url not in [THANKYOU_URL, THANKYOU_URL_2]:
        print_log('ERROR: did not display thank you page. Exiting.')
        return False

    # if we got here...
    if DEBUG_MODE:
        print_log('Successfully entered lottery!')

    driver.close()
    return True

if __name__ == '__main__':
    from sys import argv
    if len(argv) == 2 and argv[1] in  ['-d', '--debug']:
        DEBUG_MODE = True

    print_log('*****{}'.format(datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')))
    enter_lottery()