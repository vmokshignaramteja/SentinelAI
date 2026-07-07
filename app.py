from flask import Flask, render_template, jsonify, Response
from io import StringIO
import csv
from database import (
    get_packets,
    get_statistics,
    get_alerts,
    export_packets
)

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/packets")
def packets_api():
    return jsonify(get_packets())


@app.route("/stats")
def stats_api():
    return jsonify(get_statistics())

@app.route("/alerts")
def alerts_api():
    return jsonify(get_alerts())

@app.route("/download_csv")
def download_csv():

    output = StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "Time",
        "Source IP",
        "Destination IP",
        "Protocol",
        "Size"
    ])

    for row in export_packets():
        writer.writerow(row)

    return Response(
        output.getvalue(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=packet_logs.csv"
        }
    )

@app.route("/login")
def login():
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)