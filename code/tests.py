import os
import unittest

import scraper

class TestScraper(unittest.TestCase):

    def setUp(self):
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        self.csvPath = os.path.join(scriptDir, "test_data", "codepoint.csv")
        htmlPath = os.path.join(scriptDir, "test_data", "generationmap.html")
        with open(htmlPath, "r") as f:
             self.htmlString = unicode(f.read())

    def test_csvToList(self):
        postcodeList = ["CF101AA", "CF101AB"]
        self.assertEqual(
            scraper.csvToList(self.csvPath, startswithstring="CF10"),
            postcodeList
        )

    def test_getHTML(self):
        postcode = "CF101AA"
        self.assertTrue('<div class="location">' in scraper.getHTML(postcode))

    def test_extractDataFromHTML(self):
        data = [
            {
                u"name": u"BAKERS ROW",
                u"Voltage": u"11 kV",
                u"Capacity at substation": u"5000 kW",
                u"Capacity 1km from substation": u"5000 kW",
                u"Substation ID": u"512615",
                u"Lat": 51.4793281555176,
                u"Lon": -3.177579164505
            }, {
                u"name": u"NEW DAVID MORGAN",
                u"Voltage": u"11 kV",
                u"Capacity at substation": u"5000 kW",
                u"Capacity 1km from substation": u"5000 kW",
                u"Substation ID": u"513554",
                u"Lat": 51.4792747497559,
                u"Lon": -3.17744898796082
            }
        ]
        self.assertEqual(scraper.extractDataFromHTML(self.htmlString), data)

    def test_extractLatLngFromJS(self):
        coordinates = {
            "BAKERS ROW": (51.4793281555176, -3.177579164505),
            "NEW DAVID MORGAN": (51.4792747497559, -3.17744898796082)
        }
        self.assertEqual(
            scraper.extractLatLngFromJS(self.htmlString), coordinates
        )

if __name__ == '__main__':
    unittest.main()
