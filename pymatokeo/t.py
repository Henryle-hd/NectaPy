from main import Pymatokeo
while True:
        level=int(input('level(1. csee/ 2. acsee/ 3. ftna / 4. sfna): ').strip())
        studentId=input('student_id(XXXXX/XXXX/XXXX): ').strip()
        if level==1:
            r=Pymatokeo().matokeo(studentId,'csee')
        elif level==2:
            r=Pymatokeo().matokeo(studentId,'acsee')
        elif level==3:
            r=Pymatokeo().matokeo(studentId,'ftna')
        elif level==4:
            r=Pymatokeo().matokeo(studentId,'sfna')
        else:
            print("choose a valid level!")
        for i in r:
            print(f'{i}: {r[i]}')
        print('---------------------------------------')