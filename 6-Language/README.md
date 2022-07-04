# [Week 6 - Language](https://cs50.harvard.edu/ai/2020/weeks/6/)

## Module description

This module introduces various techniques used in Natural Language Processing. In particular, it first focuses on how an AI can understand syntax and generate syntactically correct sentences, introducing the concept of context-free grammar and the Python library _nltk_. Topics covered include:

- n-grams;
- Tokenization;
- Markov models.

The module then focuses on the task of making an AI that can extract meaning from language. The bag-of-words model is introduced, and an application of bayesian techniques is shown, with the aim to deduce whether an online review of a product is positive or negative. Moreover, the module introduces the problem of information retrieval and extraction, i.e. the task of finding relevant text in response to a user query. The Python library _tf-idf_ along with concepts such as Inverse Document Frequency are introduced. The module concludes with an overview of how words can be represented as vectors in an AI in a way such that vectors that are close together represent words with similar meanings.

## Projects

The module includes two project assignments:

### [Project 6.0: Parser](https://cs50.harvard.edu/ai/2020/projects/6/parser/)

The aim of this project is to create an AI that can correctly parse sentences (i.e. determine their structure given a list of grammar rules) and extract the basic noun phrases of a sentence. This is achieved with the help of the nltk library.

### [Project 6.1: Questions](https://cs50.harvard.edu/ai/2020/projects/6/questions/)

The goal of this project is to write an AI that can search through a corpus of documents and extract useful information in response to some user query.
