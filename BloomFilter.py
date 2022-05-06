import math
import csv
import sys
import mmh3
from pathlib import Path

# Project 2 - Jonathan Rivera Chico - 802-19-6401

#  n = ceil(m / (-k / log(1 - exp(log(p) / k)))) Number of items in the filter
#  m = ceil((n * log(p)) / log(1 / pow(2, log(2)))); Number of bits in the filter 
#  k = round((m / n) * log(2)); Number of hash functions

FP_PROB = 0.0000001

"""
Function that takes two .csv files and creates two lists with all the data inside the .csv file

Args:
    input,input2 - .csv file with the emails to put in the bloomfilter and the emails to compare

Returns:
    emails - list of the emails in the first .csv file
    echeck - list of emails in the second .csv file
    len(emails) - size of the first list

"""

def extract_data(input,input2):
    emails = []
    echeck = []

    reader1 = csv.reader(open(input, 'r'))
    reader2 = csv.reader(open(input2, 'r'))

    # Since the first element is just a header, iterate to the second element
    reader1.__next__() 
    reader2.__next__()

    # Puts all the emails in the bloom filter list
    for element in reader1:
        for email in element:
            emails.append(email)

    # Puts all the emails in the to be compared list
    for element in reader2:
        for email in element:
            echeck.append(email)

    # Returns both lists and the length of the first list for use in the bloom filter
    return emails,echeck,len(emails)
    


"""
Bloom Filter class:
Creates a bloom filter by using the parameters given
to its constructor

"""

class bloom_filter:

    """
    Constructor function: takes the parameters and sets its values for the
    creation of the bloomfilter

    Args:
        emails1 - list of emails to be used in the bloom filter
        emails2 - list of emails to be compared
        ecount - count of emails in the first list
        fp - false positive probability number

    """
    def __init__(self,emails1,emails2,ecount,fp):
        self.fp_prob = fp
        self.items = ecount # email count
        self.size = math.ceil((ecount * math.log(FP_PROB)) / math.log(1 / pow(2, math.log(2)))) # number of bits
        self.hashes = round((self.size / ecount) * math.log(2)) # number of hashes
        self.array = [0]*self.size # array of zeros
        self.collection = emails1
        self.collection2 = emails2
        self.result = [] # result array

    """
    Sets up the bloom filter using the first list of emails
    and using hashing function to use an array of 0's, converting a 0 to a 1 
    means that the email is in the filter.

    """

    def setUp(self):
        for email in self.collection:
            for seed in range(1,self.hashes+1):
                pos = mmh3.hash(email,seed) % self.size # hashes the email with a seed and uses the modulo of the size of the array
                self.array[pos] = 1 # sets the given position as 1 in the array to indicate that the element exists

    """
    Checks if the second list of emails is on the bloom filter,
    using hash function, if the element in the array is 1, then its Probably in the DB
    else, its Not in the DB. It sets an string array with the probabilities of the emails
    being in the filter
    
    Returns:
    tcount - count of all the emails probably in the DB
    fcount - count of all the emails that are not in the DB

    """
    def check(self):
        checked = [] # result array 
        # optional truth and false counts for debugging
        tcount = 0 
        fcount = 0

        # iterates through the second list of emails and checks if they are in the bloom filter
        for email in self.collection2:
            flag = True
            for seed in range(1,self.hashes+1):
                digest = mmh3.hash(email,seed) % self.size # hashes the email with a seed and uses the modulo of the size of the array
                # if the element in the bloom filter is 0, the element does not exist in the DB therefore it returns Not in the DB
                if(self.array[digest] == 0):
                    checked.append("Not in the DB")
                    flag = False
                    fcount +=1
                    break
            # if the element in the bloom filter is 1, it probably exists in the DB, therefore it returns Probably in the DB
            if flag:
                checked.append("Probably in the DB")
                tcount+=1
        self.result =  checked # sets the result array 
        return tcount,fcount

    """
    Function that outputs the results of the bloom filter into a .csv file by using the 
    list of the emails to be compared and the list of the probabilities of those emails
    being in the filter

    """
    
    def results(self):
        output_file = open('results.csv', 'w') # Opens the input file
        writer = csv.writer(output_file) # .csv file writer

        # Sets the header rows
        writer.writerow(["email", "result"])

        # writes on the .csv file, the first column is the email and the second one is the probability of it being in the DB
        for i in range(len(self.collection2)):
            writer.writerow([self.collection2[i], self.result[i]])


"""
    Main function in charge of taking the two .csv files and running them throught
    the bloom filter class

    Args:
        file1 - first .csv file
        file2 - second .csv file
"""
def main(file1,file2):

    if not Path(file1).is_file():
        print("Error: File 1 does not exist.")
        sys.exit(1)
    if not Path(file2).is_file():
        print("Error: File 2 does not exist.")
        sys.exit(1)

    emails,emails2,size = extract_data(file1,file2)
    bf = bloom_filter(emails,emails2,size,FP_PROB)
    bf.setUp()
    # print("Prob in DB : Not in DB") // Optional: if the function below is printed, the count of the emails in the db and not in the db appear
    bf.check()
    bf.results()


main(sys.argv[1:2][0], sys.argv[2:][0])
print("Results succesfully generated!")

          




