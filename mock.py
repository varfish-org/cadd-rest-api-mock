from flask import Flask, jsonify, request
from random import random
from uuid import uuid4
import sqlite3 as sl
import re


RE_VAR = (
    r"^(?P<contig>[a-zA-Z0-9\._])+-(?P<pos>\d+)-"
    "(?P<reference>[ACGTN]+)-(?P<alternative>[ACGTN]+)$"
)


app = Flask(__name__)
con_global = sl.connect('annotations.db')
with con_global:
    try:
        con_global.execute("""
            CREATE TABLE annotations (
                id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
                uuid TEXT,
                variant TEXT,
                score1 REAL,
                score2 REAL
            );
        """)
    except sl.OperationalError:
        pass


def _normalize_var(var, genomebuild):
    """Normalize variant regarding the ``"chr"`` prefix."""
    if genomebuild == "GRCh37":
        return var[3:] if var.startswith("chr") else var
    return var if var.startswith("chr") else ("chr" + var)


@app.route("/annotate/", methods=["POST"])
def annotate():
    con = sl.connect('annotations.db')
    uuid = str(uuid4())
    genomebuild = request.json["genome_build"]
    sql = "INSERT INTO annotations (uuid, variant, score1, score2) VALUES (?, ?, ?, ?)"
    data = [
        (uuid, _normalize_var(var, genomebuild), random(), random() * 10)
        for var in request.json["variant"]
        if re.search(RE_VAR, var)
    ]
    with con:
        con.executemany(sql, data)
    return jsonify({"uuid": uuid})


@app.route("/result/", methods=["POST"])
def results():
    con = sl.connect('annotations.db')
    uuid = request.json["bgjob_uuid"]
    with con:
        rows = con.execute("SELECT variant, score1, score2 FROM annotations WHERE uuid = ?", [uuid])
        response = {
            "status": "finished",
            "info": {"cadd_rest_api_version": 0.1},
            "scores": {row[0]: [row[1], row[2]] for row in rows},
        }
        con.execute("DELETE FROM annotations WHERE uuid = ?", [uuid])
    return jsonify(response)
