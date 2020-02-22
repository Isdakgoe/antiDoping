
from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import pandas as pd
import numpy as np
from flask_bootstrap import Bootstrap

use_col = "     -----     "
use_key = "     -----     "

data_xlsx = pd.ExcelFile('data/200218_antiDoping.xlsx').parse()
data_dic_original = {ind: [v for v in data_xlsx.loc[ind].values] for ind in data_xlsx.index}
data_col = list(data_xlsx.columns)
search_dic = {}
for c, col in enumerate(data_col):
    data_temp = data_xlsx.iloc[:, c]
    key_list = [v for v in set(data_temp) if v != "-"]
    search_dic[col] = sorted(key_list)


"""
box = []
for ind in data_xlsx.index:
    for No, v in enumerate(data_xlsx.loc[ind].values):
        if No == 4:
            if (str(v) != "nan") and ("(" in v):
                name = v.split("(")[0]
                hospital = v.split("(")[1].split(")")[0]
            else:
                name = v
                hospital = ""

            print(name, hospital)
            box += [name]

temp = pd.DataFrame(box)
temp.to_csv("a.csv", encoding="cp932")
"""

app = Flask(__name__, static_url_path="")
bootstrap = Bootstrap(app)

DATA_DIR = "./data"
@app.route('/data/<path:path>')
def send_js(path):
    return send_from_directory(DATA_DIR, path)


@app.route('/')
def index():
    app.config['data_dic'] = data_dic_original
    app.config['search_dic'] = search_dic
    app.config['use_col'] = use_col
    app.config['use_key'] = use_key

    return render_template('index_bootStrap.html',
                           data_col=data_col, data_dic=app.config['data_dic'], search_dic=app.config['search_dic'],
                           use_col=app.config['use_col'], use_key=app.config['use_key'])


@app.route('/data_refine', methods=['POST', 'GET'])
def data_refine():
    print("A", request.form["btn"])
    if request.form["btn"] == "全て表示":
        app.config['data_dic'] = data_dic_original
        app.config['use_col'] = use_col
        app.config['use_key'] = use_key

    elif request.form["btn"] == "絞り込む":
        app.config['use_col'] = request.form.get('select_refine1')
        app.config['use_key'] = request.form.get('select_refine2')
        index_use = [ind for ind in list(data_xlsx.index) if data_xlsx.loc[ind, app.config['use_col']] == app.config['use_key']]
        app.config['data_dic'] = {ind: [v for v in data_xlsx.loc[ind].values] for ind in index_use}

    return render_template('index_bootStrap.html',
                           data_col=data_col, data_dic=app.config['data_dic'], search_dic=app.config['search_dic'],
                           use_col=app.config['use_col'], use_key=app.config['use_key'])


if __name__ == '__main__':
    app.run(debug=True)
