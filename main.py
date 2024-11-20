#
#   Trust Wind
#   Made by: Tiago Farinha, Gonçalo Marinho, Bernardo Melo
#   Date: 20/11/2024
#

from flask import Flask, redirect, request, render_template, send_file
import logging

title = "TrustWind"

app = Flask(__name__, static_folder="./static")
app.url_map.strict_slashes = False

app.config['TEMPLATES_AUTO_RELOAD'] = True

logging.basicConfig(level=logging.DEBUG)

@app.route("/")
def index():
    return render_template('/pages/index.html', title=title)
