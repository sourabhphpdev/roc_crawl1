# -*- coding: utf-8 -*-
import scrapy
import datetime
import requests
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import logging
import random
from datetime import datetime
import os
import csv
import zipfile

PROXY_HOST = 'us-wa.proxymesh.com'  # rotating proxy
PROXY_PORT = 31280
PROXY_USER = 'sourabh.phpdev'
PROXY_PASS = 'kittushalu'


manifest_json = """
{
    "version": "1.0.0",
    "manifest_version": 2,
    "name": "Chrome Proxy",
    "permissions": [
        "proxy",
        "tabs",
        "unlimitedStorage",
        "storage",
        "<all_urls>",
        "webRequest",
        "webRequestBlocking"
    ],
    "background": {
        "scripts": ["background.js"]
    },
    "minimum_chrome_version":"22.0.0"
}
"""

background_js = """
var config = {
        mode: "fixed_servers",
        rules: {
          singleProxy: {
            scheme: "http",
            host: "%s",
            port: parseInt(%s)
          },
          bypassList: ["localhost"]
        }
      };

chrome.proxy.settings.set({value: config, scope: "regular"}, function() {});

function callbackFn(details) {
    return {
        authCredentials: {
            username: "%s",
            password: "%s"
        }
    };
}

chrome.webRequest.onAuthRequired.addListener(
            callbackFn,
            {urls: ["<all_urls>"]},
            ['blocking']
);
""" % (PROXY_HOST, PROXY_PORT, PROXY_USER, PROXY_PASS)

class CrawlAnualReturnAll(scrapy.Spider):
    name = 'crawl_anual_return_all'
    today = datetime.now()
    current_year = today.year
    # allowed_domains = ['mca.com']
    # start_urls = ['http://www.mca.gov.in/mcafoportal/viewPublicDocumentsFilter.do']
    start_urls = ['http://www.google.com']
    def __init__(self):
        self.start_requests()
    data=[]
    random_no_of_visit =[1,2,3]
    random_time_stop=[1,0.2,0.3,0.4,0.6,0.5,0.7,0.8,0.9,0.966,0.44,0.232,0.676,0.33,0.1232,0.768]
    random_url_list= [
        'http://www.mca.gov.in/MinistryV2/about_mca.html',
        'http://www.mca.gov.in/MinistryV2/companiesact2013.html',
        'http://www.mca.gov.in/MinistryV2/llpact.html',
        'http://www.mca.gov.in/MinistryV2/insolvency+and+bankruptcy+code.html',
        'http://www.mca.gov.in/MinistryV2/competitionact.html',
        'http://www.mca.gov.in/MinistryV2/partnershipact.html',
        'http://www.mca.gov.in/MinistryV2/charteredaccountantsact.html',
        'http://www.mca.gov.in/MinistryV2/costandworksact.html',
        'http://www.mca.gov.in/MinistryV2/thecompanysecretariesact.html',
        'http://www.mca.gov.in/MinistryV2/societiesregistrationact.html',
        'http://www.mca.gov.in/MinistryV2/companiesdonationtonationalfundact1951.html',
        'http://www.mca.gov.in/mcafoportal/login.do',
        'http://www.mca.gov.in/mcafoportal/showCheckCompanyName.do',
        'http://www.mca.gov.in/mcafoportal/findLLPIN.do',
        'http://www.mca.gov.in/mcafoportal/showCheckLLPName.do',
        'http://www.mca.gov.in/MinistryV2/changellpinformation.html',
        'http://www.mca.gov.in/MinistryV2/companyformsdownload.html#infoserv',
        'http://www.mca.gov.in/mcafoportal/viewSignatoryDetails.do',
        'http://www.mca.gov.in/mcafoportal/verifyPartnerDetails.do',
        'http://www.mca.gov.in/mcafoportal/trackStatus.do',
        'http://www.mca.gov.in/MinistryV2/companyformsdownload.html',
        'http://www.mca.gov.in/mcafoportal/showNEFTPayment.do',
        'http://www.mca.gov.in/mcafoportal/viewDirectorMasterData.do',
        'http://www.mca.gov.in/MinistryV2/rti.html',
        'http://www.mca.gov.in/MinistryV2/sfio.html',
        'http://www.mca.gov.in/MinistryV2/monthlyinformationbulletin.html',
        'http://www.mca.gov.in/MinistryV2/monthlymcanewsletters.html'
    ]

    def parse(self, response):
        today = datetime.now()
        src = "./roc/resources/savedata/2020/" + today.strftime('%Y_%m_%d')
        updated_cin_list = []
        if not os.path.exists(src):
            os.mkdir(src)
            fields = []
            with open(src + '/cin_list_anual_return.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            with open(src + '/cin_list_other_eform.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
            with open(src + '/cin_list_other_attachment.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow(fields)
        else:
            with open(src + '/cin_list_anual_return.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    try:
                        updated_cin_list.append(row[0])
                    except:
                        pass
        main_url = 'http://www.mca.gov.in/mcafoportal/viewPublicDocumentsFilter.do'
        cin_list = requests.request(method='GET', url='http://139.59.47.48:8000/api/mca_info/cinList')
        cin_list = json.loads(cin_list.json())
        # cin_list=['U72900HR2012PTC045028','U72900DL2011PTC225614']
        driver = self.start_driver(response.url)
        for cin in cin_list:
            work = {}
            # driver.get(main_url)
            # time.sleep(3)
            # ckecks = driver.find_element_by_xpath('//input[@name="cinChk"]')
            # ckecks.click()
            # time.sleep(10)
            # cin_input = driver.find_element_by_xpath('//input[@name="cinFDetails"]')
            # cin_input.clear()
            # cin_input.send_keys(cin)
            save_cin_to_csv = 1
            if cin in updated_cin_list:
                continue
            max_loop_count=10
            loop_count=0
            process_done=False
            while process_done==False and loop_count < max_loop_count:
                # self.send_email_start()
                try:
                    driver.get(main_url)
                except Exception as e:
                    loop_count +=1
                    # driver.close()
                    continue;
                nv=random.choice(self.random_no_of_visit)
                for i in range(nv):
                    rurl=random.choice(self.random_url_list)
                    rt=random.choice(self.random_time_stop)
                    driver.get(rurl)
                    time.sleep(rt)
                work['cin']=cin
                self.logger.info('Process Start for cin {} loop count: {}'.format(cin,loop_count))


                try:
                    time.sleep(2)
                    ckecks= driver.find_element_by_xpath('//input[@name="cinChk"]')
                    ckecks.click()
                    time.sleep(2)
                    cin_input = driver.find_element_by_xpath('//input[@name="cinFDetails"]')
                    cin_input.clear()
                    cin_input.send_keys(cin)
                    cin_input.send_keys(Keys.RETURN)
                    time.sleep(1)
                    self.logger.info('Entered cin {} Number'.format(cin))
                except Exception as e:
                    self.logger.info('Input checkbox not found for cin {}'.format(cin))
                    loop_count +=1
                    # driver.close()
                    continue

                try:
                    link=driver.find_element_by_xpath('//a[@class="dashboardlinks"]')
                except Exception as e:
                    link='';
                    try:
                        temp = 'No company found with this CIN'
                        self.save_to_api(cin, False, temp)
                        fields = [cin, 'Success', temp]
                        with open(src + '/cin_list_anual_return.csv', 'a') as f:
                            writer = csv.writer(f)
                            writer.writerow(fields)
                        time.sleep(3)
                        driver.find_element_by_xpath('//a[@id="msgboxclose"]').click()
                        process_done = True
                    except:
                        continue


                if link:
                    link.click()
                    strik_off='yes'
                    try:
                        driver.find_element_by_xpath('//input[@name="submitBtn"][@value="Yes"]').click()
                        time.sleep(1)
                        strik_off = 'no'
                    except:
                        strik_off='no'

                    if strik_off=='no':
                        err=0
                        try:
                            driver.find_element_by_xpath("//select[@name='categoryName']/option[text()='Annual Returns and Balance Sheet eForms']").click()
                            driver.find_element_by_xpath("//select[@name='finacialYear']/option[text()='2020']").click()
                            driver.find_element_by_xpath("//input[@id='viewCategoryDetails_0']").click()
                            time.sleep(0.3)
                        except Exception as e:
                            err=1
                            save_cin_to_csv = 0
                            self.logger.info('exception occuer when choose annual return select option for- cin {} Number'.format(cin))
                            loop_count +=1
                            # driver.close()
                            continue
                        ar_text=''
                        if err==0:
                            try:
                                not_availabe_text=driver.find_element_by_xpath('//div[@id="msg_overlay"][@style="top: 250px; display: block;"]')
                            except:
                                not_availabe_text=''

                            if not_availabe_text:
                                try:
                                    get_text=driver.find_element_by_xpath('//div[@id="msg_overlay"][@style="top: 250px; display: block;"]/div[@id="overlayCnt"]/ul[@class="errorMessage"]/li')
                                    err=get_text.get_attribute('innerHTML')
                                    self.logger.info('Result: {} ,No documents are available for CIN:{} Number'.format(err,cin))
                                    temp = ''+err
                                    self.save_to_api(cin, False, temp)
                                    fields = [cin, 'Success', temp]
                                    with open(src + '/cin_list_anual_return.csv', 'a') as f:
                                        writer = csv.writer(f)
                                        writer.writerow(fields)
                                    time.sleep(3)
                                    driver.find_element_by_xpath('//a[@id="msgboxclose"]').click()
                                    process_done =True
                                    # driver.close()
                                except Exception as e:
                                    save_cin_to_csv = 0
                                    self.logger.info('Exception Raised for  cin {}, -- {} '.format(cin, e))
                                    loop_count +=1
                                    # driver.close()
                                    continue
                            else:
                                try:
                                    element = driver.find_element_by_css_selector("#vpdCategoryDetails")
                                    html = element.get_attribute('innerHTML')
                                    work['Doc_Proc']=self.parse_doc(html, cin)
                                    ar_text='data saved'
                                    fields = [cin, 'Success', ar_text]
                                    with open(src + '/cin_list_anual_return.csv', 'a') as f:
                                        writer = csv.writer(f)
                                        writer.writerow(fields)
                                    # driver.close()
                                    process_done =True
                                except Exception as e:
                                    save_cin_to_csv = 0
                                    self.logger.info('Detail Content not found cin {} Number, Exception: {}'.format(cin, e))
                                    loop_count +=1
                                    # driver.close()
                                    continue
        driver.close()
        self.logger.info('Process complete')



    def parse_doc(self, html,cin):
        soup = BeautifulSoup(html, 'html.parser')
        temp=''
        try:
            table = soup.find('table' ,attrs={'class':'result-forms_vpd'})
            trs = table.find_all('tr')
            res=[]
            for tr in trs:
              tds = tr.find_all('td')
              for td in tds:
                res.append(td.text)
            for x, y in zip(res[0::2], res[1::2]):
                temp += x.strip() + ' : ' + y.strip() + '<br>'
            self.save_to_api(cin, True, temp)
            return 'Work Completed'
        except Exception as e:
            temp = 'no response found today'
            self.save_to_api(cin,False,temp)
            return 'Exception:'+e


    def parse_edoc(self, html, cin):
        soup = BeautifulSoup(html, 'html.parser')
        temp = ''
        try:
            table = soup.find('table', attrs={'class': 'result-forms_vpd'})
            trs = table.find_all('tr')
            res = []
            for tr in trs:
                tds = tr.find_all('td')
                for td in tds:
                    res.append(td.text)
            for x, y in zip(res[0::2], res[1::2]):
                temp += x.strip() + ' : ' + y.strip() + '<br>'
            self.save_to_api_eform(cin, True, temp)
            return 'Work Completed'
        except Exception as e:
            temp = 'no response found today'
            self.save_to_api_eform(cin, False, temp)
            return 'Exception:' + e

    def start_driver(self,url):
        driver = None

        PROXY = "49.248.154.237:80"  # IP:PORT or HOST:PORT
        # PROXY = "51.158.106.54:8811"  # IP:PORT or HOST:PORT
        # PROXY = "51.38.34.40:3128"  # IP:PORT or HOST:PORT
        # PROXY = "us-wa.proxymesh.com:31280"  # IP:PORT or HOST:PORT

        chrome_options = Options()
        # chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--window-size=1420,1080')
        chrome_options.add_argument('--disable-gpu')
        pluginfile = 'proxy_auth_plugin.zip'

        with zipfile.ZipFile(pluginfile, 'w') as zp:
            zp.writestr("manifest.json", manifest_json)
            zp.writestr("background.js", background_js)
        chrome_options.add_extension(pluginfile)
        # chrome_options.add_argument('--proxy-server=https://%s' % PROXY)
        driver = webdriver.Chrome('./chrome_driver/chromedriver_linux',chrome_options=chrome_options)
        driver.get(url)

        return driver

    def save_to_api(self,cin,doc_present,doc_info):

        url = "http://139.59.47.48:8000/api/mca_info/cinMarked/"
        if doc_present==True:
            payload = "cinNumer="+cin+"&doc_present=True&doc_information="+doc_info
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)
        else:
            payload = "cinNumer="+cin+"&doc_present=False&doc_information="+doc_info
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)

    def save_to_api_eform(self, cin, doc_present, doc_info):

        url = "http://139.59.47.48:8000/api/mca_info/cinMarked/"
        if doc_present == True:
            payload = "cinNumer=" + cin + "&other_eform_documents_present=True&other_eform_documents_information=" + doc_info
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)
            # print('from true', requestto.text)
        else:
            payload = "cinNumer=" + cin + "&other_eform_documents_present=False&other_eform_documents_information=" + doc_info
            headers = {
                'content-type': "application/x-www-form-urlencoded",
            }
            requestto = requests.request("POST", url, data=payload, headers=headers)

    def send_email_report(self):
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # print("Current Time =", current_time)
        mail_content = '''<h3>Entracter Report</h3>
        <table><tr><th>CIN</th><th>Doc Process</th><th>Other Doc Process</th></tr>
        '''
        data=self.data
        try:
            for row in data:
                mail_content+='<tr><td>'+row['cin']+'</td><td>'+row['Doc_Proc']+'</td><td>'+row['Other_Doc_Proc']+'</td></tr>'
        except:
            pass
        mail_content+='</table>'

        # The mail addresses and password
        sender_address = 'softgneer.entracker@gmail.com'
        sender_pass = 'Mca@1234'
        receiver_address = 'ninjakissmo@gmail.com'
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Entracker Report-. '+current_time  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()


        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        # print('Mail Sent')

    def send_email_start(self):
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # print("Current Time =", current_time)
        mail_content = '''<h3>Entracter Crawler Start</h3> 
           '''
        mail_content += ''

        # The mail addresses and password
        sender_address = 'softgneer.entracker@gmail.com'
        sender_pass = 'Mca@1234'
        receiver_address = 'ninjakissmo@gmail.com'
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = 'Entracker Crawl Start-. ' + current_time  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        # print('Mail Sent')

    def send_email(self,sub,message):
        from datetime import datetime
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        # print("Current Time =", current_time)
        mail_content = message


        # The mail addresses and password
        sender_address = 'softgneer.entracker@gmail.com'
        sender_pass = 'Mca@1234'
        receiver_address = 'ninjakissmo@gmail.com'
        # Setup the MIME
        message = MIMEMultipart()
        message['From'] = sender_address
        message['To'] = receiver_address
        message['Subject'] = sub + ':' + current_time  # The subject line
        # The body and the attachments for the mail
        message.attach(MIMEText(mail_content, 'html'))
        # Create SMTP session for sending the mail
        session = smtplib.SMTP('smtp.gmail.com', 587)  # use gmail with port
        session.starttls()  # enable security
        session.login(sender_address, sender_pass)  # login with mail_id and password
        text = message.as_string()
        session.sendmail(sender_address, receiver_address, text)
        session.quit()
        # print('Mail Sent')
