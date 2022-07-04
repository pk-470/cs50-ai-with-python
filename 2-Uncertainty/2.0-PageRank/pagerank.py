import os
import random
import re
import sys
import numpy

DAMPING = 0.85
SAMPLES = 100000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(link for link in pages[filename] if link in pages)

    return pages


# ----------------------------------------------------RANDOM-SAMPLING-MODEL----------------------------------------------------


def transition_model(corpus, current_page, damping_factor):
    n = len(corpus)
    distribution = []
    for page in corpus:
        if not corpus[current_page]:
            distribution.append(1 / n)
        elif page not in corpus[current_page]:
            distribution.append((1 - damping_factor) / n)
        else:
            distribution.append(
                (1 - damping_factor) / n + damping_factor / len(corpus[current_page])
            )

    return distribution


def sample_pagerank(corpus, damping_factor, n):
    distributions = {
        page: transition_model(corpus, page, damping_factor) for page in corpus
    }
    visits = {page: 0 for page in corpus}
    current_page = random.choice(list(corpus))
    visits[current_page] = 1
    for _ in range(n - 1):
        current_page = random.choices(
            list(corpus), weights=distributions[current_page]
        )[0]
        visits[current_page] += 1

    ranks = {page: visits[page] / n for page in corpus}

    return ranks


# ---------------------------------------------------MARKOV-CHAIN-MODEL----------------------------------------------------------


def transition_matrix(corpus, damping_factor):
    n = len(corpus)
    pages = list(corpus)
    p = numpy.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if not corpus[pages[i]]:
                p[i, j] = 1 / n
            elif pages[j] not in corpus[pages[i]]:
                p[i, j] = (1 - damping_factor) / n
            else:
                p[i, j] = (1 - damping_factor) / n + damping_factor / len(
                    corpus[pages[i]]
                )

    return p


def iterate_pagerank(corpus, damping_factor):
    p = transition_matrix(corpus, damping_factor)
    old_p = p.copy()
    while True:
        new_p = numpy.matmul(p, old_p)
        if (numpy.absolute(new_p - old_p) < 0.001).all():
            break
        old_p = new_p.copy()

    ranks = {page: new_p[0, j] for j, page in enumerate(corpus)}

    return ranks


if __name__ == "__main__":
    main()
