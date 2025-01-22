from main import Pymatokeo
while True:
        level=input('level(csee/acsee/ftna/sfna/psle/gatce/dsee/gatscce): ').strip()
        studentId=input('student_id(XXXXX/XXXX/XXXX): ').strip()
        r=Pymatokeo().matokeo(studentId,level)
        for i in r:
            print(f'{i}: {r[i]}')
        print('---------------------------------------')