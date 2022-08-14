import requests
import pandas as pd

TOTAL_PROGRAM = 1118411  # Total number of programs, listed in the website
PAGE_LIMIT = 25  # Number of programs per page, max is 25
BASE_URL = 'https://www.topuniversities.com/program/endpoint'
CSV_OUTPUT = 'uniprograms.csv'

# prepare list to store data
program_output = []

# loop through each page
# limiting to 500 pages for now
for i in range(TOTAL_PROGRAM//PAGE_LIMIT+1)[:500]:
    # construct page code
    page_code = f'?page=[{i}]&pagerlimit=[{PAGE_LIMIT}]'
    page_url = BASE_URL + page_code
    # get page data
    page_request = requests.get(page_url)
    # parse page data
    program_data = page_request.json()['data']

    # loop through each uni program
    for program in program_data:
        try:
            # get program details
            program_output.append({
                'University' : program['uni_name'],
                'Program' : program['program_name'],
                'Study Level' : program['program_attributes']['Study Level'],
                'Country' : program['country'][0],
                'Official Website' : program['uni_website'],
            })
        except IndexError:
            # program has no country
            program_output.append({
                'University' : program['uni_name'],
                'Program' : program['program_name'],
                'Study Level' : program['program_attributes']['Study Level'],
                'Country' : '',
                'Official Website' : program['uni_website'],
            })
        except KeyError:
            # program has no study level
            program_output.append({
                'University' : program['uni_name'],
                'Program' : program['program_name'],
                'Study Level' : '',
                'Country' : program['country'],
                'Official Website' : program['uni_website'],
            })

# store data in csv file
program_df = pd.DataFrame(program_output)
program_df.to_csv(CSV_OUTPUT, index=False)
