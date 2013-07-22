from flask import Flask, request, session, g, redirect, url_for, \
    abort, render_template, flash
import csv

app = Flask(__name__)
app.config.from_object('fl_config')


def parse_csv_to_chords(f):
    """
    Takes a comma separated square matrix in as an input and parses it for
    a chord layout.
    """
    reader = csv.reader(f, delimiter=",")
    data, ids, matrix = {}, [], []
    header = reader.next()

    for i in header:
        ids.append(str(i))

    for line in reader:
        row = []
        for val in line:
            row.append(float(val))
        matrix.append(row)

    data['ids'] = ids
    data['data'] = matrix

    return data


def parse_csv_to_stacked_bar_graph(files):
    """
    Takes a comma separated file and parses it for a stacked bar graph layout.
    Each column in the csv should represent a column in the bar graph, with the
    headers corresponding to the displayed ids of each column.
    """
    pass


def render_graph(graph_type, update_url):
    if graph_type == "chord":
        return render_template('chord.html', update_url=update_url)
    elif graph_type == "stacked_bar_graph":
        return render_template('stacked_bar_graph.html', update_url=update_url)


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/chord/<update_url>')
def chord(update_url):
    return render_template('chord.html', update_url=update_url)


@app.route('/stacked_bar_graph/<update_url>')
def stacked_bar_graph(update_url):
    return render_template('stacked_bar_graph.html', update_url=update_url)


@app.route('/analyze_dynamic_data', methods=["GET", "POST"])
def analyze_dynamic_data():
    """
    Takes in a URL that spits out the json values needed for the selected graph
    type.
    """
    if request.method == "GET":
        return render_template('analyze_dynamic_data.html')
    elif request.method == "POST":
        gtype, u = request.form['gtype'], request.form['update_url']
        return render_graph(gtype, u)


@app.route('/analyze_csv', methods=["GET", "POST"])
def analyze_csv():
    """
    Accepts a csv file WITH A HEADER and a graph type from a form.
    The header should correspond to the ids of the nodes
    """
    if request.method == "GET":
        return render_template('analyze_csv.html')
    elif request.method == "POST":
        title = request.form['title']
        gtype, f = request.form['gtype'], request.files['csv_file']
        if gtype == "chord":
            data = parse_csv_to_chords(f)
            data['title'] = title
            return render_template('chord.html', one_shot_data=data)


if __name__ == '__main__':
    app.config['DEBUG'] = True
    app.run()
