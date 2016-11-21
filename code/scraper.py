import csv
import os

import mechanize
from bs4 import BeautifulSoup

def csvToList(csvPath, startswithstring=""):
    ''' Returns a list of postcodes from a codepoint csv file.'''
    postcodes = []
    with open(csvPath, "rb") as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            postcode = row[0]
            if postcode.startswith(startswithstring):
                postcodes.append(postcode)
    return postcodes

def getHTML(postcode):
    url = "https://www.westernpower.co.uk/Connections/Generation/Generation-Capacity-Map/Distributed-Generation-Map.aspx"
    browser = mechanize.Browser()
    browser.set_handle_robots(False)
    browser.open(url)
    browser.select_form(nr=0)
    browser.form["ctl00$plcMain$plcZones$lt$DistributionMap2$tbSearch"] = postcode
    response = browser.submit()

    return response.get_data()


def extractDataFromHTML(htmlString):
    soup = BeautifulSoup(htmlString, "html.parser")
    data = []
    for location in soup.find_all("div", class_="location"):
        dataDict = {}
        dataDict[u"name"] = location.h2.string
        for strongTag in location.find_all("strong"):
            k = strongTag.string.replace(":", "")
            v = strongTag.next_sibling.strip()
            if k != "Distance from search point":
                dataDict[k] = v
        data.append(dataDict)
    return data


if __name__ == '__main__':
    # Input paths
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    csvPath = os.path.abspath(os.path.join(
        scriptDir,
        "..",
        "data",
        "codepoint_1589995",
        "two_letter_pc_code",
        "cf.csv"
    ))

    # Get list of postcodes
    postcodes = csvToList(csvPath, "CF34")
