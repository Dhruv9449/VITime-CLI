from .Slotdata import *
from datetime import datetime
from .initialize import *
import click
import re

def savecourse(Course):
    Course.type = Course.slots[0][0]
    if Course.type == 'L':
        Course.type = 'P'
    else :
        Course.type = 'L'

    if Course.type == "L":
        daysTL = daysTh
        days = list(daysTL.keys())
        times = thSlots
        allslots = theoryslots
    else:
        daysTL = daysLb
        days = list(daysTL.keys())
        times = lbSlots
        allslots = labslots

    for slot in Course.slots:
        if slot not in allslots:
            print(f"\nInvalid slots entered for {Course.code}! Please enter valid slots.\nCourse not added!")
            return False

    for slot in Course.slots:
        for day in daysTL:
            dt = {}
            dt[day]=[]
            daysl = daysTL[day]
            if slot in daysl:
                for i in range(len(daysl)):
                    if slot == daysl[i]:
                        time = times[i]
                        dt[day].append(time)
                        coursedetails = [time, Course.code, Course.name, slot, Course.type]
                        d1 = loadday(day)
                        d1.schedule.append(coursedetails)
                        d1.schedule.sort()
                        addschedule_db(d1)
    addcourse_db(Course)
    return True





@click.group(cls=CustomGroup, context_settings=help)
def vitime():
    pass

@vitime.command()
@click.pass_context
def addtimetable(ctx):
    '''
    Add your timetable and delete existing one.
    '''
    if ctx.invoke(deletetimetable):
        print("Please type 'yes' to delete existing timetable and add new one!")
        return

    print("-"*50)
    text = retrieveinput()
    if text == False:
        return
    print("\n"+"-"*50)

    data = scrape(text)
    if len(data)==0:
        print("\nInvalid input! Please try again with a valid input or use the addcourse command to add courses manually.")
        print("\nFor more detailed help on how to add timetable check -\n  https://github.com/Dhruv9449/VITime-CLI#vitime-addtimetable\n")
        return

    for i in data :
        Course = course()
        Course.code = i[0]
        Course.name = i[1]
        Course.slots = i[2]
        if Course.slots[0]=="NIL":
            continue
        if checkcourse(Course):
            continue
        if not savecourse(Course):
            continue
        print(f"{Course.code} added!")

    print('\nTimetable added!\n')



@vitime.command(cls=CustomCommand)
def showcourses():
    '''
    Shows all courses.
    '''
    print("             VITIME\n")
    cursor.execute("SELECT code, name, type, slots FROM Courses")
    courses = cursor.fetchall()
    if courses == []:
        print("No courses! Empty timetable!")
    for i in range(len(courses)):
        if courses[i][2] == 'L':
            type = '  [Theory] '
        else:
            type = '   [Lab]    '
        print(i+1, courses[i][0] + " - "+ courses[i][1])
        print(type, f"({'+'.join(eval(courses[i][3]))})")
        print()



@vitime.command(cls=CustomCommand)
def addcourse():
    '''
    Adds courses to your time table.
    '''
    print("             VITIME")
    while True:
        Course = course()
        Course.code = input("\nEnter course code : ").upper()
        if len(Course.code)<5:
            print("\nInvalid course code, please enter a valid course code.(eg - BCHY101L/CSE1002)\n")
            return
        Course.name = input("Enter course name : ")
        Course.slots = input("Please enter course slots (eg- E2+TE2) : ").upper().split("+")

        if checkcourse(Course):
            return

        check = savecourse(Course)
        if check:
            print("\nSuccessfully added course!")
        opt = input("\nDo you want to add more courses (y/n) : ").lower()[:1]
        if opt == "n":
            break
            print()



@vitime.command(cls=CustomCommand)
def deletecourse():
    '''
    Deletes a course from the timetable.
    '''
    print("             VITIME")
    cursor.execute("SELECT code, name, type, slots FROM Courses")
    courses = cursor.fetchall()
    cursor.execute("SELECT schedule FROM Schedules")
    days = cursor.fetchall()
    if len(courses) == 0 :
        print("\nYou've got no courses!")
        return
    print("Courses\n")
    for i in range(len(courses)):
        if courses[i][2] == 'L':
            type = '  [Theory] '
        else:
            type = '   [Lab]    '
        print(i+1, courses[i][0] + " - "+ courses[i][1])
        print(type, f"({'+'.join(eval(courses[i][3]))})")
        print()
    deletecourse = input(("Input enter the sno of course to be deleted from above : "))
    if not deletecourse.isdigit():
        print("\nPlease enter a valid number!")
        return
    deletecourse = int(deletecourse)
    if deletecourse>len(courses) or deletecourse<1:
        print("\nInvalid option plese enter valid option!")
        return
    courses = courses[deletecourse-1]
    coursecode, courseslot = courses[0], courses[3]
    courses = coursecode, courseslot
    cursor.execute("DELETE FROM Courses WHERE code = ? AND slots = ?", courses)
    for i in days:
        i = eval(i[0])
        k = list(i)
        for j in i:
            if j[1] == coursecode :
                k.remove(j)
        cursor.execute("UPDATE Schedules SET schedule = ? WHERE schedule = ?",
                        (str(k), str(i)))
    mycon.commit()
    print(f"\nCourse {coursecode} deleted!\n")



@vitime.command(cls=CustomCommand)
def deletetimetable():
    '''
    Deletes entire timetable including all courses.
    '''
    print("             VITIME")
    confirm = input("""\nAre you sure you want to clear all the contents of the existing timetable?
This step is irreversible. Type "yes" to confirm : """)

    if confirm != "yes" :
        print("\nTimetable not deleted, if you want to delete the timetable try again!\n")
        return True
    cursor.execute("DROP TABLE Schedules")
    cursor.execute("DROP TABLE Courses")
    initialize()
    mycon.commit()
    print("\nDeleted timetable!\n")



@vitime.command(cls=CustomCommand)
@click.option('-n', '--name', required=True, type = str,
              prompt = "Enter the day ", help = "Specifies the name of day")
def showday(name):
    '''
    Shows the timetable for the given day.
    '''
    print("             VITIME")
    Day = name.lower()
    if Day not in days :
        print("\nPlease enter a working day (eg - monday - friday)!\n")
        return
    cursor.execute("SELECT schedule FROM Schedules WHERE day = ?",(Day,))
    timetable = eval(cursor.fetchone()[0])
    print(f"\nDay's schedule : {Day}")
    if timetable == [] :
        print("No classes on this day!\n")
        return
    print()
    for i in timetable:
        print(i[1])
        print(i[2])
        print(f"Course type : {checktype(i[4])}")
        print(f"Slot : {i[3]}")
        print(f"Time : {i[0]}\n")
    print()



@vitime.command(cls=CustomCommand)
def today():
    '''
    Show's today's timetable and the classes left.
    '''
    print("             VITIME\n")
    d, time = datetime.now().strftime("%A %H:%M").lower().split()
    if d in ["saturday","sunday"] :
        print("It's holiday! Have fun!\n")
        return
    cursor.execute("SELECT schedule FROM Schedules WHERE day = ?",(d,))
    timetable = eval(cursor.fetchall()[0][0])
    ongoing = False
    for i in range(len(timetable)):
        end = timetable[i][0].split()[2]
        if end<time:
            continue
        else:
            start = timetable[i][0].split()[0]
            if start < time:
                ongoing = True
            timetable = timetable[i:]
            break
    else:
        timetable = []

    print("Today's Timetable :  Classes left\n")
    if timetable == []:
        print("No classes left to attend today!\n")
        return
    if ongoing:
        print("-> Ongoing!")
    else:
        print("-> Next class")
    for i in timetable:
        print(i[1])
        print(i[2])
        print(f"Course type : {checktype(i[4])}")
        print(f"Slot : {i[3]}")
        print(f"Time : {i[0]}\n")
    print()



@vitime.command(cls=CustomCommand)
def full():
    '''
    Shows the full timetable for all the days.
    '''
    print("             VITIME")
    cursor.execute("SELECT * FROM Schedules")
    data = cursor.fetchall()
    print("\nFull timetable")
    print("-"*50)
    for k in data:
        day, schedule = k
        schedule = eval(schedule)
        print(f"Day's schedule : {day}\n")
        for i in schedule:
            print(i[1])
            print(i[2])
            print(f"Course type : {checktype(i[4])}")
            print(f"Slot : {i[3]}")
            print(f"Time : {i[0]}\n")
        print("-"*50)
