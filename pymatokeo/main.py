from bs4 import BeautifulSoup
import requests
from datetime import datetime

def response(year,schoolId,current_year):
    try:
        if year>=2015 and year<=current_year-2:
            url=f'https://onlinesys.necta.go.tz/results/{year}/csee/results/{schoolId}.htm'
            response=requests.get(url)
            response.raise_for_status()
            return response
        else:
            print(f"Invalid year. Please choose a year between 2015 and the {current_year-2}.")
            exit()
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")

def table_tr(studentId:str):
    current_year = datetime.now().year
    year=int(studentId.split('/')[2])
    schoolId=studentId.split('/')[0].lower()
    try:
        soup= BeautifulSoup(response(year,schoolId,current_year).content,'html.parser')
        table=soup.find_all('table')
        if year >=2015 and year <=2018:
            return table[0].find_all('tr')
        elif year >=2019 and year <= current_year-1:
            return table[2].find_all('tr')
        else:
            print("Invalid year. Please choose a year between 2015 and the current year.")
    except Exception as e:
        print(f"Error occurred: {e}")



def get_headers(studentId:str):
    list_headers=[]
    for iteam in table_tr(studentId)[0]:
        try:
            header=iteam.get_text().replace("\n",'').replace("\r",'').strip()
            if header:
                list_headers.append(header)
        except:
            continue
    return list_headers

# print(get_headers(studentId))

def get_results(studentId:str):
    result=[]
    for element in table_tr(studentId)[1:]:
        result_row=[]
        for item in element:
            try:
                row_item=item.get_text().replace("\n",'').replace("\r",'').strip()
                if row_item:
                    result_row.append(row_item)
            except:
                continue
        result.append(result_row)
    return result
# print(get_results(studentId))

def result_to_truple(studentId):
    result=[]
    for row in get_results(studentId):
        # cno=row[0]
        # sex=row[1]
        # aggt=row[2]
        # div=row[3]
        # subjects=row[4].split('-')
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
    return ""


def dictStudentResults(studentId):
    heandes=get_headers(studentId)
    results=result_to_truple(studentId)
    student_results=searchStudentResults(studentId,results)
    result_dict=dict(
        zip(heandes,student_results)
    )
    return result_dict


def ffour_r(studentId):
    st_r=dictStudentResults(studentId)
    if st_r =='':
        print('Not found')
    else:
        for key, value in st_r.items():
            print(f'{key}: {value}')

if __name__ == '__main__':
    while True:
        studentId=input('student_id(XXXXX/XXXX/XXXX): ').strip()
        ffour_r(studentId)

