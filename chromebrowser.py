from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, NoSuchWindowException
from vlc import MediaPlayer
from threading import Thread
from time import sleep
import json
import random


class ChromeBrowse(Chrome):
    
    def __init__(self):
        super().__init__(executable_path='.//bin//chromedriver.exe')
        self.maximize_window()
        #self.implicitly_wait(50)

        self.login_url    = 'https://portail.if-algerie.com/login'
        self.exams_url    = 'https://portail.if-algerie.com/exams'
        self.playsound    = MediaPlayer('.//bin//audio.mp3')
        self.td_count     = []
        self.fc_mor_count = []

        # User settings
        with open('settings.json', 'r') as f:
            config = json.load(f)
        
        self.username   = config["email"]
        self.password   = config["password"]
        self.regions    = config["regions"]
        self.tcf_exams  = config["tcf-exams"]
        self.motivation = config["motivation"]
        self.max_month  = config["max-month"]
        self.date_mod   = config["date"]
        self.period_mod = config["period"]

        self.loginWait  = WebDriverWait(self, 10)
        self.searchWait = WebDriverWait(self, 1)
        self.submitWiat = WebDriverWait(self, 5)
    
    def login(self):
        while True:
            try:
                self.get(self.login_url)
                email = self.loginWait.until(EC.visibility_of_element_located((By.NAME, 'email')))
                password = self.loginWait.until(EC.visibility_of_element_located((By.NAME, 'password')))
                submit = self.loginWait.until(EC.element_to_be_clickable((By.ID, 'login')))
                email.send_keys(self.username)
                password.send_keys(self.password)
                submit.click()
                self.loginWait.until(EC.url_changes(self.current_url))
                self.get(self.exams_url)
                break
            except: pass
    
    def submit(self, a, tcf):
        # Get active FC and correct
        if a.get_attribute('class') == 'fc-day-grid-event fc-h-event fc-event fc-start fc-end bg-secondary':
            return False
        # Check if correct exam
        if tcf.text in self.tcf_exams:
            # Open date appointment modal
            self.clear()
            a.click()
            exams_modal = self.submitWiat.until(EC.visibility_of_element_located((By.ID, 'exams-modal')))
            payment_day = exams_modal.find_element_by_id('paymentDay')
            close_exam_button = exams_modal.find_element_by_css_selector('button.btn.btn-default.waves-effect')
            select_motivation = exams_modal.find_element_by_id('motivation')
            Select(select_motivation).select_by_visible_text(self.motivation)
            # Check if payment day is disabled
            if payment_day.get_property('disabled'):
                self.execute_script("arguments[0].click();", close_exam_button)
                self.submitWiat.until(EC.invisibility_of_element_located(exams_modal))
                return False
            self.playsound.play()
            try:
                # Send date and submit
                Select(select_motivation).select_by_visible_text(self.motivation)
                payment_day.click()
                # Pick an available date (Not tested yet)
                calendar = self.submitWiat.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.datepicker.datepicker-dropdown.dropdown-menu.datepicker-orient-left.datepicker-orient-top')))
                days_active = calendar.find_elements_by_css_selector('td.day.active')
                if self.date_mod == 1:
                    self.execute_script("arguments[0].click();", random.choice(days_active))
                else:
                    self.execute_script("arguments[0].click();", days_active[self.date_mod])
                self.submitWiat.until(EC.invisibility_of_element_located(calendar))
                periods = self.find_element_by_id('periods')
                options = periods.find_elements_by_tag_name('option')
                if self.period_mod == 1:
                    period_value = random.choice(options).get_attribute('value')
                else:
                    period_value = options[self.period_mod].get_attribute('value')
                Select(periods).select_by_value(period_value)
                self.execute_script("arguments[0].click();", submit_exam_button)
                return True
            except:
                return False

    def clear(self):
        try:
            errors_close = self.find_elements_by_class_name('close-jq-toast-single')
            for e in errors_close:
                self.execute_script("arguments[0].click();", e)
        except: pass
    
    # Search for available appointment
    def search(self, r):
        select_region = self.searchWait.until(EC.visibility_of_element_located((By.ID, 'antenna_filter')))
        next_month_button = self.find_element_by_css_selector('button.fc-next-button.fc-button.fc-state-default.fc-corner-right')
        Select(select_region).select_by_value(r)
        # Loop for months
        for m in range(self.max_month):
            td = self.find_elements_by_class_name('fc-event-container')
            for i in range(len(td)):
                if (r, m, i) in self.td_count:
                    continue
                a = td[i].find_element_by_tag_name('a')
                tcf_type = td[i].find_element_by_class_name('fc-title')
                if self.submit(a, tcf_type):
                    self.td_count.append((r, m, i))
                    # Switch to a new tab if submit fails and search for another
                    self.execute_script("window.open()")
                    self.switch_to.window(self.window_handles[-1])
            fc_mor = self.find_elements_by_class_name('fc-more')
            for i in range(len(fc_mor)):
                self.clear()
                fc_mor[i].click()
                plus_model = self.searchWait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, 'div.fc-popover.fc-more-popover')))
                mbox = plus_model.find_element_by_class_name('fc-event-container')
                p_model_close = plus_model.find_element_by_css_selector('span.fc-close.fc-icon.fc-icon-x')
                ambox = mbox.find_elements_by_tag_name('a')
                for a in range(len(ambox)):
                    if (r, m, i, a) in self.fc_mor_count:
                        continue
                    tcf_type = ambox[a].find_element_by_class_name('fc-title')
                    if self.submit(ambox[a], tcf_type):
                        self.fc_mor_count.append((r, m, i, a))
                        # Switch to a new tab if submit fails and search for another
                        self.execute_script("window.open()")
                        self.switch_to.window(self.window_handles[-1])
                self.clear()
                p_model_close.click()
                self.searchWait.until(EC.invisibility_of_element(plus_model))
            # Switch to next content
            self.execute_script("arguments[0].click();", next_month_button)
            self.find_element_by_tag_name('body').send_keys(Keys.CONTROL + Keys.HOME)
    
    def run(self):
        while True:
            for r in self.regions:
                try:
                    self.refresh()
                    if self.current_url != self.exams_url: self.get(self.exams_url)
                    if self.current_url == self.login_url: self.login()
                    self.search(r)
                except Exception as e:
                    print(e)
                    '''
                    if e.__class__  in (WebDriverException, NoSuchWindowException):
                        self.stop_client()
                        self.quit()
                        break
                    '''


if __name__ == "__main__":
    cb = ChromeBrowse()
    cb.login()
    cb.run()