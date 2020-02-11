#!/usr/bin/env python
import json
import math
import os
import re
import sys

from PorterStemmer import PorterStemmer
from collections import defaultdict, Counter

class IRSystem:

    def __init__(self):
        # For holding the data - initialized in read_data()
        self.titles = []
        self.docs = []
        self.vocab = []
        # For the text pre-processing.
        self.alphanum = re.compile('[^a-zA-Z0-9]')
        self.p = PorterStemmer()


    def get_uniq_words(self):
        uniq = set()
        for doc in self.docs:
            for word in doc:
                uniq.add(word)
        return uniq


    def __read_raw_data(self, dirname):
        print("Stemming Documents...")

        titles = []
        docs = []
        os.mkdir('%s/stemmed' % dirname)
        title_pattern = re.compile('(.*) \d+\.txt')

        # make sure we're only getting the files we actually want
        filenames = []
        for filename in os.listdir('%s/raw' % dirname):
            if filename.endswith(".txt") and not filename.startswith("."):
                filenames.append(filename)

        for i, filename in enumerate(filenames):
            title = title_pattern.search(filename).group(1)
            print("    Doc %d of %d: %s" % (i+1, len(filenames), title))
            titles.append(title)
            contents = []
            f = open('%s/raw/%s' % (dirname, filename),'r',encoding='Latin-1')
            of = open('%s/stemmed/%s.txt' % (dirname, title),'w',encoding='Latin-1')
            for line in f:
                # make sure everything is lower case
                line = line.lower()
                # split on whitespace
                line = [xx.strip() for xx in line.split()]
                # remove non alphanumeric characters
                line = [self.alphanum.sub('', xx) for xx in line]
                # remove any words that are now empty
                line = [xx for xx in line if xx != '']
                # stem words
                line = [self.p.stem(xx) for xx in line]
                # add to the document's conents
                contents.extend(line)
                if len(line) > 0:
                    of.write(" ".join(line))
                    of.write('\n')
            f.close()
            of.close()
            docs.append(contents)
        return titles, docs


    def __read_stemmed_data(self, dirname):
        print("Already stemmed!")
        titles = []
        docs = []

        # make sure we're only getting the files we actually want
        filenames = []
        for filename in os.listdir('%s/stemmed' % dirname):
            if filename.endswith(".txt") and not filename.startswith("."):
                filenames.append(filename)

        if len(filenames) != 60:
            msg = "There are not 60 documents in ./data/RiderHaggard/stemmed/\n"
            msg += "Remove ./data/RiderHaggard/stemmed/ directory and re-run."
            raise Exception(msg)

        for i, filename in enumerate(filenames):
            title = filename.split('.')[0]
            titles.append(title)
            contents = []
            f = open('%s/stemmed/%s' % (dirname, filename), 'r')
            for line in f:
                # split on whitespace
                line = [xx.strip() for xx in line.split()]
                # add to the document's conents
                contents.extend(line)
            f.close()
            docs.append(contents)

        return titles, docs


    def read_data(self, dirname):
        """
        Given the location of the 'data' directory, reads in the documents to
        be indexed.
        """
        # NOTE: We cache stemmed documents for speed
        #       (i.e. write to files in new 'stemmed/' dir).

        print("Reading in documents...")
        # dict mapping file names to list of "words" (tokens)
        filenames = os.listdir(dirname)
        subdirs = os.listdir(dirname)
        if 'stemmed' in subdirs:
            titles, docs = self.__read_stemmed_data(dirname)
        else:
            titles, docs = self.__read_raw_data(dirname)

        # Sort document alphabetically by title to ensure we have the proper
        # document indices when referring to them.
        ordering = [idx for idx, title in sorted(enumerate(titles),
            key = lambda xx : xx[1])]

        self.titles = []
        self.docs = []
        numdocs = len(docs)
        for d in range(numdocs):
            self.titles.append(titles[ordering[d]])
            self.docs.append(docs[ordering[d]])

        # Get the vocabulary.
        self.vocab = [xx for xx in self.get_uniq_words()]

    def index(self):
        """
        Build an index of the documents.
        """
        print("Indexing...")
        # ------------------------------------------------------------------
        # TODO: Create an inverted index.
        #       Granted this may not be a linked list as in a proper
        #       implementation.

        inv_index = defaultdict(list)
        for indexDoc, doc in enumerate(self.docs):
            for word in set(doc):
                inv_index[word].append(indexDoc)
                
        self.inv_index = inv_index
        # ------------------------------------------------------------------

    def get_posting(self, word):
        """
        Given a word, this returns the list of document indices (sorted) in
        which the word occurs.
        """
        # ------------------------------------------------------------------
        # TODO: return the list of postings for a word.
        posting = self.inv_index[word]
        
        # ------------------------------------------------------------------
        return posting

    def get_posting_unstemmed(self, word):
        """
        Given a word, this *stems* the word and then calls get_posting on the
        stemmed word to get its postings list. You should not change
        this function. 
        """
        word = self.p.stem(word)
        return self.get_posting(word)

    #Function defined to compute the intersection between two arrays
    #This function takes advantage of the fact that arrays are sorted for efficiency purpose
    def intersection_arrays(self, array1, array2):
        i, j = 0, 0
        intersection = []
        while i < len(array1) and j < len(array2):
            if(array1[i] == array2[j]):
               intersection.append(array1[i])
               i = i+1
               j = j+1
            elif (array1[i] > array2[j]):
               j = j+1
            else:
               i = i+1

        return intersection
               
    def boolean_retrieve(self, query):
        """
        Given a query in the form of a list of *stemmed* words, this returns
        the list of documents in which *all* of those words occur (ie an AND
        query).
        Return an empty list if the query does not return any documents.
        """
        # ------------------------------------------------------------------
        # TODO: Implement Boolean retrieval. You will want to use your
        #       inverted index that you created in index().
        # Right now this just returns all the possible documents!
        aux = [] #Array in which we can keep the temporary intersection of inv_indexes 

        for word in set(query):
            if len(aux) == 0: #For the first word, we fill aux with the inv_index directly
                aux = self.inv_index[word]
            else: #After the first word, we calculate the intersection
                aux = self.intersection_arrays(aux, self.inv_index[word])

        return sorted(aux)   # sorted doesn't actually matter
        # ------------------------------------------------------------------
    
    def compute_tfidf(self):
        print("Calculating tf-idf...")
        # -------------------------------------------------------------------
        # TODO: Compute and store TF-IDF values for words and documents.
        #       Recall that you can make use of:
        #         * self.vocab: a list of all distinct (stemmed) words
        #         * self.docs: a list of lists, where the i-th document is
        #                   self.docs[i] => ['word1', 'word2', ..., 'wordN']
        #       NOTE that you probably do *not* want to store a value for every
        #       word-document pair, but rather just for those pairs where a
        #       word actually occurs in the document.

        tftd = defaultdict(Counter)
        tfidf = defaultdict(Counter)

        numberDocs = len(self.docs)
        
        for indexDoc in range(len(self.docs)):
            for word in self.docs[indexDoc]:
                if word not in tfidf:
                    tfidf[indexDoc][word] = {}
                tftd[indexDoc][word] += 1
                
                #Compute the actual value of the tfidf
                #Number of docs in which the word appears
                dft = len(self.get_posting(word))
                try:
                    tfidfValue = (1+math.log10(tftd[indexDoc][word]))*math.log10(float(numberDocs)/float(dft))
                    tfidf[indexDoc][word] = tfidfValue
                except ValueError: #In case we run into an issue with the log
                    print("The tfidf for the word " + word + " has not been computed nominally")
                    tfidf[indexDoc][word] = 0
                
        # ------------------------------------------------------------------
        self.tftd = tftd #Needed later on for the cosine similarity calculation
        self.tfidf = tfidf

    def get_tfidf(self, word, document):
        # ------------------------------------------------------------------
        # TODO: Return the tf-idf weigthing for the given word (string) and
        #       document index.
        tfidf = self.tfidf[document][word]
        # ------------------------------------------------------------------
        return tfidf


    def get_tfidf_unstemmed(self, word, document):
        """
        This function gets the TF-IDF of an *unstemmed* word in a document.
        Stems the word and then calls get_tfidf. You should not
        change this interface.
        """
        word = self.p.stem(word)
        return self.get_tfidf(word, document)


    def rank_retrieve(self, query):
        """
        Given a query (a list of words), return a rank-ordered list of
        documents (by ID) and score for the query.
        """
        scores = [0.0 for xx in range(len(self.docs))]
        # ------------------------------------------------------------------
        # TODO: Implement cosine similarity between a document and a list of
        #       query words.

        #Three main arguments needed: the tftd, tfidf for the document and the query
        #Let's compute the tfiqf of the query, by creating the tftq as before
        tftq = defaultdict(Counter)
        tfiqf = defaultdict(Counter)

        for word in query:
            if word not in tftq:
                tftq[word] = 1
            else:
                tftq[word] += 1

            tfiqf[word] = 1 + math.log10(tftq[word])

        #Now let's compute the cosine similarity for each document using all the ingredients calculated
        denominator1 = 0
        for word in tfiqf: #The first factor of the denominator only depends on the query, not the document
            denominator1 += (tfiqf[word])**2

        for indexDoc in range(len(self.docs)): #The score will be computed for each document
            numerator = 0 #To be initialized for each document
            denominator2 = 0

            for word in self.tfidf[indexDoc]:
                if word in query: #Sum of the numerator performed on words in the query and in the document
                    numerator += (tfiqf[word] * self.get_tfidf(word, indexDoc))
                denominator2 += (self.get_tfidf(word, indexDoc))**2

            if denominator1*denominator2 == 0.0:
                score = 0
            else:
                try:
                    score = numerator/(math.sqrt(1) * math.sqrt(denominator2))
                except ValueError:
                    print("Cosine similarity computation issue!")
        
            scores[indexDoc] = score
                
        #Sort the scores calculated
        ranking = [idx for idx, sim in sorted(enumerate(scores),
            key = lambda xx : xx[1], reverse = True)]
        results = []
        for i in range(10):
            results.append((ranking[i], scores[ranking[i]]))
        return results

    
    def process_query(self, query_str):
        """
        Given a query string, process it and return the list of lowercase,
        alphanumeric, stemmed words in the string.
        """
        # make sure everything is lower case
        query = query_str.lower()
        # split on whitespace
        query = query.split()
        # remove non alphanumeric characters
        query = [self.alphanum.sub('', xx) for xx in query]
        # stem words
        query = [self.p.stem(xx) for xx in query]
        return query


    def query_retrieve(self, query_str):
        """
        Given a string, process and then return the list of matching documents
        found by boolean_retrieve().
        """
        query = self.process_query(query_str)
        return self.boolean_retrieve(query)


    def query_rank(self, query_str):
        """
        Given a string, process and then return the list of the top matching
        documents, rank-ordered.
        """
        query = self.process_query(query_str)
        return self.rank_retrieve(query)


def run_tests(irsys):
    print("===== Running tests =====")
    ff = open('./data/queries.txt')
    questions = [xx.strip() for xx in ff.readlines()]
    ff.close()
    ff = open('./data/solutions.txt')
    solutions = [xx.strip() for xx in ff.readlines()]
    ff.close()

    epsilon = 1e-4
    for part in range(4):
        points = 0
        num_correct = 0
        num_total = 0

        prob = questions[part]
        soln = json.loads(solutions[part])

        if part == 0:     # inverted index test
            print("Inverted Index Test")
            words = prob.split(", ")
            for i, word in enumerate(words):
                num_total += 1
                posting = irsys.get_posting_unstemmed(word)
                if set(posting) == set(soln[i]):
                    num_correct += 1

        elif part == 1:   # boolean retrieval test
            print("Boolean Retrieval Test")
            queries = prob.split(", ")
            for i, query in enumerate(queries):
                num_total += 1
                guess = irsys.query_retrieve(query)
                if set(guess) == set(soln[i]):
                    num_correct += 1

        elif part == 2:   # tfidf test
            print("TF-IDF Test")
            queries = prob.split("; ")
            queries = [xx.split(", ") for xx in queries]
            queries = [(xx[0], int(xx[1])) for xx in queries]
            for i, (word, doc) in enumerate(queries):
                num_total += 1
                guess = irsys.get_tfidf_unstemmed(word, doc)
                if guess >= float(soln[i]) - epsilon and \
                        guess <= float(soln[i]) + epsilon:
                    num_correct += 1

        elif part == 3:   # cosine similarity test
            print("Cosine Similarity Test")
            queries = prob.split(", ")
            for i, query in enumerate(queries):
                num_total += 1
                ranked = irsys.query_rank(query)
                top_rank = ranked[0]
                if top_rank[0] == soln[i][0]:
                    if top_rank[1] >= float(soln[i][1]) - epsilon and \
                            top_rank[1] <= float(soln[i][1]) + epsilon:
                        num_correct += 1

        feedback = "%d/%d Correct. Accuracy: %f" % \
                (num_correct, num_total, float(num_correct)/num_total)

        print("    Score: %d Feedback: %s" % (num_correct*5, feedback))


if __name__ == '__main__':
    irsys = IRSystem()
    irsys.read_data('./data/RiderHaggard')
    irsys.index()
    irsys.compute_tfidf()
    args = sys.argv[1:]    
    if len(args) == 0:
        run_tests(irsys)
    else:
        query = " ".join(args)
        print("Best matching documents to '%s':" % query)
        results = irsys.query_rank(query)
        for docId, score in results:
            print("%s: %e" % (irsys.titles[docId], score))
