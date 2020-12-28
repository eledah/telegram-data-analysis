import pandas as pd
import arabic_reshaper
from bidi.algorithm import get_display
import matplotlib.pyplot as plt
import json

# FILE_PATH = "C:/Users/eledah/Documents/GitHub/telegram-data-analysis/data/result.json"
# FILE_PATH = "C:/Users/eledah/Documents/GitHub/telegram-data-analysis/data/result2.json"
FILE_PATH = "C:/Users/eledah/Documents/GitHub/telegram-data-analysis/data/result3.json"
REMOVE_DELETED_ACCOUNTS = True


def openFile(path):
    return open(path, encoding='utf-8')


def loadFile(file):
    return json.load(file)


def closeFile(file):
    file.close()


def bubbleSort(arr, arr2, expand=False, sort="descending"):
    n = len(arr)
    if sort == "descending":
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                if arr[j] < arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    if expand:
                        arr2[j], arr2[j + 1] = arr2[j + 1], arr2[j]
    else:
        for i in range(n - 1):
            for j in range(0, n - i - 1):
                print(arr[j], arr[j + 1])
                if arr[j] > arr[j + 1]:
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    if expand:
                        arr2[j], arr2[j + 1] = arr2[j + 1], arr2[j]


def dataFind(data, dataType, msg_from='EVERYONE', msg_year='ALLYEAR'):
    headers = []
    for row in data['messages']:
        if row['type'] == 'message' \
                and (msg_from == 'EVERYONE' or msg_from == row['from']) \
                and (msg_year == 'ALLYEAR' or msg_year == row['date'][0:4]):
            if dataType == "hour":
                header = int(row['date'][11:13])
            elif dataType == "from":
                if row['from'] is not None:
                    header = row['from']
            elif dataType == "day":
                header = row['date'][0:10]
            if not (header in headers):
                headers.append(header)
    return headers


def dataCount(data, dataHeader, dataType, msg_from="EVERYONE", msg_year="ALLYEAR"):
    dataCount = []
    for i in range(len(dataHeader)):
        dataCount.append(0)
    for row in data['messages']:
        if row['type'] == 'message'\
                and (msg_from == 'EVERYONE' or msg_from == row['from'])\
                and (msg_year == 'ALLYEAR' or msg_year == row['date'][0:4]):
            if dataType == "hour":
                dataCount[dataHeader.index(int(row['date'][11:13]))] += 1
            elif dataType == "from":
                if row['from'] is not None:
                    dataCount[dataHeader.index(row['from'])] += 1
            elif dataType == "day":
                dataCount[dataHeader.index(row['date'][0:10])] += 1
    if dataType == "hour":
        dataHeader.append(24)
        dataCount.append(int(dataCount[dataHeader.index(0)]))
        bubbleSort(dataHeader, dataCount, expand=True, sort="descending")
    elif dataType == "from":
        bubbleSort(dataCount, dataHeader, expand=True)
    return dataHeader, dataCount


FILE = openFile(FILE_PATH)
DATA = loadFile(FILE)

print("Creating Posters' List...")

posterList, postCount = dataCount(DATA, dataFind(DATA, 'from'), 'from')
for i in range(0, len(posterList)):
    posterList[i] = get_display(arabic_reshaper.reshape(posterList[i]))

hourList_2017, hourCount_2017 = dataCount(DATA, dataFind(DATA, 'hour', msg_year='2017'), 'hour', msg_year='2017')
hourList_2018, hourCount_2018 = dataCount(DATA, dataFind(DATA, 'hour', msg_year='2018'), 'hour', msg_year='2018')
hourList_2019, hourCount_2019 = dataCount(DATA, dataFind(DATA, 'hour', msg_year='2019'), 'hour', msg_year='2019')
hourList_2020, hourCount_2020 = dataCount(DATA, dataFind(DATA, 'hour', msg_year='2020'), 'hour', msg_year='2020')

dayList, dayCount = dataCount(DATA, dataFind(DATA, 'day'), 'day')

# for i in posterList:
#     dayList, dayCount = dataCount(DATA, dataFind(DATA, 'day', msg_from=i), 'day', msg_from=i)
#     for j in range(0, len(dayList)):
#         if not (REMOVE_DELETED_ACCOUNTS and dayList[j] is None):
#             print(dayList[j], dayCount[j])


print("Drawing Graph...")

fig = plt.figure(figsize=(20, 5))
axes = plt.axes()
ax = plt.bar(posterList, postCount)
# plt.plot(hourList_2017, hourCount_2017, label="2017")
# plt.plot(hourList_2018, hourCount_2018, label="2018")
# plt.plot(hourList_2019, hourCount_2019, label="2019")
# plt.plot(hourList_2020, hourCount_2020, label="2020")
plt.legend()

fig.autofmt_xdate()
# plt.xticks(range(0, 24))
plt.xticks(fontname="Sahel FD")
plt.yticks(fontname="Sahel FD")
axes.grid()
# plt.xlim([0, 24])
# plt.ylim([0, 90])
plt.show()

closeFile(FILE)
