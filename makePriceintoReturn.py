from datetime import datetime, timedelta
import numpy as np
import time
import pandas as pd
import math
import csv


def last_day_of_month(date1):

    date = datetime.strptime(str(date1), "%Y%m%d")
    month = date.month
    month2 = date.month
    while month == month2:
        date = date + timedelta(days=1)
        month = date.month

    date = date - timedelta(days=1)
    year = str(date.year)
    day = str(date.day)
    if month2 < 10:
        month2 = str('0' + str(month2))
    else:
        month2 = str(month2)
    return int(str(year + month2 + day))


outfile = open('/Users/surge/Dropbox/My Mac (MacBook Pro)/Desktop/JIW/Best versions of things/SuperExcitingPriceData.csv', 'w')
with open('/Users/surge/Dropbox/My Mac (MacBook Pro)/Desktop/JIW/Best versions of things/WowPriceData.csv', 'r') as csv_file:

    reader = csv.reader(csv_file, delimiter=",")
    header = next(reader)

    permnoList = []
    dateList = []
    siccdList = []
    cusipList = []
    ReturnList = []

    uniquePermno = 0
    permno = 0
    uniqueDate = 0
    date = 0
    SICCD = 0
    price = 0
    dividend = 0
    cusip = 'not this'
    monthReturn = 0

    previousPrice = 0
    previousDividend = 0

    previousPrice2 = 0
    previousDividend2 = 0

    firstfirst = 0
    first = 0

    uniqueAssets = []

    howManyRows = 0

    for row in reader:
        howManyRows += 1


        permno = int(row[0])

        if permno not in uniqueAssets:
            uniqueAssets.append(permno)

        date = last_day_of_month(str(math.floor(float(row[1]))))
        if row[2] == '':
            SICCD = 0
        if row[2] == 'Z':
            SICCD = 0
        else:
            SICCD = row[2]
        cusip = str(row[3])
        if row[4] != '':
            dividend = float(row[4])
        else:
            dividend = 0
        if row[5] != '':
            price = float(row[5])
        else:
            price = 0

        if permno != uniquePermno:

            if firstfirst == 0:
                previousDividend = dividend
                previousPrice = price
                uniquePermno = permno
                first = 1
                firstfirst += 1
                continue

            if firstfirst != 0:
                uniquePermno = permno
                if first == 3:

                    previousPrice = previousPrice2
                    previousDividend = previousDividend2

                    previousPrice2 = price
                    previousDividend2 = dividend

                    if previousPrice == 0 and previousDividend == 0:
                        monthReturn = 0
                    else:
                        monthReturn = (price + dividend) / (previousPrice + previousDividend)

                    permnoList.append(permno)
                    dateList.append(date)
                    siccdList.append(SICCD)
                    cusipList.append(cusip)
                    ReturnList.append(monthReturn)
                    first = 1
                    continue

        if permno == uniquePermno:

            if first == 1:
                previousDividend2 = dividend
                previousPrice2 = price
                uniquePermno = permno
                first = 2
                continue

            if first == 2:
                if previousPrice == 0 and previousDividend == 0:
                    monthReturn = 0
                else:
                    monthReturn = (price + dividend) / (previousPrice + previousDividend)

                permnoList.append(permno)
                dateList.append(date)
                siccdList.append(SICCD)
                cusipList.append(cusip)
                ReturnList.append(monthReturn)

                first = 3
                continue

            if first == 3:

                previousPrice = previousPrice2
                previousDividend = previousDividend2

                previousPrice2 = price
                previousDividend2 = dividend

                if previousPrice == 0 and previousDividend == 0:
                    monthReturn = 0
                else:
                    monthReturn = (price + dividend) / (previousPrice + previousDividend)

                permnoList.append(permno)
                dateList.append(date)
                siccdList.append(SICCD)
                cusipList.append(cusip)
                ReturnList.append(monthReturn)
                first = 3


    # array = np.empty([howManyRows, 6])

    with open('/Users/surge/Dropbox/My Mac (MacBook Pro)/Desktop/JIW/Best versions of things/SuperExcitingPriceData.csv', mode='w') as csv_file:
        fieldnames = ['PERMNO', 'date', 'SICCD', 'CUSIP', 'Return']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        x = 0
        while x < howManyRows - 1 - len(uniqueAssets):
            print(str(howManyRows - x - len(uniqueAssets) - 1))
            writer.writerow({'PERMNO': str(permnoList[x]), 'date': str(dateList[x]), 'SICCD': str(siccdList[x]), 'CUSIP': str(cusipList[x]), 'Return': str(ReturnList[x])})
            x += 1


