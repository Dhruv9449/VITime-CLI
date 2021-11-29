import os
import sqlite3 as sq
import click

homedir = os.path.expanduser("~")


mycon = sq.connect(homedir+"/VITime.db")
cursor = mycon.cursor()
cursor.execute("""CREATE TABLE IF NOT EXISTS Schedules(day TEXT PRIMARY KEY,
                  schedule TEXT)""")
cursor.execute("""CREATE TABLE IF NOT EXISTS Courses(name TEXT,
                  slots TEXT, type TEXT, dt TEXT)""")
cursor.execute("SELECT * FROM Schedules")
if cursor.fetchall()==[]:
    cursor.executemany("INSERT INTO Schedules VALUES (?,?)",[("monday","[]"),
                                                         ("tuesday","[]"),
                                                         ("wednesday","[]"),
                                                         ("thursday","[]"),
                                                         ("friday","[]")])
    mycon.commit()


class day:
    def __init__(self, day, schedule = []):
        self.day = day
        self.schedule = schedule

class course:
    def __init__(self, name="", slots=[], type="L", dt=[]):
        self.name = ""
        self.slots = []
        self.type = "L"
        self.dt = []

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
        self.format_commands(ctx, formatter)
        formatter.write("\nUSAGE:\n"+"  vitime [COMMAND] [COMMAND OPTIONS]\n")
        self.format_options(ctx, formatter)




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
