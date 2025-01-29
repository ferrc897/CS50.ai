import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


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
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    prob_distribution = dict()
    for pages in corpus:
        prob = (1 - damping_factor) / len(corpus)
        prob_distribution.update({pages: prob})
        if pages in corpus[page]:
            prob_distribution.update({pages: prob + (damping_factor / len(corpus[page]))})
    return prob_distribution



def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
   
    PageRank = dict()
    for pages in corpus:
        PageRank.update({pages: 0})

    page = random.choice(list(corpus.keys()))
    PageRank.update({page: PageRank[page] + 1 / n})
    
    for _ in range(n-1):
        probability = transition_model(corpus, page, damping_factor)
        page = random.choices(list(probability.keys()), list(probability.values()))[0]
        PageRank.update({page: PageRank[page] + 1 / n})
    
    return PageRank



def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    PageRank = dict()
    print(corpus)
    for page in corpus:
        PageRank.update({page: 1 / len(corpus)})
    
    for _ in range(20):
        for p in corpus:
            pr = (1 - damping_factor) / len(corpus)

            sum = 0
            for i in corpus:
                if p in corpus[i]:
                    sum += PageRank[i] / len(corpus[i])

            pr = pr + (damping_factor * sum)
            PageRank.update({p: pr})
    
    return PageRank


if __name__ == "__main__":
    main()
