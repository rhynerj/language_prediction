### Description

This project uses trigram frequencies to predict the language of one or more documents based on a sample of documents where the language is known. Predictions are made by comparing the cosin similarity between the unknown documents and the known documents in each language, and are returned as probabilities for each language. The bigger the sample of reference documents, the more accurate the prediction. Trigram frequencies are normalized, so the length and number of documents only matters for accuracy (and processing time) purposes.

### Implementation Instructions
Download the *predict_lang.py* file and place it in the same folder as your sample set of known and unknown .txt files. These files must contain only ASCII characters. The *test_files* folder contains a set of example documents. In this same folder, create an input .txt file. In this file, list each language and file name seperated by a space. For example, "French ftest1.txt". Write each languange and file name on a new line.For your unknown files, write "Unknown" and the file name. See *input.txt* for an example of what your input text file should look like.

Open a terminal and make sure you are in the directory that contains *predict_lang.py*, your known and unknown documents, and your input file. In the command line, type:

**python predict_lang.py input.txt output.txt**

where "input.txt" is the name of your input file and "output.txt" is the name you want for your output file. The program uses Python's File write() method, so it will create the file if it does not exist, but will overwrite the file if it does. If you run the program multiple times and want to save previous results, make sure to use unique names for the output files. The output file will list the name of each unknown file followed by the percentage probability that the file is in each of the provided languages. See *output.txt* for an example.