#/usr/bin/python

from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import time
import sys

###
# requirements:
# pip install selenium webdriver
#
# to sound a bell, it detects an open slot, invoke it with:
# python covidbot.py && echo \a
#
# to send a text message on MacOS, invoke it with:
# python covidbot.py && osascript text.scpt [imessage_number] "`date`: VACCINE POSSIBLY AVAILABLE at https://bit.ly/3r0Etbk"
###

now = datetime.now()
current_time = now.strftime("%H:%M:%S")
print("🚦 Started at", current_time)

browser = webdriver.Chrome(ChromeDriverManager().install())

# takes a little while to load the iframe with client side js so wait up to 20 seconds
browser.implicitly_wait(10)

while True: # exits when we get a hit

    try: # ignore exceptions, just keep going

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        print("🔎 Checking at", current_time)

        try:
            browser.get('https://www.eventbrite.com/e/ucsf-health-covid-19-vaccination-drive-through-clinic-for-age-65-and-over-registration-137488823773')
            # browser.get('https://www.eventbrite.com/e/trivia-d-recurring-event-tickets-134426728965')

        except Exception:
            # restart browser if it dies
            print("Couldn't get web page, reinvoking browser")

            browser = webdriver.Chrome(ChromeDriverManager().install())
            browser.implicitly_wait(10)

        # --- daytime mode (when it's all Sales Ended)
        # try:
        #     sales_ended_text = browser.find_element_by_css_selector('#event-page > main > div.js-hidden-when-expired.event-listing.event-listing--has-image > div.g-grid.g-grid--page-margin-manual > div > div.listing-panel-wrapper.js-listing-panel-wrapper.clrfix > div.listing-panel.js-sticky-panel.sticky-listing-panel.sticky.clrfix > div > div.g-cell.g-cell-1-1.g-cell-lg-5-12.listing-panel__g-cell > div > div > div').text

        #     print("Availability text = '" + sales_ended_text +"'")
        #     if(sales_ended_text != "Sales Ended" and sales_ended_text != ""):
        #         print("✅ GET TICKETS NOW!")
        #         # browser.quit()
        #         sys.exit(0)

        # except Exception:
        #     # ignore element missing
        #     print("Couldn't find availability text element, so retrying...")

        #     pass

        # --- end daytime mode

        # click the button to list events, if it exists (if not,)
        try:
            browser.find_element_by_id('eventbrite-widget-modal-trigger-137488823773').click()

            try:
                # browser.find_element_by_id('eventbrite-widget-modal-trigger-134426728965').click()
                browser.switch_to.frame(browser.find_element_by_tag_name('iframe'))

                # check the text of the first event groupd button in the list to see if it says Register or Sold Out
                sold_out_text = browser.find_element_by_css_selector('#root > div > div > div > div.eds-collapsible-pane-layout > div.eds-collapsible-pane-layout__content.eds-collapsible-pane-layout__content--has-pane > div > main > div > div.eds-modal__content__children > div > div.series-events-container > div > ul > li > div > div > div.eds-g-cell.eds-g-cell-6-12.eds-text--right.eds-l-mar-top-5 > div > button').text

                print("First button text: " + sold_out_text)

                # if (sold_out_text == "Sold Out"):
                #     print("TOUGH LUCK")

                if(sold_out_text == "Register"):
                    print("✅ GET TICKETS NOW!")
                    # browser.quit()

                    # click on the register button then quit without killing browser
                    # #root > div > div > div > div.eds-collapsible-pane-layout > div.eds-collapsible-pane-layout__content.eds-collapsible-pane-layout__content--has-pane > div > main > div > div.eds-modal__content__children > div > div.series-events-container > div > ul > li:nth-child(1) > div > div > div.eds-g-cell.eds-g-cell-6-12.eds-text--right.eds-l-mar-top-5 > div > button

                    sys.exit(0)

            except Exception:
                print("Couldn't find first button, ignoring")

            try:
                # check second Register button in the list in case the first one still exists and is Sold Out
                sold_out_text = browser.find_element_by_css_selector('#root > div > div > div > div.eds-collapsible-pane-layout > div.eds-collapsible-pane-layout__content.eds-collapsible-pane-layout__content--has-pane > div > main > div > div.eds-modal__content__children > div > div.series-events-container > div > ul > li:nth-child(2) > div > div > div.eds-g-cell.eds-g-cell-6-12.eds-text--right.eds-l-mar-top-5 > div:nth-child(1) > button').text

                print("Second button text (if available): " + sold_out_text)

                if(sold_out_text == "Register"):
                    print("✅ GET TICKETS NOW!")
                    # browser.quit()

                    # click on the register button then quit without killing browser
                    # #root > div > div > div > div.eds-collapsible-pane-layout > div.eds-collapsible-pane-layout__content.eds-collapsible-pane-layout__content--has-pane > div > main > div > div.eds-modal__content__children > div > div.series-events-container > div > ul > li:nth-child(2) > div > div > div.eds-g-cell.eds-g-cell-6-12.eds-text--right.eds-l-mar-top-5 > div > button
                    sys.exit(0)

            except Exception:
                print("Couldn't find second button, ignoring")

        except Exception:
            print("Couldn't find events button, retrying in a few seconds")

        time.sleep(30)

        # needs you to go to another site in order to refresh
        browser.get('http://google.com')

    except Exception:
        # ignore element missing
        print("Browser probably died, retrying...")

        pass