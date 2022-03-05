#! /user/bin/env ptython3

import csv
import operator
import os
import re
import sys

FIND_ERROR = r'(ERROR ([\w \[]*)) '
MATCH_USER = r'\((.*?)\)'
ERROR_IN_LINE = " Error "
INFO_IN_LINE = " INFO "
NO_TICKET = "Ticket doesn't exist"
TICKET = "Ticket"


error_counter = {}
error_user = {}
info_user = {}


def search_file(filename: str):
    with open(filename, "r") as my_file:
        for line in my_file:
            if ERROR_IN_LINE in line:
                find_error(line)
                add_user_list(line, 1)
            elif INFO_IN_LINE in line:
                add_user_list(line, 2)


def find_error(line: str):
    match = re.search(FIND_ERROR, line)
    if match is not None:
        aux = match.group(1).strip()
        if aux == TICKET:
            aux = NO_TICKET
        if not aux in error_counter:
            error_counter[aux] = 1
        else:
            error_counter[aux] += 1
    return


def add_user_list(str, op):
    match = re.search(MATCH_USER, str)
    user = match.group(1)

    if op == 1:
        if not user in error_user:
            error_user[user] = 1
        else:
            error_user[user] += 1
    elif op == 2:
        if not user in info_user:
            info_user[user] = 1
        else:
            info_user[user] += 1
    return

# This function will read the list, arrange it and return a tuple with the dictionary items


def sort_list(op, list):
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


def write_csv(op: int):
    if op == 1:
        with open('user_statistics.csv', 'w', newline='') as output:
            fieldnames = field_names_header()
            csvw = csv.DictWriter(output, fieldnames=fieldnames)
            csvw.writeheader()
            for key, value in info_user:
                valError = getErrValue(key)
                csvw.writerow(
                    {'Username': key, 'INFO': value, 'ERROR': valError})
    if op == 2:
        with open('error_message.csv', 'w', newline='') as output:
            fieldnames = ['Error', 'Count']
            csvw = csv.DictWriter(output, fieldnames=fieldnames)
            csvw.writeheader()
            for key, value in error_counter:
                csvw.writerow({'Error': key, 'Count': value})
    return


def field_names_header():
    fieldnames = ['Username', 'INFO', 'ERROR']
    return fieldnames

# This function adds zero to the other dictionary in case that user is not a key, it will add a key with the user and value 0


def add_zeros():
    for user in error_user.keys():
        if user not in info_user:
            info_user[user] = 0
    for user in info_user.keys():
        if user not in error_user:
            error_user[user] = 0
    return


def main():

    search_file('syslog.log')

    add_zeros()
    error_counter = sort_list(1, error_counter)
    error_user = sort_list(2, error_user)
    info_user = sort_list(2, info_user)
    write_csv(1)
    write_csv(2)


if __name__ == '__main__':
    main()
