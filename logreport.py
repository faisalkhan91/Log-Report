#!/usr/bin/python3

#############################################################################################
#                               Program by Mohammed Faisal Khan                             #
#                               Email: faisalkhan91@outlook.com                             #
#                               Date: 09/17/2019                                            #
#############################################################################################

# Importing system module

import sys
import re
import sqlite3

# Function Definitions

#############################################################################################


# Function to check if the filename was given, if not ask the user to input file(s)
def check_file(filename):

    if not filename:
        print("File name not specified.")
        filename = input("Please enter the name of the log file: ")
        if 'log' in filename:
            return filename
        else:
            print("Not a log file! Try Again!!!")
            exit()
    else:
        if 'log' in filename:
            return filename
        else:
            print("Not a log file! Try Again!!!")
            exit()


# Function to read in the file contents if the file exists
def read_file(filename=""):

    # File exist error handling - http://www.diveintopython.net/file_handling/index.html
    try:
        current_file = open(filename, "r", encoding="utf8")
    except IOError:
        print("File does not exist.")
        return "Nothing to print."

    # Split lines - http://stackoverflow.com/questions/15233340/getting-rid-of-n-when-using-readlines
    content = current_file.read().splitlines()
    current_file.close()

    return content

#############################################################################################


def create_table():

    c.execute('CREATE TABLE IF NOT EXISTS Requests(IP TEXT, Name TEXT, Page TEXT, Code INT)')


def parse_get(logfile):

    # print(logfile)

    # http://stackoverflow.com/questions/106179/regular-expression-to-match-dns-hostname-or-ip-addre
    IP_address = re.compile(r"(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)(\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)){3}")
    MAC_address = re.compile(r"(^[-.a-z0-9]+)")
    response_code = re.compile(r"([^\w./-]([0-9]{3})[^.\w/-:])")
    page_name = re.compile(r"[^\w]((([/])([/.~\w]+)([.][\w]+)([?][\w./=]+)?)|[/])[^\w]")

    for line in logfile:
        # print(line)
        if '"GET' in line:
            print(line)
            IP = IP_address.match(line)
            MAC = MAC_address.match(line)
            page = page_name.search(line)
            code = response_code.search(line)
            if IP is not None:
                print(IP.group())
                print(code.group())
                if page is not None:
                    print(page.group())
                    c.execute("INSERT INTO Requests (IP, Name, Page, Code) VALUES (?, ?, ?, ?)",
                              (IP.group(), None, page.group(), code.group()))

            elif MAC is not None:
                print(MAC.group())
                print(code.group())
                if page is not None:
                    print(page.group())
                    c.execute("INSERT INTO Requests (IP, Name, Page, Code) VALUES (?, ?, ?, ?)",
                              (None, MAC.group(0), page.group(), code.group()))

    # c.execute("INSERT INTO Requests (IP, Name, Page, Code) VALUES (?, ?, ?, ?)", ('TestIP', 'TestNAME', 'TestPAGE',
    #                                                                               'TestCode'))
    conn.commit()

    output = c.execute("SELECT * from Requests")

    # for obj in output:
    #     print(obj[0], obj[1], obj[2], obj[3])


def generate_reports():

    file_write = open("logreport.txt", "w")

    Not_found = c.execute("SELECT DISTINCT Page from Requests WHERE Code == 404")
    file_write.write("##################################################################")
    file_write.write("\n")
    file_write.write("##################################################################")
    file_write.write("\n")
    for obj in Not_found:
        file_write.write(obj[0])
        file_write.write("\n")
    # for obj in Not_found:
    #     print(obj[0])

    Popular = c.execute("SELECT Page from Requests WHERE code == 200")
    file_write.write("##################################################################")
    file_write.write("\n")
    file_write.write("##################################################################")
    file_write.write("\n")
    for obj in Popular:
        file_write.write(obj[0])
        file_write.write("\n")
    # for obj in Not_found:
    #     print(obj[0])

    popular_unique = c.execute("SELECT Page from Requests")
    file_write.write("##################################################################")
    file_write.write("\n")
    file_write.write("##################################################################")
    file_write.write("\n")
    for obj in popular_unique:
        file_write.write(obj[0])
        file_write.write("\n")

    requestor = c.execute("SELECT Name from Requests")
    domain_name = re.compile(r"[a-zA-Z]+[.][a-zA-Z]+")
    file_write.write("##################################################################")
    file_write.write("\n")
    file_write.write("##################################################################")
    file_write.write("\n")
    for obj in requestor:
        if obj[0] is not None:
            domain = domain_name.search(obj[0])
            if domain is not None:
                # print(domain.group())
                string = domain.group()
                # print(string)
                file_write.write(string)
                file_write.write("\n")

    file_write.close()

#############################################################################################

# Main Program

# Command line argument to take names of files as input
file = ""

try:
    file = sys.argv[1]
except IndexError:
    check_file(file)

checked_file = check_file(file)
# print("Files: ", files)

print("\n###################################", file, "###################################", end="\n")
log_data = read_file(checked_file)
# print(log_data)

# Connect to database
# SQLlite type: REAL, INT, TEXT, BLOB, None/Null(?)
conn = sqlite3.connect("logreport.db")
c = conn.cursor()

# create_table()

# parse_get(log_data)

generate_reports()

# Close connection to database
c.close()
conn.close()

#############################################################################################
#                                       End of Program                                      #
#                                       Copyright 2019                                      #
#############################################################################################
