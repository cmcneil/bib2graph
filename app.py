from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route("/")
def list_graphs():
    graphs = [os.path.basename(f).split('.')[0] for f in 
              os.listdir("static/graphs_json")]
    print(graphs)
    return render_template("list_graphs.html",
                            graphs=graphs)


@app.route("/<bib_filename>")
def citegraph(bib_filename):
    return render_template("index.html", bib_filename=bib_filename)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=True)