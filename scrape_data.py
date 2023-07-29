#!/usr/bin/env python3

import pathlib
import requests
import re
import bs4
# import os
import sqlite3

current_dir = pathlib.Path(__file__).parent.resolve()

regex = r"faculty_main_page\.php\?id=(\d+)"

departments = {1: 'applied_science_and_humanities', 2: 'computer_science_and_engineering', 3: 'electrical_engineering', 4: 'electronics_and_telecommunication', 5: 'information_technology', 6: 'mechanical_engineering', 7: 'business_administration'}
table_header = ('name_designation_contact', 'qualification', 'area_of_specialization', 'experience', 'courses_taught', 'membership', 'publications', 'research_and_development', 'fellowship_award', 'other')


conn = sqlite3.connect(current_dir / 'faculties.db')
cursor = conn.cursor()











for i in [2, 4, 1, 3, 5, 6, 7]:    # range(1, 8)
    dept = departments[i]

    cursor.execute(f'''CREATE TABLE {dept} (name_designation_contact TEXT, qualification TEXT, area_of_specialization TEXT, experience TEXT, courses_taught TEXT, membership TEXT, publications TEXT, research_and_development TEXT, fellowship_award TEXT, other TEXT)''')
    
    res = requests.get(f'https://www.ssgmce.ac.in/faculty_page_all_dept.php?department_id={i}')
    matches = re.finditer(regex, res.text)
    for m in matches:
        x = m.group(1)
        res = requests.get(f'https://www.ssgmce.ac.in/faculty_main_page.php?id={x}')
        soup = bs4.BeautifulSoup(res.text, 'html.parser')
        for br in soup.find_all('br'):
            br.append('\n')
        
        table = soup.find('table')
        name = table.find('h2').text.strip()
        row = [tr.find_all('td')[1].text.encode('ascii', 'ignore').strip().decode().replace('\n', '; ').replace('\r', '; ').replace("'", "") for tr in table.find_all('tr')]
        row[0] = row[0].replace(name, f'{name}; ')
        
        #### print('please generate a list of pre-defined questions and answers for trainning the chatterbot bot for the following data. (please try to cover all possible question types, keep questions simple and do not frame question and answer with "no", "not" or other negative words)')
        #### print(f'department: "{dept.replace("_", " ")}"')
        #### for a, b in zip(table_header, row):
        ####     print(f'{a}: "{b}"')
        #### input('Waiting for command...')
        #### os.system('clear')

        cursor.execute(f'INSERT INTO {dept} (name_designation_contact, qualification, area_of_specialization, experience, courses_taught, membership, publications, research_and_development, fellowship_award, other) VALUES {tuple(row)}')

conn.commit()
conn.close()        

# https://inloop.github.io/sqlite-viewer/
