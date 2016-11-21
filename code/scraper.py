import csv
import os
import re

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

def extractLatLngFromJS(htmlString):
    coordinates = {}

    expression = '\{\s*?' \
    + 'title: "Name: (.*?)",\s*?' \
    + 'position: new google.maps.LatLng\((.*?),(.*?)\),\s*?' \
    + 'icon: "/App_Themes/WPD/images/buttons/location-marker.png"\s*?' \
    + '\}'
    regex = re.compile(expression)

    soup = BeautifulSoup(htmlString, "html.parser")
    for script in soup.find_all("script", attrs={"type": "text/javascript"}):
        results = regex.findall(script.string)
        for r in results:
            name = r[0]
            lat = float(r[1])
            lon = float(r[2])
            coordinates[name] = (lat, lon)

    return coordinates

if __name__ == '__main__':
    # Input paths
    scriptDir = os.path.dirname(os.path.abspath(__file__))
    codepointCsvPath = os.path.abspath(os.path.join(
        scriptDir,
        "..",
        "data",
        "codepoint_1589995",
        "two_letter_pc_code",
        "cf.csv"
    ))
    # Output paths
    outCsvPath = os.path.abspath(
         os.path.join(scriptDir, "..", "results", "substations.csv")
    )

    # Get list of postcodes
    postcodes = csvToList(codepointCsvPath, "CF340A")

    # Scrape data for each postcode
    data = []
    for postcode in postcodes:
        html = getHTML(postcode)
        data += extractDataFromHTML(html)

    # Remove duplicates
    data = [dict(t) for t in set([tuple(sorted(d.items())) for d in data])]

    # Write to csv
    with open(outCsvPath, "wb") as outCsv:
        fieldnames = [
            "Substation ID",
            "name",
            "Voltage",
            "Capacity at substation",
            "Capacity 1km from substation"
        ]
        writer = csv.DictWriter(outCsv, fieldnames)
        writer.writeheader()
        writer.writerows(data)
