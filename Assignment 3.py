# Assignment 3
# By Joshua Rifkin


import requests
import csv
import re
import datetime

hours = {0: 0, 1: 0, 2: 0, 3: 0,
         4: 0, 5: 0, 6: 0, 7: 0,
         8: 0, 9: 0, 10: 0, 11: 0,
         12: 0, 13: 0, 14: 0, 15: 0,
         16: 0, 17: 0, 18: 0, 19: 0,
         20: 0, 21: 0, 22: 0, 23: 0, }


def downloadData(url):

    file = requests.get(url)
    csvFile = file.content.decode()

    return csvFile


def processData(data):
    lines = 0
    images = 0
    browsers = {'Firefox': 0,
                'Google Chrome': 0,
                'Internet Explorer': 0,
                'Safari': 0}

    file = csv.reader(data.splitlines())

    for line in file:
        lines += 1
        if re.search('jpe?g|JPE?G|gif|GIF|png|PNG', line[0]):
            images += 1

        if re.search("Firefox", line[2]):
            browsers['Firefox'] += 1
        elif re.search("Chrome", line[2]):
            browsers['Google Chrome'] += 1
        elif re.search("MSIE", line[2]):
            browsers['Internet Explorer'] += 1
        elif re.search("Safari[^Chrome]", line[2]):
            browsers['Safari'] += 1

        extraCredit(line)

    print("Files that are images: " + str(images))
    imagePct = float((images / lines) * 100)
    print("Image requests account for {}% of all requests".format(imagePct))

    for browser in browsers:
        print(browser + " usage: " + str(browsers[browser]))

    topB = max(browsers, key=browsers.get)
    print("{} is the most popular broswer with {} uses.".format(topB, browsers[topB]))

    for hour in hours:
        print("Hour {} has {} hits.".format(hour, hours[hour]))


def extraCredit(line):
    hour = (datetime.datetime.strptime(line[1], "%Y-%m-%d %H:%M:%S")).hour

    hours[hour] += 1


def main():
    try:
        # Pull file from internet
        # URL: http://s3.amazonaws.com/cuny-is211-spring2015/weblog.csv
        source = input('File Source: ')
        csvData = downloadData(source)
    except ValueError:
        print('Invalid URL.')
        exit()

    processData(csvData)


if __name__ == '__main__':
    main()
