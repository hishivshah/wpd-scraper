import os
import unittest

import scraper

class TestScraper(unittest.TestCase):

    def test_csvToList(self):
        scriptDir = os.path.dirname(os.path.abspath(__file__))
        csvPath = os.path.join(scriptDir, "test_data", "codepoint.csv")
        postcodeList = ["CF101AA", "CF101AB"]
        self.assertEqual(
            scraper.csvToList(csvPath, startswithstring="CF10"),
            postcodeList
        )

    def test_getHTML(self):
        postcode = "CF101AA"
        self.assertTrue('<div class="location">' in scraper.getHTML(postcode))

    def test_extractDataFromHTML(self):
        htmlString = unicode("""
            <!DOCTYPE html>
            <html>
            <head>
            <meta charset="UTF-8">
            <title>test html</title>
            </head>
            <body>
            <div class="locations" style="overflow-y:scroll; height:600px;">
                <div class="location">
                    <h2>BRIDGE ST</h2>
                    <div class="details">
                        <p><strong>Voltage:</strong> 11 kV</p>
                        <p><strong>Capacity at substation:</strong> 310 kW</p>
                        <p><strong>Capacity 1km from substation:</strong> 300 kW</p>
                        <p><strong>Substation ID:</strong> 563353</p>
                        <p><strong>Distance from search point:</strong> 0.15 Km</p>
                    </div>
                </div>
                <div class="location">
                    <h2>CWMDU ST</h2>
                    <div class="details">
                        <p><strong>Voltage:</strong> 11 kV</p>
                        <p><strong>Capacity at substation:</strong> 310 kW</p>
                        <p><strong>Capacity 1km from substation:</strong> 300 kW</p>
                        <p><strong>Substation ID:</strong> 563354</p>
                        <p><strong>Distance from search point:</strong> 0.16 Km</p>
                    </div>
                </div>
            </div>
            </bodY>
            </html>
        """)
        data = [
            {u"name": u"BRIDGE ST", u"Voltage": u"11 kV", u"Capacity at substation": u"310 kW", u"Capacity 1km from substation": u"300 kW", u"Substation ID": u"563353"},
            {u"name": u"CWMDU ST", u"Voltage": u"11 kV", u"Capacity at substation": u"310 kW", u"Capacity 1km from substation": u"300 kW", u"Substation ID": u"563354"}
        ]
        self.assertEqual(scraper.extractDataFromHTML(htmlString), data)

if __name__ == '__main__':
    unittest.main()
