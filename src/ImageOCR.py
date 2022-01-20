from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import selenium.webdriver.support.expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import selenium.webdriver.support.ui as ui
import time
import logging

logging.basicConfig(encoding='utf-8',format='%(asctime)s %(message)s')

class ImageOCR:

    def __init__(self,isDebug = True):
        s = Service('../drivers/chromedriver.exe')
        option = webdriver.ChromeOptions()
        if not isDebug:
            option.add_argument('headless')
        self.driver  = webdriver.Chrome(service=s,chrome_options=option)
        self.init = False

    def extract(self,pics):
        #初始化页面
        if not self.init:
            self.driver.get('https://pearocr.com/')
            logging.warning('页面加载中')
            ui.WebDriverWait(self.driver,5,0.2).until(EC.title_contains('PearOCR'))
            logging.warning('页面加载成功')
            time.sleep(2)
            logging.warning('字体加载中')
            ui.WebDriverWait(self.driver, 40,0.2).until_not(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"加载:")]')))
            logging.warning('字体加载成功')
            time.sleep(1)
            try:
                self.driver.find_element(By.XPATH, '//*[contains(text(),"待识别模块加载完毕")]')
                logging.warning('加载识别模块')
                ui.WebDriverWait(self.driver, 10,0.2).until_not(EC.presence_of_element_located((By.XPATH, '//*[contains(text(),"待识别模块加载完毕")]')))
                logging.warning('识别模块加载完毕')
            except NoSuchElementException:
                logging.warning('未加载识别模块')

            self.init = True
        res = []
        for pic in pics:
            try:
                logging.warning('开始识别图片:'+pic)
                self.driver.find_element(By.TAG_NAME,'input').send_keys(pic)
                time.sleep(1)
                ui.WebDriverWait(self.driver, 50,0.2).until_not(EC.presence_of_element_located((By.CSS_SELECTOR, '.q-inner-loading.absolute-full')))
                logging.warning('识别成功')

                text = self.driver.find_element(By.CSS_SELECTOR,'.textbox .textItem').get_attribute('value')
                self.driver.find_element(By.XPATH,'//div[@class="BtnBound"]/i[contains(text(),"delete_outline")]').click()
                logging.warning('识别内容：'+text)
                res.append(text)
            except TimeoutException:
                logging.error('识别超时:'+pic)
        return res
        
    def quit(self):
        self.driver.quit()
