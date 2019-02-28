# -*- coding: utf-8
"""Implement some functionality from the R programming language in
Python.

This module provides some functions presented in R to be used in
Python. This module is far from being a fully implemented R port
and is likely to be unstable. Use it at your own risk.

Attributes:
  RYTHON_VERSION (float): the current version of the module.
  
History:
  * 0.3
    - Now DataFrame objects have implemented the size property.
    - Added the 'printer' method used as a console progress bar.
    - Renamed the method "str" to "strc", since the name conflicted 
       with the "str" built-in function.
    - Added a helper method to install the stopwords.
    - Added a helper method to show help about the installation of 
       nltk.
    - Improved the output of the 'summary' method
    - Overall code style improvement.
"""

import math
import random
import re
import string
import sys

try:
    from nltk.corpus import stopwords
except ImportError:
    print("Error while importing stopwords!")
    print("Try executing python(3) rython.py --help for more information.")

RYTHON_VERSION = 0.3

#----------------------------------------------------------------------
#							Data Structures
#----------------------------------------------------------------------

class Corpus(object):
    """Emulate the Corpus data structure from R's tm package."""

    def __init__(self, docs):
        """Create a new Corpus.

        Args:
          docs (list): the string documents to be stored whithin the
            Corpus.
        """
        self.docs = docs

    def __repr__(self):
        """Print the number of documents in the Corpus."""
        return ("A corpus with {0} text documents".format(len(self.docs)))

    def get_docs(self, start, end):
        """Get a set of documents from this corpus.

        Args:
          start (int): the first document to be fetched (inclusive).
          end (int): the last document to be included (exclusive).
  
        Returns:
          (list) the documents extracted from the Corpus.
        """
        return self.docs[start:end]

    def inspect(self, indexes):
        """Print some of the documents stored in the Corpus.

        The documents printed are those whose indexes are included
        inside of the given list.

        Args:
          indexes (list): a list of integers.
        """
        for number in indexes:
            print("[[{0}]]".format(number))
            print(self.docs[number])

class DataFrame(object):
    """Emulate the Data Frame R structure."""

    def __init__(self, headers):
        """Create a new Data Frame.

        Args:
          headers (list): the categories that will be stored in
            the Data Frame.
        """
        self.headers = headers;
        self.data = dict()

        for name in self.headers:
            self.data[name] = list()

    def __repr__(self):
        """Prints the entire contents of the Data Frame.

        Returns:
          (string) a representation of the data stored here.
        """
        str = repr(self.headers) + "\n"

        for number in range(0, len(self.data[self.headers[0]])):
            for category in self.headers:
                str += repr(self.data[category][number])
            str += "\n"

        return str

    def __getitem__(self, key):
        """Fetch a categorie from the Data Frame.

        Args:
          key (string): the name of the categorie to be fetched.

        Returns:
          (list): the data of the given categorie.
        """
        return self.data[key]
    
    def __len__(self):
        """Get the length of the Data Frame.
        
        The Length of a Data Frame is the number of registers that it
        contains.
        
        Returns:
          int: The number of registers in the Data Frame.
        """
        h = self.headers[0]
        
        return len(self.data[h])

    def cat(self, category):
        """Fetch a categorie from the Data Frame.

        Args:
          category (string): the name of the categorie to be fetched.

        Returns:
          (list) the data of the given category if it is inside the
          Data Frame. None otherwise
        """
        if category in self.data:
            return self.data[category]
        else:
            print("Category {0} is not defined".format(category))
            return None

    def clean(self, category):
        """Clean the category from undesired characters.

        The complete process converts all characters in the category to
        lowercase, removes all digits, punctuation symbols, extra white
        spaces, and the list of English stopwords defined in the nltk
        module.

        Args:
          category (string) the name of the category to be cleaned.
        """
        if category in self.data:
            self.tolower(category)
            self.remove_numbers(category)
            self.remove_stop_words(category)
            self.remove_punctuation(category)
            self.strip_whitespaces(category)
        else:
            print("Category {0} is not defined".format(category))

    def exclude(self, indexes):
        """Create a copy of the Data Frame.

        The copy Data Frame will include all of the data inside the
        original one, with the exception of all the categories whose
        indexes are inside of the given list.

        Args:
          indexes (list): a list of integers.

        Returns:
          (DataFrame) a Data Frame object, containing the copied data
          of the original data frame, minus all the categories whose
          indexes are given.
        """
        nheaders = []
        ndata = dict()

        for number in range(0, len(self.headers)):
            if number not in indexes:
                nheaders.append(self.headers[number])
                column = self.data[self.headers[number]][:]
                ndata[self.headers[number]] = column

        copy = DataFrame(nheaders)
        copy.data = ndata

        return copy;

    def getset(self, start, end):
        """Fetch a set of registers from the Data Set.

        Registers are the rows of the Data Frame.

        Args:
          start (int): the first register to be fetched (inclusive).
          end (int): the last register to be fetched (exclusive).

        Returns:
          (list) a list of registers extracted from the Data Frame.
        """
        regs = list()
        for number in range(start, end):
            regs.append(self.reg(number))

        return regs

    def get_subdataframe(self, start, end, condition=None, clause=None):
        """Extract some registers from the Data Frame into a new
        Data Frame.

        In addition to simply get some registers from the Data Frame
        'as is', it is also possible to specify a filter: only the
        registers between the start and end positions AND whose
        'condition' category has the value 'clause' will be included
        in the resulting Data Frame.

        Args:
          start (int): the first register to be included in the copy
            Data Frame (inclusive).
          end (int): the last register to be included in the copy
            Data Frame (exclusive).
          condition (string, optional): the name of the category to
            be "filter". Defaults to None.
          clause (object, optional): the value that a register must
            have in the 'condition' categorie to be included in the
            copy Data Frame. Defaults to None.

        Returns:
          (DataFrame) a copy of the Data Frame, only with the
          registers which satisfy the given conditions inside of it.
        """
        subset = DataFrame(self.headers)
        subdata = dict()

        for category in subset.headers:
            if condition is None:
                subdata[category] = self.data[category][start:end]
            else:
                subdata[category] = list()
                for number in range(start, end):
                    if self.data[condition][number] == clause:
                        subdata[category].append(self.data[category][number])

        subset.data = subdata

        return subset

    def get_sparse_matrix(self, category, start, end, frequent=None):
        """Compute the sparse matrix for the given category.

        The sparse matrix counts every value that appears in the
        column, making possible to see how many times every value
        occurs. This method is designed to be used with string
        categories (for example, for counting words).

        First all of the different possible values in the category
        are extracted as a corpus, and then for every register in the
        interval given a dictionary is created, with every possible
        value as an entry. Then all the values in the category is
        counted and stored under the proper entry.

        The 'matrix' then is a list of dictionaries, a dictionary per
        every register in the interval.
          
        Args:
          category (string): the name of the category whose sparse
            matrix will be created.
          start (int): the first register to be included in the
            analysis (inclusive).
          end (int): the last register to be included in the
            analysis (exclusive).
          frequent (list, optional): the items to be considered in
            the analysis. If not given, a set of items will be
            automatically generated. Defaults to None.

        Returns:
          (list) a sparse matrix for the category.
        """
        corpus = set()

        if category in self.data:
            if frequent is None:
                for number in range(start, end):
                    try:
                        message_words = self.data[category][number].split()
                        words = set(message_words)
                        corpus = corpus.union(words)
                    except AttributeError:
                        continue
            else:
                corpus = set(frequent)

            sparse_matrix = list()
            for number in range(start, end):
                row = dict()
                try:
                    for word in corpus:
                        row[word] = 0

                    for mword in self.data[category][number].split():
                        if mword in corpus:
                            qty = int(row[mword])
                            qty += 1
                            row[mword] = qty
                except AttributeError:
                    continue

                sparse_matrix.append(row)

            return sparse_matrix
        else:
            print("Category {0} is not defined".format(category))

    def include(self, indexes):
        """Create a copy of the Data Frame.

        The copy Data Frame will include all of the data inside the
        original one if their category index is inside of the given
        list of indexes.

        Args:
          indexes (list): a list of integers.

        Returns:
          (DataFrame) a Data Frame object, contained the copied data
          of the original Data Frame stored in the categories whose
          indexes are in the given list.
        """
        nheaders = []
        ndata = dict()

        for number in range(0, len(self.headers)):
            if number in indexes:
                nheaders.append(self.headers[number])
                column = self.data[self.headers[number]][:]
                ndata[self.headers[number]] = column

        copy = DataFrame(nheaders)
        copy.data = ndata

        return copy;

    def norm(self):
        """Normalize all of the values stored in the Data Frame.

        This method uses the min-max technique to normalize the values.
        """
        for key in self.data:
            column = self.data[key]
            if isinstance(column[0], int) or isinstance(column[0], float):
                norm_column = normalize(column)
                self.data[key] = norm_column

    def order(self, indexes):
        """Create a copy Data Frame with the specified order.

        The new Data Frame will contain the number of elements
        contained in the indexes list, ordered by the numbers in
        it.

        Args:
          indexes (list): a list of numbers.
        
        Returns:
          (DataFrame) a Data Frame object, ordered by the numbers
          inside the list.
        """
        nheaders = []
        ndata = dict()
        
        for category in self.headers:
            nheaders.append(category)
            ndata[category] = list()
            for number in indexes:
               ndata[category].append(self.data[category][number])

        copy = DataFrame(nheaders)
        copy.data = ndata
        
        return copy            

    def reg(self, index):
        """Fetch a register from the Data Frame.

        A register is a collection of values (one per category in the
        Data Frame).

        Args:
          key (int): the index of the desired register.

        Returns:
          (list) The register located at the given index, or None if
          the index is out of range.
        """
        if(index < len(self.data[self.headers[0]])):
            register = list()
            for category in self.headers:
                register.append(self.data[category][index])
            return register
        else:
            print("Register {0} is out of range".format(index))
            return None

    def remove_numbers(self, category):
        """Removes all the digits in the values of a category given.

        This method is designed to be used with non-numerical
        categories.

        Args:
          category (string): the name of the category to be cleaned.
        """
        if category in self.data:
            for number in range(0, len(self.data[category])):
                register = self.data[category][number]
                word = ""
                try:
                    for character in register:
                        if not character.isdigit():
                            word += character
                    self.data[category][number] = word
                except TypeError:
                    continue
                    self.data[category][number] = register				
        else:
            print("Category {0} is not defined".format(category))

    def remove_stop_words(self, category):
        """Remove all the stop words in the category.

        Stop words are words that are useless in a lexicographical
        analysis, since they're very common, such as 'the', 'is',
        'at', 'which', 'on', etc.

        The words considered stop words by this method are those
        defined in the nltk Python module.

        Args:
          category (string): the name of the category to be cleaned.
        """
        stop_words = stopwords.words("english")

        if category in self.data:
            for number in range (0, len(self.data[category])):
                try:
                    register = self.data[category][number].split()
                    clean_register = ""
                    for word in register:
                        if (word not in stop_words) and (len(word) > 2):
                            clean_register += word
                            clean_register += " "
                        self.data[category][number] = clean_register
                except AttributeError:
                    continue
        else: 
            print("Category {0} is not defined".format(category))

    def remove_punctuation(self, category):
        """Remove all the punctuation symbols from the given category.

        The list of punctuation symbols are those defined by Python in
        the string module.

        Args:
          category (string): the name of the category to be cleaned.
        """
        regex = re.compile('[%s]' % re.escape(string.punctuation))

        if category in self.data:
            for number in range (0, len(self.data[category])):
                try:
                    register = self.data[category][number]
                    clean_register = regex.sub(' ', register)				
                    self.data[category][number] = clean_register
                except AttributeError:
                    continue
                except TypeError:
                    continue
        else:
            print("Category {0} is not defined".format(category))

    def strip_whitespaces(self, category):
        """Remove all of the extra whitespaces in the given category.

        Only one simple whitespace will be left between every word.
        All initial and final whitespaces will also be removed.

        Args:
          category (string): the name of the category to be stripped.
        """
        if category in self.data:
            for number in range(0, len(self.data[category])):
                try:
                    register = self.data[category][number]
                    clear_register = register.strip()
                    clear_register = re.sub('\s\s+', " ", clear_register)
                    self.data[category][number] = clear_register
                except AttributeError:
                    continue
                except TypeError:
                    continue
        else:
            print("Category {0} is not defined".format(category))

    def tolower(self, category):
        """Transform all the characters in the category to lower case.

        Args:
          category (string): the name of the category to be modified.
        """
        if category in self.data:
            for number in range(0, len(self.data[category])):
                try: 
                    register = self.data[category][number]
                    self.data[category][number] = register.lower()
                except AttributeError:
                    continue
        else:
            print("Category {0} is not defined".format(category))

    def znorm(self):
        """Normalize all of the values stored in the Data Frame.

        This method uses the z-score technique to normalize the values.
        """
        for key in self.data:
            column = self.data[key]
            if isinstance(column[0], int) or isinstance(column[0], float):
                norm_column = z_normalize(column)
                self.data[key] = norm_column

class ArgumentException(Exception):
    """Basic exception to show that a wrong type argument was given."""

    def __init__(self, value):
        """Create a new ArgumentException

        Args:
          value (string): the message to be showed by the exception.
        """
        self.value = value

    def __str__(self):
        """Shows the message of this exception."""
        return repr(self.value)

#----------------------------------------------------------------------
#							R Methods
#----------------------------------------------------------------------

def copyright():
    """Print the information about Rython."""
    print("rython v{0}".format(RYTHON_VERSION))
    print("\u00a9 2014 - 2015 Knepa Corporation. All rights reserved.")
    print("WARNING: this script is provided 'as is'. It is for from being an"
          + " actual R port to Python. Use it at your own risk")

def cross_table(predictions, results, headers, pivot):
    """Print a table comparing the two given lists.

    Args:
      predictions (list): a list of strings, usually the output of a
        machine learning algorithm.
      results (list): a list of strings, usually the true values of a
        prediction made by a machine learning algorithm.
      headers (list): a list of string, which will be used as headers
        in the output table.
      pivot (string): the value that will be used as 'true', 'good'
        or 'positive' result. It is used to calculate false positives
        and negatives.
    """
    true_negative = 0
    false_positive = 0
    false_negative = 0
    true_positive = 0
    row_positive = 0
    row_negative = 0
    column_positive = 0
    column_negative = 0

    for number in range(0, len(predictions)):
        if predictions[number] == results[number]:
            if predictions[number] == pivot:
                true_positive += 1
            else:
                true_negative += 1
        else:
            if predictions[number] == pivot:
                false_positive += 1
            else:
                false_negative += 1

        if results[number] == pivot:
            row_positive += 1
        else:
            row_negative += 1

        if predictions[number] == pivot:
            column_positive += 1
        else:
            column_negative += 1

    print("Total observations in table: {0}".format(len(predictions)))
    print("")
    print("Res.\Pred.\t|{0}\t|{1}\t| Row total".format(headers[0], headers[1]))
    print(" {0}\t\t| {1}\t| {2}\t| {3}".format(headers[0],
        true_negative, false_positive, row_negative))
    print(" {0}\t\t| {1}\t| {2}\t| {3}".format(headers[1],
        false_negative, true_positive, row_positive))
    print("Col. Tot.\t| {0}\t| {1}\t| {2}".format(column_negative,
        column_positive, len(predictions)))

def diff(vector):
    """Calculate the range of a vector.

    The range of a vector is the difference of the max and the min
    values of the vector.

    Args:
      vector (list): a vector of numbers.

    Returns:
      (number): the distance between the max value and the min value
      of the vector. Depending on the type of vector, it can be
      either an int or a float.
    """
    return (max(vector) - min(vector))

def findFreqTerms(matrix, qty):
    """Find all the entries in a sparse matrix that appears often.

    Args:
      matrix (list): a sparse matrix, preferably one generated from
        a Data Frame object.
      qty (int): the minimum amount of times an item should appear to
        be considered "frequent".

    Returns:
      (dictionary): a dictionary of all the terms that appear at least
      the specified amount of times.
    """
    freqTerms = dict()
    for row in matrix:
        for key in row:
            freq = int(row[key])
            if freq >= qty and len(key) > 1:
                freqTerms[key] = freq

    return freqTerms

def flip(p=0.5):
    """Implement a biased coin.
    
    This method represents a coin that returns True with probability
    of p. A number between 0 and 1 is selected uniformly at random, and
    if it is lower or equal to p, then True is returned.
    
    Args:
      p (float, optional): the probability of the coin to return True.
        It must be a value between 0 and 1. Defaults to 0.5.
        
    Returns:
      bool: True with probability p, and False with probability 1 - p.
      
    Raises:
      ValueError: if p is negative, or if it is higher than 1.
    """
    if p < 0 or p > 1:
        raise ValueError("P must be in the range [0, 1].")
    
    return (random.uniform(0, 1) < p)


def head(vector):
    """Print the first few values in the given vector.
    
    Args:
      vector (list): a list of elements.
    """
    print("{0}\t{1}\t{2}\t{3}\t{4}\t{5}".format(vector[0],
        vector[1], vector[2], vector[3], vector[4], vector[5]))

def IQR(vector):
    """Calculate the IRQ (Inter-Quantil Range) of the vector.
    
    IRQ is the difference between the first and the third quantiles.

    Args:
      vector (list): a list of numbers.

    Returns:
      (float): the IRQ of the vector.
    """
    svector = vector[:]
    quarts = quartile(svector)
    if isinstance(vector[0], float):
        return math.fabs(quarts[2] - quarts[0])
    else:
        return round(math.fabs(quarts[2] - quarts[0]))

def mean(vector):
    """Calculate the arithmetic mean of a vector.
    
    Args:
      vector (list): a list of numbers.

    Returns:
      (float): the arithmetic mean of the vector.
    """
    if len(vector) == 0:
        print("Vector is empty. It has no mean")
        return

    summa = 0;

    for number in vector:
        summa += number

    return summa / len(vector)

def median(vector):
    """Calculate the median of a vector.

    The median is the value that divides the vector in two
    equal halfs.

    If the vector has an even amount of elements, the median is
    the mean of the two elements that are in the middle. Otherwise,
    the median is the element that is exactly in the half of the
    vector.

    Args:
      vector (list): a list of numbers.

    Returns:
      (number): the median of the vector. Depending on the
      contents of the vector, it can be either a float or an int.
    """
    if len(vector) == 0:
        print("Vector is empty. It has no median")
    elif (len(vector) % 2) == 0:
        if isinstance(vector[0], float):
            return ((vector[len(vector) // 2]
                + vector[(len(vector) // 2) + 1]) / 2)
        else:
            return round((vector[len(vector) // 2]
                + vector[(len(vector) // 2) + 1]) / 2)
    else:
        return vector[int(math.ceil(len(vector) / 2))]

def normalize(vector):
    """Normalize a vector.

    This method uses the min-max technique to normalize the
    values, resulting in a vector with values in the range [0, 1]
    
    Args:
      vector (list): a list of numbers.

    Returns:
      (list): a list containing the normalized values of the
      given vector.
    """
    minimum = min(vector)
    maximum = max(vector)
    normalized_vector = list()

    for number in vector:
        normalized_vector.append(min_max_norm(number, minimum, maximum))

    return normalized_vector

def prop_table(vector, show=True):
    """Calculates a table with the proportion of values in a vector.

    Args:
      vector (list): a list of elements.
      show (boolean): if True, the calculated table will be printed.
        Defaults to False.

    Returns:
      (dictionary): a dictionary with a entry per unique element in the
      vector, with the proportion of that element as the value for each
      key.
    """
    tab = table(vector, False)

    for item in tab:
        value = tab[item]
        value = (value / len(vector))
        tab[item] = value

    if show:
        for key in tab:
            print("{0} :\t {1}".format(key, tab[key]))

    return dict

def quartile(vector):
    """Calculate the quartiles of a vector.

    Quartiles are the three elements that divide the vector in four
    parts of equal length, in the same way the median divides the
    vector in two equal halfs.

    Args:
      vector (list): a list of numbers.

    Returns:
      (list): a list with three elements: the quartiles of the vector,
      or None if the vector has no quartiles (for example, if it has)
      less than 4 elements.
    """
    quartiles = list()

    if len(vector) == 0:
        print("Vector is empty. It has no quartiles")
        return None
    elif(len(vector) < 4):
        print("Vector is lenght {0}. It has no quartiles".format(len(vector)))
        return None
    elif (len(vector) % 2) == 0:
        quartiles.append(median(vector[0:(len(vector)//2)]))
        quartiles.append(median(vector))
        quartiles.append(median(vector[(len(vector)//2) + 1:]))
    else:
        quartiles.append(median(vector[0:int(math.ceil(len(vector)/2))]))
        quartiles.append(median(vector))
        quartiles.append(median(vector[int(math.ceil(len(vector)/2)):]))

    return quartiles

def read_csv(filename, enc="utf-8"):
    """Open a CSV file and read its contents.
    
    Args:
      filename (string): the name of the file to be opened.
      enc (string): the encoding of the file. Defaults to utf-8

    Returns:
      (Data Frame): a Data Frame object, with the contents of the
      CSV file.
    """
    f = open(filename, mode="r", encoding=enc)

    headers = f.readline().replace("\n","").split(",")
    d = DataFrame(headers)

    for line in f:
        register = line.replace("\n","").split(",")
        columnIndex = 0
        for category in headers:
            try:
                if "." in register[columnIndex]:
                    d.data[category].append(float(register[columnIndex]))
                else: 
                    d.data[category].append(int(register[columnIndex]))
            except ValueError:
                d.data[category].append(register[columnIndex])				
            columnIndex+=1

    f.close()

    return d

def runif(amount):
    """Create a list of random ordered numbers.
    
    The amount specified is the length of the list. The number in it
    will range from 0 to amount, and they will not be repeated.
    
    Args:
      amount (int): the number of elements that will contain the list.
        It also will be de maximum number inside of it (exclusive).
        
    Returns:
      (list) a list of numbers pseudo-randomly ordered.
    """
    return random.sample(range(amount), amount)

def set_seed(s):
    """Set the seed for Rython's pseudo-random number generator.
    
    Args:
    s (int): the seed.
    """
    random.seed(s)

def std(vector):
    """Calculate the standard deviation of a vector.

    Standard deviation is a measure of how homogeneous is a vector.

    Args:
      vector (list): a list of numbers.

    Returns:
      (float): the standard deviation of the vector.
    """
    if len(vector) == 0:
        print("Vector is empty. It has no standard deviation")
    else:
        return math.sqrt(variance(vector))

def strc(dataframe):
    """Print the structure of a Data Frame.
    
    Args:
      dataframe (Data Frame): a Data Frame object.
    """
    print("data.frame: {0} obs. of {1} variables:".format(
        len(dataframe.data[dataframe.headers[0]]), len(dataframe.headers)))
    for category in dataframe.headers:
        print("{0}\t: {1} {2}".format(
            category, type(dataframe[category][0]),
            repr(dataframe[category][0:4])))

def summary(vector):
    """Print statistical information about a vector.

    The info printed includes the minimum and maximum value, the mean,
    medians and quartiles. The vector is not modified.

    Args:
      vector (list): a list of numbers.
    """
    svector = vector[:]
    svector.sort()

    minimum = min(svector)
    mmean = mean(svector)
    maximum = max(svector)
    quarts = quartile(svector)
    print("Min\t1st Q.\tMedian\tMean\t3rd Q.\tMax")
    print("{m}\t{q}\t{d}\t{p}\t{t}\t{x}".format(
        m=minimum, q=quarts[0], d=quarts[1], p=mmean, t=quarts[2], x=maximum))

def table(vector, show=True):
    """Calculates a frequency table of a vector.

    Args:
      vector (list): a list of objects.
      show (boolean): if True, the table will be printed. Defaults
        to True.

    Returns:
      (dictionary) a dictionary, with every unique element as a key,
      and the number of times said element appears as the value.
    """
    svector = vector[:]
    svector.sort()
    head = set(svector)
    tab = dict()

    for item in head:
        tab[item] = 0

    for item in vector:
        valor = int(tab[item])
        valor += 1
        tab[item] = valor

    if show:
        for key in tab:
            print("{0} :\t {1}".format(key, tab[key]))

    return tab

def variance(vector):
    """Calculates the variance of a vector.
    
    Variance is a statistical value that measures how
    diverse are the elements of the vector.

    Args:
      vector (list): a list of numbers.

    Returns:
      (float): the variance of the vector.
    """
    if len(vector) == 0:
        print("Vector is empty. It has no variance")
        return None

    m = mean(vector)
    sum = 0

    for number in vector:
        sum += ((number - m) ** 2)

    return (sum / len(vector))

def vector_range(vector):
    """Calculate the range of a vector.

    The range of a vector is the difference of the max and the min
    values of the vector.

    Args:
      vector (list): a list of numbers.

    Returns:
      (number): the range of the vector. Depending on the vector
      contents, it can be either a float or an int.
    """
    return (min(vector), max(vector))

def z_normalize(vector):
    """Normalize a vector.

    This method uses the z-score technique to normalize the
    values.
    
    Args:
      vector (list): a list of numbers.

    Returns:
      (list): a list containing the normalized values of the
      given vector.
    """
    minimum = min(vector)
    maximum = max(vector)
    normalized_vector = list()

    for number in vector:
        normalized_vector.append(z_score_norm(number, minimum, maximum))

    return normalized_vector

# ---------------------------------------------------------------------
#							Helper methods
#----------------------------------------------------------------------

def install_stopwords():
    """Brings the nltk window to install the stopwords"""
    # Tries to import the nltk module    
    try:
        import nltk
    except ImportError:
        print_usage(-1)

    # Shows the download window
    nltk.download()

def min_max_norm(value, mn, mx):
    """Normalize a value with the min-max technique.

    Args:
      value (number): the value to normalize.
      mn (number): the minimum value of the value's list.
      mx (number): the maximum value of the value's list.

    Returns:
      (number): the normalized value.
    """
    return ((value - mn) / (mx - mn))

def print_usage(code=0):
    """Print information about the correct use of the script.

    Args:
      code (int, optional): The exit code for the script. Defaults to 0.
    """
    print("USAGE: python(3) rython.py [-i] [--help]")
    print("  where:")
    print("\t-i:\tPops up a window to install the stopwords module.")
    print("\t--help:\tPrints this message.")
    print("WARNING: This script requires the nltk module to work properly.")
    print("\tIf not installed, try running the following command:\n")
    print("\t\tpip(3) install nltk\n")
    print("After that, run the script again. with the [-i] argument again.\n")
    print("\t\tpython(3) rython.py -i\n")
    print("Select 'Corpora' in the pop up window, then look for 'stopwords'")
    print("and click in 'Download'. Then you're ready to continue!")

    sys.exit(code)

def printer(msg):
    """Prints a message to the standard output.
    
    This method simulates a progress bar and is used to give the user
    an idea of how much time the algorithm will take to complete.
    
    Args:
      msg (str): the message to print in the standard output.
    """
    sys.stdout.write("\r" + msg)
    sys.stdout.flush()

def round(x):
    """Round a number.

    Args:
      x (number): the number to round.
      
    Return:
      (number): the rounded number.
    """
    if (x % 1) > 0.5:
        return int(math.ceil(x))
    else:
        return int(math.floor(x))	

def z_score_norm(value, mean, std):
    """Normalize a value with the z-score technique.

    Args:
      value (number): the value to normalize.
      mean (number): the mean value of the value's list.
      std (number): the standard deviation value of the value's list.

    Returns:
      (number): the normalized value.
    """
    return ((value - mean) / std)

if __name__ == '__main__':
    # Attempts to get parameters
    try:
        for i, arg in enumerate(sys.argv):
            if arg == '-i':
                install_stopwords()
            elif arg == '--help':
                print_usage()
    except ValueError:
        print_usage()
    except IndexError:
        print_usage()

    copyright()
