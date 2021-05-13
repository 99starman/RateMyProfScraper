import requests
from bs4 import BeautifulSoup
import re
import json
import csv


def main():
    review = []
    pds = ProfDetailScraper(review)
    profs = readJson()
    profs_record = []
    students_review = []
    for prof in profs:
        # print(prof)
        profs_record.append(pds.scrape_detail(prof))
        # print('Done')
    writeRecordToCSV(profs_record)


def readJson():
    with open('./profs.json') as f:
        profs = json.load(f)
    return profs


def writeRecordToCSV(profs_record):
    with open('./records.csv', 'w') as file:
        header = ['Name', 'Avg Rating', 'Avg Difficulty']
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for record in profs_record:
            dict_prof = {'Name': record[0], 'Avg Rating': record[1], 'Avg Difficulty': record[2]}
            writer.writerow(dict_prof)


def selectAttribute(soup, identifier):
    attribute = []
    attribute_raw = soup.select(identifier)
    for i in attribute_raw:
        if len(i.text) != 0:
            attribute.append(i.text)
    return attribute[-1]


class ProfDetailScraper:

    def __init__(self, review):
        self.review = review

    # def selectReview(self):

    def scrape_detail(self, prof):
        result = requests.get(prof)
        # print(result.status_code)
        src = result.content
        soup = BeautifulSoup(src, 'html.parser')

        # get prof name
        name = selectAttribute(soup, 'div[class*="NameTitle__Name"]')
        # get average rating
        rating = selectAttribute(soup, 'div[class*="RatingValue__Numerator"]')
        # get average difficulty
        difficulty = selectAttribute(soup, 'div[class*="FeedbackItem__FeedbackNumber"]')

        record = [name, rating, difficulty]
        # print(record[0], " ", record[1], " ", record[2])

        counter = 0
        review = ['', '', '', '']
        regex_body = re.compile('^Rating__RatingBody.*')
        regex_num = re.compile('^CardNumRating__CardNumRatingNumber.*')
        ratings_raw = soup.find_all('div', {'class': regex_body})
        # print(len(ratings_raw))
        for rating_raw in ratings_raw:
            for r in rating_raw.find_all('div', {'class': regex_num}):
                review[counter % 2] = r.text
                # if counter % 2 == 1:
                # print(review[0], ' ', review[1], ' ', review[2], ' ', review[3])
                counter = counter + 1

        return record


main()
