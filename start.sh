#!/bin/bash

BIBPATH=$1
BIBDIR=(dirname $BIBPATH)
BIBFILE=(basename $BIBPATH .bib)
if [[ -f static/graphs_bib/$BIBFILE.bib ]]; then
    echo "$BIBFILE is already saved.";
else 
    echo "Caching $BIBFILE.bib";
    cp $BIBPATH static/graphs_bib/;
fi;

if [[ -f static/graphs_json/$BIBFILE.json ]]; then
    echo "Using cached graph $BIBFILE.json";
else
    echo "Generating new graph for $BIBFILE.bib...";
    python3 scripts/compile_graphs.py
    echo "Graph generation complete."
fi;

flask --app app.py run
