from configparser import ConfigParser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from time import sleep
import vlc


# Initialize
browser = webdriver.Chrome('chromedriver.exe')
config = ConfigParser()
playsound = vlc.MediaPlayer('audio.mp3')
tcf_exams = ['TCF SO', 'TCF Canada', 'TCF dans le cadre de la DAP']
td_count = []
fc_mor_count = []

browser.maximize_window()
config.read('settings.ini')

# User settings
username = config['YBotConfiguration']['Username']
password = config['YBotConfiguration']['Password']

# Change index (tcf_exams[index]) to correct exam type
# 0 (TCF SO)
# 1 (TCF Canada)
# 2 (TCF dans le cadre de la DAP)
# By default is 0
tcf_exam_type = tcf_exams[int(config['YBotConfiguration']['TcfType'])]

# Change index (region = "index") to correct region
# "1" Alger (Antenne préférée)
# "3" Antenne d'Annaba
# "4" Antenne de Constantine
# By default is "1" (Alger)
region = config['YBotConfiguration']['Region']

# Change index (motivation = "index") to correct motivation
# "1" Etudes en France
# "3" Immigration au Canada
# "4" Procédure de naturalisation
# "5" Autre
# By default is "1" (Etudes en France)
motivation = config['YBotConfiguration']['Motivation']

# Change max month to serch for (Example curranate month is "September" to 2 "October")
max_month = int(config['YBotConfiguration']['MaxMonth'])

def login():
    try:
        # Get login page
        browser.get('https://portail.if-algerie.com/login')
        email_field = browser.find_element_by_name('email')
        password_field = browser.find_element_by_name('password')
        submit_button = browser.find_element_by_id('login')
        # Login process
        email_field.send_keys(username)
        password_field.send_keys(password)
        submit_button.click()
        WebDriverWait(browser, 30).until(EC.url_changes(browser.current_url))
        # Get exams appointments page
        browser.get('https://portail.if-algerie.com/exams')
        # Failed to login try again
        if browser.current_url != 'https://portail.if-algerie.com/exams': login()
    except: pass

def registering(a, tcf_type):
    # Get active FC and correct test selected
    if a.get_attribute('class') == 'fc-day-grid-event fc-h-event fc-event fc-start fc-end bg-secondary':
        return False
    if tcf_type.text == tcf_exam_type:
        # Open date modal
        a.click()
        sleep(1)
        exams_modal = browser.find_element_by_id('exams-modal')
        payment_day = exams_modal.find_element_by_id('paymentDay')
        close_exam_button = exams_modal.find_element_by_css_selector('button.btn.btn-default.waves-effect')
        # Check if payment day is disabled
        if payment_day.get_property('disabled'):
            browser.execute_script("arguments[0].click();", close_exam_button)
            return False
        select_motivation = exams_modal.find_element_by_id('motivation')
        submit_exam_button = exams_modal.find_element_by_id('submitExam')
        playsound.play()
        try:
            # Send date and submit
            Select(select_motivation).select_by_value(motivation)
            payment_day.click()
            sleep(1)
            # Pick an available date (Not tested yet)
            calendar = browser.find_element_by_css_selector('div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-top')
            days_active = calendar.find_elements_by_css_selector('td.day.active')
            browser.execute_script("arguments[0].click();", days_active[0]) # 0 First day available
            sleep(1)
            periods = browser.find_element_by_id('periods')
            options = periods.find_elements_by_tag_name('option')
            max_period_value = options[-1].get_attribute('value') # -1 Last period available
            Select(periods).select_by_value(max_period_value)
            browser.execute_script("arguments[0].click();", submit_exam_button)
            return True
        except:
            return False

login()

# Search for available appointment
while True:
    try:
        browser.refresh()
        # Check if system kick you out
        if browser.current_url != 'https://portail.if-algerie.com/exams': browser.get('https://portail.if-algerie.com/exams')
        if browser.current_url == 'https://portail.if-algerie.com/login': login()
        select_region = browser.find_element_by_id('antenna_filter')
        Select(select_region).select_by_value(region)
        next_month_button = browser.find_element_by_css_selector('button.fc-next-button.fc-button.fc-state-default.fc-corner-right')
        # Loop for months
        for m in range(max_month):
            td = browser.find_elements_by_class_name('fc-event-container')
            for i in range(len(td)):
                if (m, i) in td_count:
                    continue
                a = td[i].find_element_by_tag_name('a')
                tcf_type = td[i].find_element_by_class_name('fc-title')
                if registering(a, tcf_type):
                    td_count.append((m, i))
                    # Switch to a new tab if submit fails and search for another
                    browser.execute_script("window.open()")
                    browser.switch_to.window(browser.window_handles[-1])
            fc_mor = browser.find_elements_by_class_name('fc-more')
            for i in range(len(fc_mor)):
                fc_mor[i].click()
                plus_model = browser.find_element_by_css_selector('div.fc-popover.fc-more-popover')
                mbox = plus_model.find_element_by_class_name('fc-event-container')
                p_model_close = plus_model.find_element_by_css_selector('span.fc-close.fc-icon.fc-icon-x')
                ambox = mbox.find_elements_by_tag_name('a')
                for a in range(len(ambox)):
                    if (m, i, a) in fc_mor_count:
                        continue
                    tcf_type = ambox[a].find_element_by_class_name('fc-title')
                    if registering(ambox[a], tcf_type):
                        fc_mor_count.append((m, i, a))
                        # Switch to a new tab if submit fails and search for another
                        browser.execute_script("window.open()")
                        browser.switch_to.window(browser.window_handles[-1])
                    error_close = browser.find_elements_by_class_name('close-jq-toast-single')
                    for e in error_close:
                        try:
                            browser.execute_script("arguments[0].click();", e)
                        except: pass
                p_model_close.click()
            # Switch to next content
            browser.execute_script("arguments[0].click();", next_month_button)
            browser.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    except Exception as e:
        if e.__class__  == WebDriverException:
            browser.stop_client()
            browser.quit()
            break
    
