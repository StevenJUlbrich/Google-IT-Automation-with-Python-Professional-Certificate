#! /user/bin/env ptython3

import csv
import operator
import os
import re
import sys

FIND_ERROR = r'(ERROR ([\w \[]*)) '
MATCH_USER = r'\((.*?)\)'
ERROR_IN_LINE = " ERROR "
INFO_IN_LINE = " INFO "
NO_TICKET = "Ticket doesn't exist"
TICKET = "Ticket"


error_counter = {}
info_user = {}


def search_file(filename: str):
    with open(filename, "r") as my_file:
        for line in my_file:
            Date, Server_App, Entry, Message, User = parse_line(line)
            if Entry == "ERROR":
                update_error_dic(Message)
            update_user_dic(Entry, User)


def update_user_dic(Entry, User):
    if User not in info_user:
        if Entry == "ERROR":
            info_user[User] = [0, 1]
        else:
            info_user[User] = [1, 0]
    else:
        if Entry == "ERROR":
            info_user[User][1] += 1
        else:
            info_user[User][0] += 1


def update_error_dic(error_msg):

    if error_msg not in error_counter:
        error_counter[error_msg] = 1
    else:
        error_counter[error_msg] += 1


def parse_line(line: str):
    # Match attempt failed
    Date = ""
    Server_App = ""
    Entry = ""
    Message = ""
    User = ""
    reobj = re.compile(
        r"^(?P<Date>\w{3}\s\d{1,2}\s\d{2}:\d{2}:\d{2})(?P<Server_App>.*?:)\s(?P<Entry>INFO|ERROR)\s(?P<Message>.*?)\s\((?P<User>.*?)\)")
    match = reobj.search(line)
    if match:
        Date = match.group("Date")
        Server_App = match.group("Server_App")
        Entry = match.group("Entry")
        Message = match.group("Message")
        User = match.group("User")

    return Date, Server_App, Entry, Message, User


def sort_list(op: int, list: dict):
    if op == 1:
        s = sorted(list.items(), key=operator.itemgetter(1), reverse=True)
    elif op == 2:
        s = sorted(list.items(), key=operator.itemgetter(0))
    return s

# This is an extra function which will read the value of a user in the error dictionary and return its value if key exists


def getErrValue(keyV):
    for key, value in error_user:
        if key is keyV:
            return value
    return 0


def write_error_messages(error_counter_info):
    with open('error_message.csv', 'w', newline='') as output:
        fieldnames = ['Error', 'Count']
        csvw = csv.DictWriter(output, fieldnames=fieldnames)
        csvw.writeheader()
        for key, value in error_counter_info:
            csvw.writerow({'Error': key, 'Count': value})


def write_csv_user_statics(user_info):
    with open('user_statistics.csv', 'w', newline='') as output:
        fieldnames = field_names_header()
        csvw = csv.DictWriter(output, fieldnames=fieldnames)
        csvw.writeheader()
        for key, value in user_info:
            csvw.writerow(
                {'Username': key, 'INFO': value[0], 'ERROR': value[1]})


def field_names_header():
    fieldnames = ['Username', 'INFO', 'ERROR']
    return fieldnames


def main():

    search_file('Operating System Interact\Week_7\syslog.log')

    error_counter_1 = sort_list(1, error_counter)
    info_user_1 = sort_list(2, info_user)
    write_csv_user_statics(info_user_1)
    write_error_messages(error_counter_1)


if __name__ == '__main__':
    main()
