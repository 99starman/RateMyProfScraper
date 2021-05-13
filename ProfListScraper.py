import requests
from bs4 import BeautifulSoup
import time
import json


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

    def scrape_url(self, result):
        src = result.content
        soup = BeautifulSoup(src, features="html5lib")
        links = soup.select('a[class*="TeacherCard__StyledTeacherCard"]')
        for link in links:
            teacher = 'https://www.ratemyprofessors.com' + link.attrs['href']
            self.teacher_list.append(teacher)

    def scrape_batch(self, urls):
        for url in urls:
            result = requests.get(url)
            if result.status_code != 200:
                print("error: status code " + str(result.status_code))
                break
            # print(result.status_code)
            self.scrape_url(result)
            time.sleep(1)
        return self.teacher_list


main()
