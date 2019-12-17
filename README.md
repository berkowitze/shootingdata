## School shooting - Advanced Econometrics Final Project

Instructions to reproduce:
1. With NodeJS, run `scrape.js`: `node scrape.js`
This will go through `all_ids.json` one NCES ID at a time and download the page as HTML, putting all the .html files into `out/html`.
2. With Python, run `scrape.py`: `python scrape.py`.
This goes through all the html files and extracts the relevant data into JSON format, putting the JSON files into `out/data`. To extract other information, modify this script. This script uses multiprocessing to go faster, so be aware it will chunk your CPU for a while.
3. Run `python collect.py` to join all the data into a single table.

The data in data.tsv has been significantly cleaned from the output of `collect.py`, giving consistent datatypes to the columns, making columns blank where appropriate, removing invalid rows with student-to-teacher ratios over 200, etc.
