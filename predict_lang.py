#imports
import itertools
import numpy as np
import string as st
import sys

# take input and output file args and run the program
def predictLang() :
    # get input and output file names from command line
    inF = sys.argv[1]
    outF = sys.argv[2]
    # reference dict
    refD = genRefTri()
    # make dictionary from input file
    inDict = dictMaker(inF)
    # calculate similarities
    langSimDict = langSims(inDict, refD)
    # generate output file
    langSimFile(langSimDict, outF)

# generate all possible trigrams (space + ascii-lowercase)
def genRefTri() :
    # use space and ascii lowercase alphabet
    base = ' ' + st.ascii_lowercase
    # list permutations of base
    refList = [''.join(x) for x in itertools.product(base, repeat = 3)]
    # make a dictionary from the refList w/ counts initialized to zero
    refDict = dict.fromkeys(refList, 0.0)
    return refDict

# take in input file f
# return dict of key:langLib val:{dict w/ lang as keyword and string (combined contents) as val} 
# and key:unknown val: {dict of filename as key and contents as string as val}
def dictMaker(f) :
    # dictionary of langLib and unknown dictionaries
    fileDict = {}
    # language libary dictionary
    langLib = {}
    # dictionary of unknowns
    unknDict = {}
    # open the file and read its contents
    with open(f, 'r') as file :
        # for each line:
        for line in file :
            # split at space (default)
            lList = line.split()
            # language
            lang = lList[0].lower()
            # file name
            fName = lList[1]
            # extract file contents
            fCont = fileToString(fName)
            # if unknown, read into string and add to unknowns
            if lang == 'unknown' :
                unknDict[fName] = fCont
            # if lang
            else :
                # if key (lang) already in dict, fileToString and append to value
                if lang in langLib.keys() :
                    langLib[lang] += fCont
                # else, add new entry
                else :
                    langLib[lang] = fCont
    # add unknown and language dicitionaries to file dictionary
    fileDict['unknowns'] = unknDict
    fileDict['langLib'] = langLib

    return fileDict

# take in a file f and return it as a string
def fileToString(f) :
    # open the file in read mode
    with open(f, 'r') as file :
        # read the file into a string
        fString = file.read()
    return fString

# take in dict d with an unknown dict and a dict of lang and reference tuple rT, vectorize each dict,
# and run cosine similarity for each lang for each unknown
# return unknown dict updated with nested dict w/ cossim for each language
def langSims(d, rT) :
    # language libary dictionary
    langLib = vectorDict(d['langLib'], rT)
    # dictionary of unknowns
    unknDict = vectorDict(d['unknowns'], rT)
    # make dict for unknown similarities
    unSimDict = {}
    # iterate over unknowns
    for uName in unknDict.keys() :
        # trigram vector for curr unknown
        uVect = unknDict[uName]
        # create a dict of similarity to each given language from langLib
        langSimDict = {}
        for lang in langLib.keys():
            # trigram vector for current language
            lVect = langLib[lang]
            # find cosine similarity
            sim = cosSim(uVect, lVect)
            # use similarity as key
            langSimDict[sim] = lang
        # add the filename of the unknown and the langauge predictions to the dictionary
        unSimDict[uName] = langSimDict
    return unSimDict

# take in dictionary d of key to string pairings and a reference dict rD
# get vects for each key, make dict of key to vect pairings
def vectorDict(d, rD) :
    # vector dictionary
    vectDict = {}
    # iterate over input dictionary and add key/vector pair for each
    for key in d.keys() :
        vector = vectorizeString(d[key], rD)
        vectDict[key] = vector
    return vectDict

# clean a string and turn it into a vector
# takes in a string and reference dict
def vectorizeString(s, rD) :
    # clean
    s = cleanString(s)
    # vectorize
    return countVector(s, rD)

# clean up input text (to lowercase, numbers and punctuation and extra spaces)
# takes in string s to clean
def cleanString(s) :
    # to lowercaseascii-lowercase + 
    s = s.lower()
    # remove puntatuation and numbers
    exList = st.punctuation + st.digits
    s = ''.join(x for x in s if x not in exList)
    # replace all new lines with white space
    s = s.replace('\n', ' ')
    # replace all sequences of white space with a single white space
    s = ' '.join(s.split())
    return s

# takes in string s to analyze and reference dict rD
# slice string by 3 (trigram) -> find trigram (key) in dict and val+=1
# use sorted keys to order and normalize counts into list, and return it as array
def countVector(s, rD) :
    # copy to avoid changing original reference dictionary
    countDict = rD.copy()
    # iterate over string in trigrams
    for triGT in zip(s[0::], s[1::], s[2::]) :
        triG = ''.join(triGT)
        # check to make sure that have not reached trailing chars
        if len(triG) == 3 :
            # update count
            countDict[triG] += 1.0
    # list of normalized frequencies
    countList = []
    # get keys into list and sort
    keyList = sorted(countDict.keys())
    # total number of trigrams
    totT = sum(countDict.values())
    # make values list using ordered keys and normalize each
    for key in keyList :
        count = countDict[key]
        countList.append(count/totT)
    # to array
    normCountArr = np.array(countList)
    return normCountArr          

# cosine similarity function
# takes in two vectors, a and b, and returns their cosine similarity
def cosSim(a, b) :
    # dot product
    dotP = np.dot(a, b)
    # magnitudes
    normA = np.linalg.norm(a)
    normB = np.linalg.norm(b)
    # cosine similarity
    return dotP / (normA * normB)

# take in dict d w/ unknown file names and nested dict w/ cossim for each language 
# and print to given output oF file
def langSimFile(d, oF) :
    # open file for writing and reading
    with open(oF, 'w+') as f :
        outString = ''
        # iterate over unknown filenames
        for uName in d :
            # add file name
            outString += uName + '\n'
            langSimDict = d[uName]
            # list of similarities sorted desccending
            simDescList = sorted(langSimDict.keys(), reverse=True)
            # add all similarities to file as percents with one decimal point
            for sim in simDescList :
                lang = langSimDict[sim]
                sim = '{:.1%}'.format(sim)
                langString = '\t' + lang + ' ' + sim + '\n'
                outString += langString
        # write to file
        f.write(outString)


if __name__ == '__main__' :
    sys.exit(predictLang())