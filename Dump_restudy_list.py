# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoAlertPresentException
import os
import unittest, time, re
import collections
import json

# Get input to login
Your_Uni_c_username = raw_input('Enter your Uni-c username:')
Your_Uni_c_Password = raw_input('Enter your Uni-c password:')
#Your_Uni_c_username = "abcd1234"
#Your_Uni_c_Password = "12345678"

fag = "https://www.restudy.dk/kemi-c-niveau"

class DumpRestudyList(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(30)
        self.base_url = "https://www.restudy.dk/"
        self.verificationErrors = []
        self.accept_next_alert = True
    
    def test_dump_restudy_list(self):
        driver = self.driver
        
        url_login = "https://www.restudy.dk/"
        driver.get(self.base_url)
        url_start = driver.current_url
        print(url_start)
        print("You have to login")
        driver.find_element_by_id("loginBtn").click()
        driver.find_element_by_css_selector("img[alt=\"reg_login_using_unic\"]").click()
        driver.find_element_by_id("user").clear()
        driver.find_element_by_id("user").send_keys(Your_Uni_c_username)
        driver.find_element_by_id("pass").clear()
        driver.find_element_by_id("pass").send_keys(Your_Uni_c_Password)
        driver.find_element_by_id("login").click()
        time.sleep(0.5)
        print("You are now logged in")
        driver.get(fag)
        print "Now at %s"%fag

        page_text = driver.find_element_by_css_selector("div.right_section_course").text
        page_lines = page_text.splitlines()

        # Collect lines
        subjects_lines = []
        subjects_nr = []
        content_lines = []
        subjects_nr_videos = []
        subjects_links = []

        dic = collections.OrderedDict()

        for m in range(len(page_lines)):
            line = page_lines[m]
            if "." in line.split(" ")[0]:
                subject_nr = int(line.split(" ")[0].replace(".", ""))
                subjects_nr.append(subject_nr)
                dic['nr_of_subjects'] = subject_nr

                subjects_line = line.replace("%s. "%subject_nr, "")
                subjects_lines.append(subjects_line)
                dic[str(subject_nr)] = collections.OrderedDict()
                dic[str(subject_nr)]['subjects_line'] = subjects_line

                content_line = page_lines[m+1]
                content_lines.append(content_line)
                dic[str(subject_nr)]['content_line'] = content_line

                nr_videos = int(content_line.split(" ")[0])
                subjects_nr_videos.append(nr_videos)
                dic[str(subject_nr)]['nr_videos'] = nr_videos

                link = fag + "-" + subjects_line.lower().replace(" ", "-")
                subjects_links.append(link)
                dic[str(subject_nr)]['link'] = link

                continue
            else:
                continue

        dic['subjects_lines'] = subjects_lines
        dic['subjects_nr'] = subjects_nr
        dic['content_lines'] = content_lines
        dic['subjects_nr_videos'] = subjects_nr_videos
        dic['subjects_links'] = subjects_links

        for i in range(len(subjects_lines)):
        #for i in range(1, 2):
            #print subjects_nr[i], subjects_lines[i], subjects_nr_videos[i], subjects_links[i]
            driver.get(subjects_links[i])
            time.sleep(2.0)

            # Get the text
            subject_page_text = driver.find_element_by_id("wikiTopicsDetails").text
            subject_page_lines = subject_page_text.splitlines()

            # Collect
            video_nrs = []
            video_titles = []
            video_infos = []
            video_flags = []
            for n in range(len(subject_page_lines)):
                line = subject_page_lines[n]
                if "." in line.split(" ")[0]:
                    video_nr = int(line.split(" ")[0].replace(".", ""))
                    video_nrs.append(video_nr)
                    dic[str(i+1)]['nr_of_videos'] = video_nr

                    video_title = subject_page_lines[n+1][1:]
                    video_titles.append(video_title)
                    dic[str(i+1)][str(video_nr)] = collections.OrderedDict()
                    dic[str(i+1)][str(video_nr)]['video_title'] = video_title

                    video_info = subject_page_lines[n+2]
                    video_infos.append(video_info)
                    dic[str(i+1)][str(video_nr)]['video_info'] = video_info

                    flags = subject_page_lines[n+5]
                    video_flags.append(flags)
                    dic[str(i+1)][str(video_nr)]['flags'] = flags
    
                    print_string = "_V%s_%s"%(video_nr, video_title.replace(" ","_"))
                    drop_down = "E%s_%s%s"%(subjects_nr[i], subjects_lines[i].replace(" ","_"), print_string)
                    print drop_down

            dic[str(i+1)]['video_nrs'] = video_nrs
            dic[str(i+1)]['video_titles'] = video_titles
            dic[str(i+1)]['video_infos'] = video_infos
            dic[str(i+1)]['video_flags'] = video_flags

        #print json.dumps(dic)
        print json.dumps(dic, indent=4)
        with open(os.getenv("HOME")+os.sep+"Downloads"+os.sep+'Dump_restudy_list.json', 'w') as f:
            json.dump(dic, f, indent=4)

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
