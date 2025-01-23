from bs4 import BeautifulSoup
import requests
from datetime import datetime
from typing import Literal


CURRENT_SUPPORT_ONLY=['acsee','csee','ftna','sfna','psle','gatce','dsee','gatscce']
CURRENT_YEAR = datetime.now().year
def response(url):
    try:
        response=requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        # print(f"Error occurred: {e}")
        return "error", {e}

def determine_y_url_(studentId:str,level:str)->tuple:
    ''' Takes a student id and level, returns a tuple containing right url based on studentID and the year.'''
    year=int(studentId.split('/')[2])
    schoolId=studentId.split('/')[0].lower()

    if level.lower() in CURRENT_SUPPORT_ONLY:
        if level.lower() =='csee':
            if year>=2024 and year<CURRENT_YEAR:
                url=f"https://matokeo.necta.go.tz/results/{year}/csee/CSEE{year}/CSEE{year}/results/{schoolId}.htm"
            elif year>=2015 and year<=CURRENT_YEAR-2:
                url=f'https://onlinesys.necta.go.tz/results/{year}/csee/results/{schoolId}.htm'
            else:
                return "error",f"Invalid year. Please choose a year between 2015 and the {CURRENT_YEAR-1}."
        elif level.lower() =='acsee':
            if year>=2014 and year<=CURRENT_YEAR-1:
                url=f'https://onlinesys.necta.go.tz/results/{year}/acsee/results/{schoolId}.htm'
            else:
                return "error",f"Invalid year. Please choose a year between 2014 and the {CURRENT_YEAR-1}."
        elif level.lower() =='ftna':
            if year>=2024 and year<=CURRENT_YEAR-1:
                url=f'https://matokeo.necta.go.tz/results/{year}/ftna/FTNA{year}/{schoolId.upper()}.htm'
            elif year>=2022 and year<=2023:
                # Later the start year will be 2017
                url=f'https://onlinesys.necta.go.tz/results/{year}/ftna/results/{schoolId.upper()}.htm'
            else:
                return "error",f"We provide only rersult from 2022 and {CURRENT_YEAR-1} for now, for FTNA (Form Two)."
        elif level.lower() =='sfna':
            if year>=2024 and year < CURRENT_YEAR:
                url=f'https://matokeo.necta.go.tz/results/{year}/sfna/SFNA{year}/{schoolId}.htm'
            elif year>=2022 and year<=2023:
                url=f'https://onlinesys.necta.go.tz/results/{year}/sfna/results/{schoolId}.htm'
            else:
                return "error",f"We provide only rersult from 2017 and {CURRENT_YEAR-1} for now, for SFNA (S.Four)."
        elif level.lower() =='psle':
            if year>=2016 and year<CURRENT_YEAR:
                url=f'https://onlinesys.necta.go.tz/results/{year}/psle/results/shl_{schoolId}.htm'
            else:
                return "error",f"We provide only rersult from 2016 and {CURRENT_YEAR-1} for now, for PSLE (S.Four)."
        elif level.lower() =='gatce' or level.lower() =='dsee' or level.lower() =='gatscce':
            schoolId=schoolId[2:]
            if year >=2019 and year <= CURRENT_YEAR-1:
                url=f'https://onlinesys.necta.go.tz/results/{year}/{level.lower()}/results/{schoolId}.htm'
            else:
                return "error",f"We support only years between 2019 and {CURRENT_YEAR-1}."
        else:
            return "error","current level not supported, we're working on it"
    return url,year

# print(determine_y_url_('E0544/0001/2024','gatscce'))
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
        elif level=='acsee':
            if year >=2014 and year <=2019:
                return table[0].find_all('tr')
            elif year >=2020 and year <= CURRENT_YEAR-1:
                return table[2].find_all('tr')
        elif level=='ftna':
            if year >=2022 and year <= CURRENT_YEAR-1:
                return table[2]
            # elif year >=2017 and year <= 2021:
            #     return table[0].find_all('tr')
        elif level=='sfna':
            return table[2].find_all('tr')
        elif level=='psle':
            if year >=2019 and year <= CURRENT_YEAR-1:
                return table[1].find_all('tr')
            elif year >=2016 and year <= 2018:
                tr=soup.find_all('tr')
                return tr
        elif level.lower() =='gatce' or level.lower() =='dsee' or level.lower() =='gatscce':
            if year >=2019 and year <= CURRENT_YEAR-1:
                return table[0].find_all('tr')
    except Exception as e:
        return "error", {e}

# testing
# print(table_tr('E0544/0001/2024','gatscce'))
# with open('results.html','w') as file:
#     file.write(str(table_tr('P0104/0001/2024','ftna')))

def get_headers(studentId:str,level:str):
    """ Get the headers of the table. By accessing the first row of the table."""
    year=int(studentId.split('/')[2])
    if level == 'ftna':
        header_row = table_tr(studentId,level).find('tr')
        list_headers=[header.get_text(strip=True) for header in header_row.find_all('p')]
    elif level == 'psle' and year<=2018:
        list_headers=['CAND.NO','SEX','CANDIDATE NAME','SUBJECTS']
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
                if level=='sfna' or level=='psle':
                    row_item=row_item.replace("-","/")
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
    '''return single student results in dictionary format'''
    error,sms=determine_y_url_(studentId,level)
    if error=='error':
        return {'error':sms}
    else:
        url,year=determine_y_url_(studentId,level)
    if type(response(url)) is tuple:
        error,sms=response(url)
        return {'error':sms}
    headers=get_headers(studentId,level)
    if level=='ftna':
        results=get_data_ftna(studentId,level)
    else:
        results=result_to_truple(studentId,level)
    student_results=searchStudentResults(studentId,results)
    result_dict=dict(zip(headers,student_results))
    return result_dict


# print(dictStudentResults('s3266/0064/2024','csee'))
class Necta:
    # def __init__(self):
    #     pass
    def st_result(self,studentId:str,level:Literal['sfna','psle','ftna','csee','acsee','gatce','dsee','gatscce'])->dict:
        """Get student examination results from NECTA.
    Args:
        studentId (str): Student ID in format 'XXXXX/XXXX/YYYY' where YYYY is the year
        Example: 'S4177/0003/2023'
        level (str): Examination level, one of:
                    - 'sfna' (Standard 2, 2017-2024)
                    - 'psle' (Standard 7, 2016-2024)
                    - 'ftna' (Form 2, 2022-2024)
                    - 'csee' (Form 4, 2015-2024)
                    - 'acsee' (Form 6, 2014-2024)
                    - 'gatce' (College, 2019-2024)
                    - 'dsee' (College, 2019-2024)
                    - 'gatscce' (College, 2019-2024)
    Returns:
        dict: Student results with headers as keys and results as values
            Example: {
                "CNO": "XXXX/0003",
                "PReM NO": "xxxxxxx"
                "CANDIDATE NAME": "XXXXX XXXXX XXXXX",
                "SEX": "F",
                "AGGT": "18",
                "DIV": "II",
                "DETAILED SUBJECTS": "CIV-'D' HIST-'C' GEO-'B' KISW-'C' ENGL-'B' PHY-'D' CHEM-'B' BIO-'C' B/MATH-'C'"
            }
    """
        self.result=dictStudentResults(studentId,level)
        return self.result
    def __str__(self):
        return str(self.result)
    def __repr__(self):
        return str(self.result)

if __name__ == '__main__':
    while True:
        level=input('(csee/acsee/ftna/sfna/psle/gatce/dsee/gatscce): ').strip()
        studentId=input('STUDENT ID (XXXXX/XXXX/XXXX): ').strip()
        r=Necta().st_result(studentId,level)
        for i in r:
            print(f'{i}: {r[i]}')
        print('---------------------------------------')
