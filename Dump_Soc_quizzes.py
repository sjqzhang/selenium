from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import unittest, time, re, os
import time
import unicodedata, sys

# Get input to login
#Your_email = raw_input('Enter your Email to Socrative:')
#Your_Socrative_Password = raw_input('Enter your Password to Socrative:')
Your_email = 'tlinnet@gmail.com'
Your_Socrative_Password = 'xhwo1453Xl'

debug = False

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
        #driver.find_element_by_xpath("//li[@id='manage-quizzes-label']/button").click()
        driver.find_element_by_id("manage-quizzes-label").click()
        driver.find_element_by_id("my-quizzes-button").click()
        driver.find_element_by_id("search-all-button").click()
        all_quizzes = driver.find_element_by_xpath("//div[@id='quiz-list-container']").text
        print(all_quizzes)
        qSplit = all_quizzes.split("Quiz_")
        #print qSplit
        arr_len = len(qSplit)
        #print(arr_len)
        index = 13
        print ""
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
            ids = driver.find_elements_by_xpath('//*[@id]')

            # Make a quiz dic
            quiz_dic = {}
            quiz_dic['nr_of_quizzes'] = 0
            count_answers = False

            for ii in ids:
                c_attr = ii.get_attribute('id')
                if debug:
                    if c_attr == "roomname":
                        print "-------- ROOM NAME --------\n", ii.tag_name, ii.text, "\n----------------------------"
                    elif c_attr == "soc-number-container":
                        print "-------- SOC number --------\n", ii.tag_name, ii.text, "\n-----------------------------"
                    elif c_attr == "questions":
                        #print "-------- all questions --------\n", ii.tag_name, ii.text.translate(unaccented_map()), "\n-----------------------------"
                        print "-------- all questions --------\n", ii.tag_name, ii.text.encode('utf-8'), "\n-----------------------------"
                        print type(ii.text)
                        print unichr(ii.text)
                # Count number of quizzes
                #if c_attr.startswith( 'format-toggle-question-' ):
                if c_attr.startswith( 'question-' ):
                    quiz_nr = c_attr.split("-")[-1]
                    quiz_dic['nr_of_quizzes'] = int(quiz_nr)
                    quiz_dic[quiz_nr] = {}
                    quiz_dic[quiz_nr]['nr_of_answers'] = 0
                    quiz_dic[quiz_nr]['quiz']= ii.text.encode('utf-8')
                    quiz_dic[quiz_nr]['quiz_id']= ii.id
                    count_answers = True
                    answer_ids = []

                if count_answers:
                    #print c_attr
                    if c_attr.startswith( 'mc-answer-' ) or c_attr.startswith( 'fr-answer-'):
                        c_attr_split = c_attr.split("-")
                        answer_nr =c_attr_split[-1]
                        answer_ids.append(ii.id)
                        quiz_dic[quiz_nr]['answer_ids'] = answer_ids
                        quiz_dic[quiz_nr]['nr_of_answers'] = int(answer_nr)
                        quiz_dic[quiz_nr]['type'] = '_'.join(str(x) for x in c_attr_split[:-1])
                    elif c_attr.startswith( 'question-' ) or c_attr.startswith( 'format-toggle-question-' ):
                        count_answers = True
                    else:
                        count_answers = False

            for i in range(1, quiz_dic['nr_of_quizzes']+1):
                print i, quiz_dic[str(i)]['type'], quiz_dic[str(i)]['nr_of_answers'], quiz_dic[str(i)]['answer_ids']

            j = quiz_dic['1']

            #driver.find_element_by_xpath("//li[@id='manage-quizzes-label']/button").click()
            #time.sleep(0.5)
            #driver.find_element_by_id("my-quizzes-button").click()
            #time.sleep(0.5)
            #driver.find_element_by_id("search-all-button").click()

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




# Translation dictionary.  Translation entries are added to this dictionary as needed.
CHAR_REPLACEMENT = {
    # latin-1 characters that don't have a unicode decomposition
    0xc5: u"AA", # LATIN CAPITAL LETTER AA
    0xc6: u"AE", # LATIN CAPITAL LETTER AE
    0xd0: u"D",  # LATIN CAPITAL LETTER ETH
    0xd8: u"OE", # LATIN CAPITAL LETTER O WITH STROKE
    0xde: u"Th", # LATIN CAPITAL LETTER THORN
    0xdf: u"ss", # LATIN SMALL LETTER SHARP S
    0xe5: u"aa", # LATIN SMALL LETTER AA
    0xe6: u"ae", # LATIN SMALL LETTER AE
    0xf0: u"d",  # LATIN SMALL LETTER ETH
    0xf8: u"oe", # LATIN SMALL LETTER O WITH STROKE
    0xfe: u"th", # LATIN SMALL LETTER THORN
    }

class unaccented_map(dict):
    # Maps a unicode character code (the key) to a replacement code
    # (either a character code or a unicode string).
    def mapchar(self, key):
        ch = self.get(key)
        if ch is not None:
            return ch
        de = unicodedata.decomposition(unichr(key))
        if de:
            try:
                ch = int(de.split(None, 1)[0], 16)
            except (IndexError, ValueError):
                ch = key
        else:
            ch = CHAR_REPLACEMENT.get(key, key)
        self[key] = ch
        return ch
    if sys.version >= "2.5":
        # use __missing__ where available
        __missing__ = mapchar
    else:
        # otherwise, use standard __getitem__ hook (this is slower,
        # since it's called for each character)
        __getitem__ = mapchar

if __name__ == "__main__":
    unittest.main()
