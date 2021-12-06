import os
import sqlite3 as sq
import click
import pyperclip
import re
from subprocess import PIPE, Popen
import json
import urllib.request


__version__ = '0.2.1'


# cmdline
def cmd(command):
    process = Popen(
        args=command,
        stdout=PIPE,
        shell=True
    )
    return process.communicate()[0].decode("utf-8")



homedir = os.path.expanduser("~")


mycon = sq.connect(homedir+"/VITime.db")
cursor = mycon.cursor()

def initialize():
    cursor.execute("""CREATE TABLE IF NOT EXISTS Schedules(day TEXT PRIMARY KEY,
                      schedule TEXT)""")
    cursor.execute("""CREATE TABLE IF NOT EXISTS Courses(code TEXT, name TEXT,
                      slots TEXT, type TEXT, dt TEXT)""")
    cursor.execute("SELECT * FROM Schedules")
    if cursor.fetchall()==[]:
        cursor.executemany("INSERT INTO Schedules VALUES (?,?)",[("monday","[]"),
                                                             ("tuesday","[]"),
                                                             ("wednesday","[]"),
                                                             ("thursday","[]"),
                                                             ("friday","[]")])
    mycon.commit()

initialize()

class day:
    def __init__(self, day, schedule = []):
        self.day = day
        self.schedule = schedule

class course:
    def __init__(self, code="", name="", slots=[], type="L", dt=[]):
        self.code = code
        self.name = name
        self.slots = slots
        self.type = type
        self.dt = dt


help = dict(help_option_names = ['-h','--help'])


class CustomGroup(click.Group):
    def format_commands(self, ctx, formatter):
        commands = []
        for subcommand in self.list_commands(ctx):
            cmd = self.get_command(ctx, subcommand)
            # What is this, the tool lied about a command.  Ignore it
            if cmd is None:
                continue
            if cmd.hidden:
                continue

            commands.append((subcommand, cmd))

        # allow for 3 times the default spacing
        if len(commands):
            limit = formatter.width - 6 - max(len(cmd[0]) for cmd in commands)

            rows = []
            for subcommand, cmd in commands:
                help = cmd.get_short_help_str(limit)
                rows.append((subcommand, help))

            if rows:
                with formatter.section('COMMANDS'):
                    formatter.write_dl(rows)

    def format_options(self, ctx, formatter):
        """Writes all the options into the formatter if they exist."""
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                if rv[0] == '-h, --help':
                    rv = list(rv)
                    rv[1] = "Show this message."
                    rv = tuple(rv)
                opts.append(rv)
        if opts:
            with formatter.section('OPTIONS'):
                formatter.write_dl(opts)

    def format_help(self, ctx, formatter):
        head = """__      __ _____  _______  _                  \n\\ \\    / /|_   _||__   __|(_)                 \n \\ \\  / /   | |     | |    _  _ __ ___    ___ \n  \\ \\/ /    | |     | |   | || '_ ` _ \\  / _ \\\n   \\  /    _| |_    | |   | || | | | | ||  __/\n    \\/    |_____|   |_|   |_||_| |_| |_| \\___|\n\n"""
        body = """CLI tool to view your timetable from terminal anytime!

Developer :
  Dhruv Shah (https://github.com/Dhruv9449)\n"""

        formatter.write(head)
        formatter.write(body)
        formatter.write("\nFor more detailed help:\n  https://github.com/Dhruv9449/VITime-CLI/blob/main/README.md\n")
        self.format_commands(ctx, formatter)
        formatter.write("\nUSAGE:\n"+"  vitime [COMMAND] [COMMAND OPTIONS]\n")
        self.format_options(ctx, formatter)
        check, Latest_version = checkLatestVersion()
        if check :
            formatter.write(f"\nVITIME UPDATE AVAILABLE!\nVersion {Latest_version} available, do 'vitime -u' to update now!\n")


class CustomCommand(click.Command):
    def format_options(self, ctx, formatter):
        """Writes all the options into the formatter if they exist."""
        opts = []
        for param in self.get_params(ctx):
            rv = param.get_help_record(ctx)
            if rv is not None:
                if rv[0] == '-h, --help':
                    rv = list(rv)
                    rv[1] = "Show this message."
                    rv = tuple(rv)
                elif rv[0] == '-n, --name TEXT':
                    rv = list(rv)
                    rv[0] = "-n, --name     "
                    rv = tuple(rv)
                opts.append(rv)
        if opts:
            with formatter.section('OPTIONS'):
                formatter.write_dl(opts)
        return opts

    def format_help(self, ctx, formatter):
        print("             VITIME\n\nCOMMAND:")
        path = ctx.command_path
        print("  "+ctx.command_path+"\n")
        print("DESCRIPTION:")
        text = self.help
        print("  "+text)
        self.format_options(ctx, formatter)
        print("\nUSAGE:\n  "+path+" [OPTIONS]\n")
        print("For more detailed help:\n  https://github.com/Dhruv9449/VITime-CLI/blob/main/README.md\n")



#Database functions
def addcourse_db(Course):
    cursor.execute("INSERT INTO Courses values (?,?,?,?,?)",
                    (Course.code, Course.name, str(Course.slots), Course.type, str(Course.dt)))
    mycon.commit()

def addschedule_db(Day):
    cursor.execute("UPDATE Schedules SET schedule = ? WHERE day = ?", (str(Day.schedule), Day.day,))
    mycon.commit()

def loadcourse(code):
    cursor.execute("SELECT * FROM Courses WHERE code = ?",(code,))
    code, name, slots, type, dt = cursor.fetchall()[0]
    slots, dt = eval(slots), eval(dt)
    Course = course(code, name, slots, type, dt)
    return Course

def loadday(name):
    cursor.execute("SELECT * FROM Schedules WHERE day = ?",(name,))
    name, schedule = cursor.fetchall()[0]
    schedule = eval(schedule)
    Day = day(name, schedule)
    return Day


# auto updates

def checkLatestVersion():
    # Get the currently installed version
    current_version = __version__
    # Check pypi for the latest version number
    contents = urllib.request.urlopen('https://pypi.org/pypi/vitime/json').read()
    data = json.loads(contents)
    latest_version = data['info']['version']
    check = latest_version != current_version
    return check, latest_version



def check_update(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    try:
        print("             VITIME\n")
        req = cmd("pip install vitime --upgrade")
        if "Successfully uninstalled vitime" in req:
            version = cmd("pip show vitime").split("\n")[1]
            print(f"NEW UPDATE! [{version}]")
            print("VITime updated! Check out what's new at -\n  https://github.com/Dhruv9449/VITime-CLI/blob/main/CHANGELOG.md\n")
        else:
            print("You are already using latest version of VITime!\n")
    except:
        print("An error occured! Please update manually using 'pip install vitime --upgrade'.\n")
    ctx.exit()


# print version
def print_version(ctx, param, value):
    if not value or ctx.resilient_parsing:
        return
    print("             VITIME\n")
    print("Version:", __version__,"\n")
    ctx.exit()


#checks
def checkcourse(Name):
    if not re.search("[A-Z][A-Z][A-Z][A-Z]\d\d\d|[A-Z][A-Z][A-Z]\d\d\d\d", Name.code):
        print(f"\n{Name.code} is an invalid course code, please enter a valid course code.(eg - BCHY101L/CSE1002)\n")
        return True
    cursor.execute("SELECT * from Courses WHERE code = ? AND slots = ?",(Name.code, str(Name.slots)))
    courses = cursor.fetchall()
    if len(courses) == 0:
        return False
    print(f"\nCourse {Name.code} already exists!\n")
    return True


def checktype(type):
    if type == "L" :
        return "Theory"
    else:
        return "Lab"

#input command
def retrieveinput():
    print("\nGo to vtop and copy all the courses.")
    print("For more help on how to do that check -\n  https://github.com/Dhruv9449/VITime-CLI#vitime-addtimetable")
    confirm = input("\nType 'yes' if you have copied all the courses : ").lower()
    if confirm == 'yes' :
        text = pyperclip.paste().replace('\r','\n')
        return text
    else:
        print("\nPlease go copy all your courses and try again!")
        return False


def scrape(data):
    try:
        code_name = [i[:-1] for i in re.findall("[A-Z][A-Z][A-Z][A-Z]\d\d\d.+\n|[A-Z][A-Z][A-Z]\d\d\d\d.+\n", data)]
        code = [i.split()[0] for i in code_name]
        name = [i.split(" - ")[1] for i in code_name]
        slots = [j[:-3].split('+') for j in re.findall(".+\d.+[-]\n|NIL.+[-]\n",data)]
        return list(zip(code, name, slots))

    except IndexError :
        return []
