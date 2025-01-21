from bs4 import BeautifulSoup
import requests
from datetime import datetime

CURRENT_SUPPORT_ONLY=['acsee','csee','ftna']
CURRENT_YEAR = datetime.now().year
def response(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        exit()

def determine_y_url_(studentId:str,level:str)->tuple:
    year=int(studentId.split('/')[2])
    schoolId=studentId.split('/')[0].lower()

    if level.lower() in CURRENT_SUPPORT_ONLY:
        if level.lower() =='csee':
            if year>=2015 and year<=CURRENT_YEAR-2:
                url=f'https://onlinesys.necta.go.tz/results/{year}/csee/results/{schoolId}.htm'
            else:
                print(f"Invalid year. Please choose a year between 2015 and the {CURRENT_YEAR-2}.")
                exit()
        elif level.lower() =='acsee':
            if year>=2014 and year<=CURRENT_YEAR-1:
                url=f'https://onlinesys.necta.go.tz/results/{year}/acsee/results/{schoolId}.htm'
            else:
                print(f"Invalid year. Please choose a year between 2014 and the {CURRENT_YEAR-1}.")
                exit()
        elif level.lower() =='ftna':
            if year>=2024 and year<=CURRENT_YEAR-1:
                url=f'https://matokeo.necta.go.tz/results/{year}/ftna/FTNA{year}/{schoolId.upper()}.htm'
            elif year>=2022 and year<=2023:
                url=f'https://onlinesys.necta.go.tz/results/{year}/ftna/results/{schoolId.upper()}.htm'
            else:
                print(f"We provide only rersult from 2022 and {CURRENT_YEAR-1} for now, for FTNA (Form Two).")
                exit()
        else:
            print("current level not supported, we're working on it")
    return url,year

# print(determine_y_url_('S1144/0501/2024','ftna'))
def table_tr(studentId:str,level:str):
    url,year=determine_y_url_(studentId,level)
    try:
        soup= BeautifulSoup(response(url=url).content,'html.parser')
        table=soup.find_all('table')
        if level=='csee':
            if year >=2015 and year <=2018:
                return table[0].find_all('tr')
            elif year >=2019 and year <= CURRENT_YEAR-1:
                return table[2].find_all('tr')
            else:
                print(f"We support only years between 2014 and {CURRENT_YEAR-1}.")
        elif level=='acsee':
            if year >=2014 and year <=2019:
                return table[0].find_all('tr')
            elif year >=2020 and year <= CURRENT_YEAR-1:
                return table[2].find_all('tr')
            else:
                print(f"We support only years between 2014 and {CURRENT_YEAR-1}.")
        elif level=='ftna':
            if year >=2022 and year <= CURRENT_YEAR-1:
                return table[2]
            # elif year >=2017 and year <= 2021:
            #     return table[0].find_all('tr')
            else:
                print(f"We provide only rersult from 2022 and {CURRENT_YEAR-1} for now, for FTNA (Form Two).")
        else:
            print("current level not supported, we're working on it")
            exit()
    except Exception as e:
        print(f"Error occurred: {e}")

# print(table_tr('P0104/0001/2024','ftna').find_all('tr'))
# with open('results.html','w') as file:
#     file.write(str(table_tr('P0104/0001/2024','ftna')))

def get_headers(studentId:str,level:str):
    """ Get the headers of the table. By accessing the first row of the table."""

    if level == 'ftna':
        header_row = table_tr(studentId,level).find('tr')
        list_headers=[header.get_text(strip=True) for header in header_row.find_all('p')]
    else:
        list_headers=[]
        for iteam in table_tr(studentId,level)[0]:
            try:
                header=iteam.get_text().replace("\n",'').replace("\r",'').strip()
                if header:
                    list_headers.append(header)
            except:
                continue
    return list_headers

# print(get_headers('P0104/0001/2023','csee'))

def get_data(studentId:str,level:str):
    """ Get the data of the table. By accessing the second row .... n row of the table."""
    data=[]
    for element in table_tr(studentId,level)[1:]:
        data_row=[]
        for item in element:
            try:
                row_item=item.get_text().replace("\n",'').replace("\r",'').strip()
                if row_item:
                    data_row.append(row_item)
            except:
                continue
        data.append(data_row)
    return data

def get_data_ftna(studentId:str,level:str):
    '''Geting the data from the ftna table, By accessing the second row .... n row of the table.'''
    header_row = table_tr(studentId,level).find('tr')
    headers=[header.get_text(strip=True) for header in header_row.find_all('p')]
    rows = table_tr(studentId,level).find_all('td')[len(headers):]
    # Group data into rows based on the number of headers
    data = []
    current_row = []
    for cell in rows:
        cell_text = cell.get_text(strip=True)
        current_row.append(cell_text)
        if len(current_row) == len(headers):
            record = tuple(current_row)
            data.append(record)
            current_row = []
    return data

# print(get_data_ftna('P0104/0001/2024','ftna'))

def result_to_truple(studentId:str,level:str)->tuple:
    result=[]
    for row in get_data(studentId,level):
        result.append(tuple(row))
    return result


def searchStudentResults(studentId,results):
    studentId=studentId.split('/')[0]+'/'+studentId.split('/')[1]
    studentId=studentId.upper()
    lo,hi=0,len(results)-1
    while lo<=hi:
        mid=(lo+hi)//2
        if mid>=0 and results[mid][0]==studentId:
            return results[mid]
        elif results[mid][0]<studentId:
            lo=mid+1
        else:
            hi=mid-1
    return (
        'NOT FOUND',
        'NOT FOUND',
        'NOT FOUND',
        'NOT FOUND',
        'NOT FOUND',
    )


def dictStudentResults(studentId:str,level:str)->dict:
    '''return single student results in dictionary format
        {'CNO': 'P0134/0014',
        'SEX': 'F',
        'AGGT': '-',
        'DIV': '0',
        'DETAILED SUBJECTS': "CIV - 'F'   HIST - 'F'   GEO - 'F'   KISW - 'F'   ENGL - 'F'"}
    '''
    headers=get_headers(studentId,level)
    if level=='ftna':
        results=get_data_ftna(studentId,level)
    else:
        results=result_to_truple(studentId,level)
    student_results=searchStudentResults(studentId,results)
    result_dict=dict(
        zip(headers,student_results)
    )
    return result_dict


class Pymatokeo:
    def __init__(self):
       pass
    def matokeo(self,studentId:str,level:str):
        self.studentId=studentId
        self.level=level
        self.headers=get_headers(studentId,level)
        if self.level=='ftna':
            self.results=get_data_ftna(studentId,level)
        else:
            self.results=get_data(studentId,level)
        self.student_results=searchStudentResults(studentId,self.results)
        self.result_dict=dict(
            zip(self.headers,self.student_results)
        )
        return self.result_dict
    def __str__(self):
        return str(self.result_dict)
    def __repr__(self):
        return str(self.result_dict)

if __name__ == '__main__':
    while True:
        level=int(input('level(1. csee/ 2. acsee/ 3. ftna): ').strip())
        studentId=input('student_id(XXXXX/XXXX/XXXX): ').strip()
        if level==1:
            r=Pymatokeo().matokeo(studentId,'csee')
        elif level==2:
            r=Pymatokeo().matokeo(studentId,'acsee')
        elif level==3:
            r=Pymatokeo().matokeo(studentId,'ftna')
        else:
            print("choose a valid level!")
        for i in r:
            print(f'{i}: {r[i]}')
        print('---------------------------------------')
