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

    for prof in profs:
        # print(prof)
        record = pds.scrape_detail(prof)
        profs_record.append(record)
        # print('Done')
    writeToCSV(profs_record, ['Name', 'Avg Rating', 'Avg Difficulty'], './records.csv')
    writeToCSV(students_review, ['Quality', 'Difficulty', 'Grade', "Comment"], './comments.csv')


def readJson():
    with open('./profs.json') as f:
        profs = json.load(f)
    return profs


def writeToCSV(data, header, path):
    with open(path, 'w') as file:
        writer = csv.DictWriter(file, fieldnames=header)
        writer.writeheader()
        for data_row in data:
            dict_prof = {}
            for i in range(len(header)):
                dict_prof[header[i]] = data_row[i]
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
        grade = 0
        regex_body = re.compile('^Rating__RatingBody.*')
        regex_num = re.compile('^CardNumRating__CardNumRatingNumber.*')
        regex_meta = re.compile('^CourseMeta__StyledCourseMeta.*')
        regex_grade = re.compile('.*Grade.*')
        regex_comment = re.compile('^Comments__StyledComments.*')
        ratings_raw = soup.find_all('div', {'class': regex_body})

        # print(len(ratings_raw))
        for rating_raw in ratings_raw:
            self.review = ['', '', '', '']
            for r in rating_raw.find_all('div', {'class': regex_num}):
                self.review[counter % 2] = r.text
                # if counter % 2 == 1:
                # print(review[0], ' ', review[1], ' ', review[2], ' ', review[3])
                counter = counter + 1
            for r in rating_raw.find('div', {'class': regex_meta}).contents:
                hasGrade = r.find(text=regex_grade)
                if hasGrade:
                    grade = hasGrade.parent.find('span').text
                if len(str(grade)) > 2:
                    grade = 'N/A'
                self.review[2] = grade
            for r in rating_raw.find('div', {'class': regex_comment}):
                self.review[3] = str(r)

            students_review.append(self.review)

        return record


students_review = []
main()
