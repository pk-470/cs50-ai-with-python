import nltk
import sys
import os
import string
import math

FILE_MATCHES = 1
SENTENCE_MATCHES = 2


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python questions.py corpus")

    # Calculate IDF values across files
    files = load_files(sys.argv[1])
    file_words = {filename: tokenize(files[filename]) for filename in files}
    file_idfs = compute_idfs(file_words)

    # Prompt user for query
    query = set(tokenize(input("Query: ")))

    # Determine top file matches according to TF-IDF
    filenames = top_files(query, file_words, file_idfs, n=FILE_MATCHES)

    # Extract sentences from top files
    sentences = dict()
    for filename in filenames:
        for passage in files[filename].split("\n"):
            for sentence in nltk.sent_tokenize(passage):
                tokens = tokenize(sentence)
                if tokens:
                    sentences[sentence] = tokens

    # Compute IDF values across sentences
    idfs = compute_idfs(sentences)

    # Determine top sentence matches
    matches = top_sentences(query, sentences, idfs, n=SENTENCE_MATCHES)
    for match in matches:
        print(match)


def load_files(directory):
    """
    Given a directory name, return a dictionary mapping the filename of each
    `.txt` file inside that directory to the file's contents as a string.
    """
    file_contents = dict()
    for filename in os.listdir(directory):
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as f:
            next(f)
            file_contents[filename] = f.read()

    return file_contents


def tokenize(document):
    """
    Given a document (represented as a string), return a list of all of the
    words in that document, in order.

    Process document by coverting all words to lowercase, and removing any
    punctuation or English stopwords.
    """
    tokenized = nltk.tokenize.word_tokenize(document.lower())
    words = [
        token
        for token in tokenized
        if token not in string.punctuation
        and token not in nltk.corpus.stopwords.words("english")
    ]

    return words


def compute_idfs(documents):
    """
    Given a dictionary of `documents` that maps names of documents to a list
    of words, return a dictionary that maps words to their IDF values.

    Any word that appears in at least one of the documents should be in the
    resulting dictionary.
    """
    words = set()
    for document in documents:
        words.update(documents[document])

    idfs = dict()
    for word in words:
        contain_word = sum(word in documents[document] for document in documents)
        idf = math.log(len(documents) / contain_word)
        idfs[word] = idf

    return idfs


def top_files(query, files, idfs, n):
    """
    Given a `query` (a set of words), `files` (a dictionary mapping names of
    files to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the filenames of the the `n` top
    files that match the query, ranked according to tf-idf.
    """
    tfidfs = dict()
    for file in files:
        query_tfidf = 0
        for word in query:
            if word in files[file]:
                query_tfidf += files[file].count(word) * idfs[word]
        tfidfs[file] = query_tfidf

    files_tfidfs = list(files.keys())
    files_tfidfs.sort(reverse=True, key=lambda file: tfidfs[file])

    return files_tfidfs[:n]


def top_sentences(query, sentences, idfs, n):
    """
    Given a `query` (a set of words), `sentences` (a dictionary mapping
    sentences to a list of their words), and `idfs` (a dictionary mapping words
    to their IDF values), return a list of the `n` top sentences that match
    the query, ranked according to idf. If there are ties, preference should
    be given to sentences that have a higher query term density.
    """
    for sentence in sentences.copy():
        if sentence.startswith("=="):
            sentences.pop(sentence)

    sent_idfs_dict = dict()
    for sentence in sentences:
        query_idf = 0
        for word in query:
            if word in sentences[sentence]:
                query_idf += idfs[word]

        density = sum(sentences[sentence].count(word) for word in query) / len(
            sentences[sentence]
        )
        sent_idfs_dict[sentence] = (query_idf, density)

    sentences_idfs = list(sentences.keys())
    sentences_idfs.sort(reverse=True, key=lambda file: sent_idfs_dict[file])

    return sentences_idfs[:n]


if __name__ == "__main__":
    main()
