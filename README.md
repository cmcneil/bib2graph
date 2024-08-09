# bib2graph
![GitHub Issues or Pull Requests](https://img.shields.io/github/issues/cmcneil/bib2graph)

Turn a bibtex file into a 3d interactive citation graph!

![demo](https://github.com/cmcneil/bib2graph/blob/media/citegraph_demo.gif)

I find this useful because it provides the inverse function of websites like [connectedpapers.com](https://www.connectedpapers.com/).
Sometimes, rather than querying papers, you have a large list of papers already, and want to explore them
at a glance and decide what order to read things in. In addition, the semantic scholar API
can't share all abstracts for legal reasons, whereas your management software (such as Paperpile)
 is more likely to have the abstracts.

 It is unecessarily animated for fun.

## Usage
Getting started takes two commands. After downloading the repo, install dependencies:
```
pip3 install -r requirements.txt
```
Then just point the starter script at a .bib file!
```
source start.sh example.bib
```
The script will compile your graph, lookup citations using the [semanticscholar](https://api.semanticscholar.org/api-docs/) api, and then launch a Flask server so you can view the results in your browser.
