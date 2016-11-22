scraper.py:
- Gets list of postcodes from OS Code-Point
- Searches for each postcode on https://www.westernpower.co.uk/Connections/Generation/Generation-Capacity-Map/Distributed-Generation-Map.aspx, gets HTML response back
- Extracts substation coordinates and attributes from HTML
- Outputs data to csv file

tests.py
- Unit tests for scraper.py

test_data
- mock data for test cases in tests.py
