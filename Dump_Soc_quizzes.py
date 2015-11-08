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

# Additional print out
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
        index = 1
        print ""

        # Make a quiz dic
        quiz_dic = {}
        indexes = []

        while index < arr_len:
            indexes.append(index)
            i = index
            current_quiz = qSplit[index].rstrip()
            driver.find_element_by_xpath("//div[@id='quiz-list-container']/div/div[" + str(i) + "]/div/div/span").click()
            driver.find_element_by_xpath("//div[@id='quiz-list-container']/div/div[" + str(i) + "]/div[2]/button[4]").click()
            time.sleep(0.5)
            SOC_url = driver.current_url
            SOC_id = SOC_url.split("edit-quiz/")[1].rstrip()
            #print("\n" + str(i) + " - " + current_quiz + " - " + SOC_id)
            time.sleep(0.5)
            ids = driver.find_elements_by_xpath('//*[@id]')

            # Default
            c_attr_list = []
            quiz_dic[str(i)] = {}
            quiz_dic[str(i)]["quiz_name"] = current_quiz
            quiz_dic['nr_of_quizzes'] = i
            count_answers = False

            for ii in ids:
                c_attr = ii.get_attribute('id')
                c_attr_list.append(c_attr)

                # Get some information
                if c_attr == "roomname":
                    quiz_dic[str(i)]['roomname'] = ii.text
                    if debug:
                        print "-------- ROOM NAME --------\n", ii.tag_name, ii.text, "\n----------------------------"
                elif c_attr == "soc-number-container":
                    quiz_dic[str(i)]['soc-number-container'] = ii.text
                    if debug:
                        print "-------- SOC number --------\n", ii.tag_name, ii.text, "\n-----------------------------"
                elif c_attr == "questions":
                    if debug:
                        print "-------- all questions --------\n", ii.tag_name, ii.text.encode('utf-8'), "\n-----------------------------"
 
                # Count number of questions, and store the quiz, and the id
                if c_attr.startswith( 'question-' ):
                    question_nr = int(c_attr.split("-")[-1])
                    quiz_dic[str(i)]['nr_of_questions'] = question_nr
                    j = question_nr
                    quiz_dic[str(i)][str(j)] ={}

                    # Start counting answers and update later
                    quiz_dic[str(i)][str(j)]['nr_of_answers'] = 0
                    quiz_dic[str(i)][str(j)]['quiz_id']= ii.id

                    # Start getting the list of answers to each question
                    count_answers = True
                    answer_ids = []
                    answer_text = []
                    answer_true = []

                    # Get the quiz text
                    quiz_text = ii.text.encode('utf-8')
                    quiz_lines = quiz_text.splitlines()

                    is_question = False
                    is_answers = False
                    is_TrueFalse = False
                    is_explanation = False

                    # Collect lines
                    quiz_question_lines = []
                    quiz_answers_lines = []
                    quiz_is_TrueFalse = False
                    quiz_explanation_lines = []

                    for m in range(len(quiz_lines)):
                        line = quiz_lines[m]
                        #print line
                        if "EDIT" in line:
                            is_question = True
                            is_answers = False
                            is_TrueFalse = False
                            is_explanation = False
                            continue

                        elif "ANSWER CHOICE" in line:
                            is_question = False
                            is_answers = True
                            is_TrueFalse = False
                            is_explanation = False
                            continue

                        elif "Correct Answer:" in line:
                            is_question = False
                            is_answers = False
                            is_TrueFalse = True
                            is_explanation = False

                        elif "Explanation:" in line:
                            is_question = False
                            is_answers = False
                            is_TrueFalse = False
                            is_explanation = True
                            continue

                        if is_question:
                            quiz_question_lines.append(line)
                        elif is_answers:
                            quiz_answers_lines.append(line)
                        elif is_TrueFalse:
                            quiz_is_TrueFalse = True
                        elif is_explanation:
                            quiz_explanation_lines.append(line)

                    # Store for quiz and question
                    quiz_dic[str(i)][str(j)]['quiz_question_lines'] = quiz_question_lines
                    quiz_dic[str(i)][str(j)]['quiz_answers_lines'] = quiz_answers_lines
                    quiz_dic[str(i)][str(j)]['quiz_is_TrueFalse'] = quiz_is_TrueFalse
                    quiz_dic[str(i)][str(j)]['quiz_explanation_lines'] = quiz_explanation_lines

                # Count number of answers, and the True/False value of the statements
                if count_answers:
                    # Get the information
                    if c_attr.startswith( 'mc-answer-' ) or c_attr.startswith( 'fr-answer-'):
                        c_attr_split = c_attr.split("-")
                        answer_nr = int(c_attr_split[-1])
                        k = answer_nr

                        # Update answer ids
                        answer_ids.append(ii.id)
                        quiz_dic[str(i)][str(j)]['answer_ids'] = answer_ids
                        quiz_dic[str(i)][str(j)]['nr_of_answers'] = k
                        quiz_dic[str(i)][str(j)]['type'] = '-'.join(str(x) for x in c_attr_split[:-1])

                        # If of type multiple-choice, see if the answer is correct.
                        if quiz_dic[str(i)][str(j)]['type'] == 'mc-answer':
                            answer_text.append(ii.text.encode('utf-8'))
                            if "is-correct" in ii.get_attribute('class'):
                                answer_true.append(True)
                            else:
                                answer_true.append(False)

                            # Store
                            quiz_dic[str(i)][str(j)]['answer_text'] = answer_text
                            quiz_dic[str(i)][str(j)]['answer_true'] = answer_true

                        # If of type short-answer, see if the answer is correct.
                        elif quiz_dic[str(i)][str(j)]['type'] == 'fr-answer':
                            if len(quiz_explanation_lines) > 0:
                                correct_answers = re.findall(r'\[(.*?)\]', quiz_explanation_lines[0], re.DOTALL)
                                if len(correct_answers) > 0:
                                    quiz_dic[str(i)][str(j)]['answer_true'] = correct_answers[0].split(";")
                                else:
                                    quiz_dic[str(i)][str(j)]['answer_true'] = []
                            else:
                                quiz_dic[str(i)][str(j)]['answer_true'] = []

                    elif "TrueFalse" in quiz_text:
                        quiz_dic[str(i)][str(j)]['answer_ids'] = None
                        quiz_dic[str(i)][str(j)]['nr_of_answers'] = None
                        quiz_dic[str(i)][str(j)]['type'] = "tf-answer"

                        correct_answers = re.findall(r'\[(.*?)\]', quiz_explanation_lines[0], re.DOTALL)[0].split(";")
                        quiz_dic[str(i)][str(j)]['answer_true'] = correct_answers
                        count_answers = False

                    # Continue counting if meeting other buttons.
                    elif c_attr.startswith('question-') or c_attr.startswith('format-toggle-question-'):
                        count_answers = True
                    else:
                        count_answers = False

            # Print all xpaths
            if debug:
                for temp_print in c_attr_list:
                    print temp_print

            # Print to screen
            if True:
            #if False:
                for i in indexes:
                    # Print quiz name
                    print("\n" + str(i) + " - " + quiz_dic[str(i)]["quiz_name"] + " - " + quiz_dic[str(i)]['soc-number-container'])

                    for j in range(1, quiz_dic[str(i)]['nr_of_questions']+1):
                        qtype = quiz_dic[str(i)][str(j)]['type']
                        if qtype == "mc-answer":
                            #continue
                            print i, j, "mc-answer", quiz_dic[str(i)][str(j)]['nr_of_answers'], quiz_dic[str(i)][str(j)]['answer_true']
                        elif qtype == "fr-answer":
                            #continue
                            print i, j, "fr-answer", quiz_dic[str(i)][str(j)]['nr_of_answers'], quiz_dic[str(i)][str(j)]['answer_true']
                        elif qtype == "tf-answer":
                            #continue
                            print i, j, "tf-answer", quiz_dic[str(i)][str(j)]['nr_of_answers'], quiz_dic[str(i)][str(j)]['answer_true']

            driver.find_element_by_xpath("//li[@id='manage-quizzes-label']/button").click()
            time.sleep(0.5)
            driver.find_element_by_id("my-quizzes-button").click()
            time.sleep(0.5)
            driver.find_element_by_id("search-all-button").click()

            # Add to index
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
