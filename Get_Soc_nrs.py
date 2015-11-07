# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os
import time

# Get input to login
Your_email = raw_input('Enter your Email to Socrative:')
Your_Socrative_Password = raw_input('Enter your Password to Socrative:')
#Your_email = 'email@example.com'
#Your_Socrative_Password = 'password'

class DownloadSocQuiz(unittest.TestCase):
    def setUp(self):
        # Set Firefox profile to allow download of odf
        fp = webdriver.FirefoxProfile()
        fp.set_preference("browser.download.folderList",2)
        fp.set_preference("browser.download.dir", os.getenv("HOME")+os.sep+"Downloads")
        #fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/msword, application/csv, application/ris, text/csv, image/png, application/pdf, text/html, text/plain, application/zip, application/x-zip, application/x-zip-compressed, application/download, application/octet-stream")
        fp.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf")
        fp.set_preference("pdfjs.disabled", True)
        #fp.set_preference("browser.download.manager.showWhenStarting", False)
        #fp.set_preference("browser.download.manager.focusWhenStarting", False)
        #fp.set_preference("browser.download.useDownloadDir",True)
        #fp.set_preference("browser.helperApps.alwaysAsk.force", False)
        #fp.set_preference("browser.download.manager.alertOnEXEOpen", False)
        #fp.set_preference("browser.download.manager.closeWhenDone", True)
        #fp.set_preference("browser.download.manager.showAlertOnComplete", False)
        #fp.set_preference("browser.download.manager.useWindow", False)
        #fp.set_preference("services.sync.prefs.sync.browser.download.manager.showWhenStarting", False)

        self.driver = webdriver.Firefox(firefox_profile=fp)
        self.driver.implicitly_wait(30)
        self.base_url = "https://b.socrative.com/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_download_soc_quiz(self):
        driver = self.driver
        url_login = "https://b.socrative.com/"
        driver.get(self.base_url + "/")
        url_start = driver.current_url
        print(url_start)
        print("You have to login")
        driver.find_element_by_id("teacherLoginName").clear()
        driver.find_element_by_id("teacherLoginName").send_keys(Your_email)
        driver.find_element_by_id("teacherLoginPass").clear()
        driver.find_element_by_id("teacherLoginPass").send_keys(Your_Socrative_Password)
        driver.find_element_by_id("teacherLoginButton").click()
        print("You are now logged in")
        driver.find_element_by_xpath("//li[@id='manage-quizzes-label']/button").click()
        driver.find_element_by_id("my-quizzes-button").click()
        driver.find_element_by_id("search-all-button").click()
        all_quizzes = driver.find_element_by_xpath("//div[@id='quiz-list-container']").text
        print(all_quizzes)
        qSplit = all_quizzes.split("Quiz_")
        print qSplit
        arr_len = len(qSplit)
        print(arr_len)
        index = 1
        while index < arr_len:
            i = index
            current_quiz = qSplit[index].rstrip()
            driver.find_element_by_xpath("//div[@id='quiz-list-container']/div/div[" + str(i) + "]/div/div/span").click()
            driver.find_element_by_xpath("//div[@id='quiz-list-container']/div/div[" + str(i) + "]/div[2]/button[4]").click()
            time.sleep(0.5)
            SOC_url = driver.current_url
            SOC_id = SOC_url.split("edit-quiz/")[1].rstrip()
            print(str(i) + " - " + current_quiz + " - " + SOC_id)
            time.sleep(0.5)
            driver.find_element_by_xpath("//li[@id='manage-quizzes-label']/button").click()
            time.sleep(0.5)
            driver.find_element_by_id("my-quizzes-button").click()
            time.sleep(0.5)
            driver.find_element_by_id("search-all-button").click()

            index += 1
    
    def is_element_present(self, how, what):
        try: self.driver.find_element(by=how, value=what)
        except NoSuchElementException, e: return False
        return True
    
    def is_alert_present(self):
        try: self.driver.switch_to_alert()
        except NoAlertPresentException, e: return False
        return True
    
    def close_alert_and_get_its_text(self):
        try:
            alert = self.driver.switch_to_alert()
            alert_text = alert.text
            if self.accept_next_alert:
                alert.accept()
            else:
                alert.dismiss()
            return alert_text
        finally: self.accept_next_alert = True
    
    def tearDown(self):
        self.driver.quit()
        self.assertEqual([], self.verificationErrors)

if __name__ == "__main__":
    unittest.main()
