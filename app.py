import sys
from flask import Flask, render_template, send_file, jsonify

sys.path.append("collect_tweet/")
from twitter_elasticsearch_util import clear, search, location_search

app = Flask(__name__)
elastic_host = "search-twittmap-wf-tos22nd6jgkyhdhvbptnb4pv7a.us-east-1.es.amazonaws.com"


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/clear/<keyword>")
def clear(keyword=None):
    return clear(elastic_host, keyword)


@app.route("/searchf/<keyword>")
def searchf(keyword):
    result = search(elastic_host, keyword)
    return jsonify(result)


@app.route('/images/<filename>')
def get_image(filename=None):
    return send_file('static/images/' + filename, mimetype='image/png')


if __name__ == "__main__":
    app.run(host='0.0.0.0')
