import requests
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mplcol
import networkx as nx
from pybtex.database import parse_file
from pybtex.database.input import bibtex

import os
import json

def generate_graph_for_bib(fname):
    bib_fname = os.path.join("static", "graphs_bib", fname + ".bib")
    parser = bibtex.Parser()
    bib_data = parser.parse_file(bib_fname)
    entries = bib_data.entries    

    paper_details = {}
    paper_titles = {}

    # Fetch details for each paper
    for key, entry in entries.items():
        title = entry.fields.get('title', 'No title')
        doi = entry.fields.get('doi', 'No DOI')
        authors = entry.persons.get('author', 'Not found')
        abstract = entry.fields.get('abstract', 'Not found')
        authors = [author.first_names[0] + ', ' + author.last_names[0] for author in authors]
        paper_titles[key] = title
        uri = f'https://api.semanticscholar.org/graph/v1/paper/{doi}?fields=title,citationCount,year,references'
        headers = {
            # 'x-api-key': API_KEY,
        }
        lookup_response = requests.get(uri, headers=headers)
        if lookup_response.status_code == 200:
            paper_id = lookup_response.json().get('paperId', None)
            if lookup_response.json() is not None:
                paper_details[paper_id] = lookup_response.json()
                paper_details[paper_id]['short_name'] = key
                paper_details[paper_id]['doi'] = doi
                paper_details[paper_id]['authors'] = authors
                paper_details[paper_id]['abstract'] = abstract
    
    # Create Graph
    G = nx.DiGraph()
    # Add nodes and edges based on citations
    for key, details in paper_details.items():
        G.add_node(key, paper_id = details['paperId'], title=details['title'],
                citation_count=details.get('citationCount', 0), year=details.get('year', None),
                shortName=details['short_name'], doi=details['doi'],
                authors=details['authors'],
                abstract=details['abstract'])
        references = details.get('references', [])
        for ref in references:
            # ref_title = ref.get('title', '')
            paper_id = ref['paperId']
            for ref_key, ref_entry in paper_details.items():
                if paper_id == ref_entry['paperId']:
                    G.add_edge(key, ref_key)

    # Dump graph to JSON
    citation_counts = [G.nodes[node]['citation_count'] for node in G.nodes]
    years = [G.nodes[node]['year'] for node in G.nodes]
    year_min, year_max = min(years), max(years)
    nodes = [{'id': node, 'title': G.nodes[node]['title'], 
              'citationCount': G.nodes[node]['citation_count'], 
              'year': G.nodes[node]['year'],
              'size': 100 + 900 * (G.nodes[node]['citation_count'] / max(citation_counts)),
              'color': mplcol.rgb2hex(cm.plasma((G.nodes[node]['year'] - year_min) / (year_max - year_min))),
              'shortName': G.nodes[node]['shortName'], 'doi': G.nodes[node]['doi'],
              'authors': G.nodes[node]['authors'],
              'abstract': G.nodes[node]['abstract']} for node in G.nodes]
    links = [{'source': u, 'target': v} for u, v in G.edges()]
    graph_data = {'nodes': nodes, 'links': links}

    # Save the graph data to a JSON file
    with open(os.path.join('static', 'graphs_json', f'{fname}.json'), 'w') as f:
        json.dump(graph_data, f)

if __name__ == "__main__":
    cwd = os.getcwd()
    json_graph_files = {f.split(".")[0] for f in os.listdir(os.path.join(cwd, "static", "graphs_json"))}
    bib_graph_files = {f.split(".")[0] for f in os.listdir(os.path.join(cwd, "static", "graphs_bib"))}

    new_bibs = bib_graph_files - json_graph_files

    if new_bibs:
        print("recommit=true")
        for bib in new_bibs:
            generate_graph_for_bib(bib)
    else:
        print("recommit=false")