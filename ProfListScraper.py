import requests
from bs4 import BeautifulSoup
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains


def main():
    prefix = "https://www.ratemyprofessors.com/search/teachers?query=*&sid="
    urls = [prefix + "1413", prefix + "1484", prefix + "1439"]
    pls = ProfListScraper()
    profs = pls.scrape_batch(urls)
    writeToJson(profs)


def writeToJson(profs):
    jString = json.dumps(profs, indent=2)
    jFile = open("profs.json", "w")
    jFile.write(jString)
    jFile.close()


class ProfListScraper:

    def __init__(self):
        self.teacher_list = []

    def scrape_url(self, src):
        soup = BeautifulSoup(src, features="html5lib")
        links = soup.select('a[class*="TeacherCard__StyledTeacherCard"]')
        for link in links:
            teacher = 'https://www.ratemyprofessors.com' + link.attrs['href']
            self.teacher_list.append(teacher)

    def scrape_batch(self, urls):
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--headless')
        driver = webdriver.Chrome()
        driver.maximize_window()

        start_url = urls[0]
        for url in urls:
            driver.get(url)
            # -- For the first visit, RMP.com has a prompt for cookies and privacy policy.
            # -- Need to simulate a click on "Close" before clicking on "Show More", otherwise they may overlap
            if url == start_url:
                driver.implicitly_wait(8)
                driver.find_element_by_css_selector('button[class*="StyledCloseButton"]').click()

            # -- For now, set the number of clicks on "Show More" to be 3, for each school
            # -- This should obtain enough data for analysis purposes
            for i in range(3):
                # driver.execute_script("window.scrollTo(0,2000)")
                element = WebDriverWait(driver, 3).until(
                    EC.element_to_be_clickable((By.CSS_SELECTOR, 'button[class*="PaginationButton"]')))
                ActionChains(driver).move_to_element(element).click().perform()
                # driver.execute_script("arguments[0].click();", button)
                time.sleep(1)

            result = requests.get(url)
            if result.status_code != 200:
                print("error: status code " + str(result.status_code))
                break
            print(result.status_code)
            src = driver.page_source
            # driver.quit()
            self.scrape_url(src)

        return self.teacher_list


main()
