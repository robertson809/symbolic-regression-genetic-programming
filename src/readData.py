import csv
import random
import math
#temporarily changing .8 to .001 to make testing easier
SPLIT = .02

#Reads a csv of datapoints into an array of datapoint pairs
def readData(filename):
    with open(filename) as csv_file:
        #dialect = csv.Sniffer().sniff(csv_file.read(1024))
        #csv_file.seek(0)
        csv_reader = csv.reader(csv_file,delimiter=',')
        dataset=list(csv_reader)
        columns = dataset[0]
        dataset = dataset[1:]
        for row in range(len(dataset)):
            for col in range(len(dataset[row])):
                dataset[row][col] = float(dataset[row][col])

        return dataset

#Splits a dataset into training and test sets with the ratio of constant SPLIT
def splitData(dataset):
    #Shuffle the data points
    random.shuffle(dataset)

    #Find the 80% mark to split the data into train and test
    split = int(math.floor(len(dataset)*SPLIT))
    train = dataset[:split]
    test = dataset[split:]

    return train, test

#Writes the split data into their own files (only needs to be done once)
def writeData(filename,dataset):
    with open(filename, mode='w') as csv_file:
        data_writer = csv.writer(csv_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in range(len(dataset)):
            data_writer.writerow(dataset[row])

# set1 = readData('../data/dataset1.csv')
# small_train1 = splitData(set1)[0]

