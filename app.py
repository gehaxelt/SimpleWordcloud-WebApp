from flask import Flask, render_template, request, url_for, redirect, g
from flask_bootstrap import Bootstrap
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import re

app = Flask(__name__)
Bootstrap(app)

app.clouds = {}

def init_cloud(cloudname):
    if not cloudname in app.clouds:
        app.clouds[cloudname] = {
            'words': [],
            'regen': False,
            'image': None
        }

@app.route('/')
def index():
    if request.args.get("cloudname", None):
        return redirect(url_for('viewcloud', cloudname=request.args.get("cloudname")))
    return render_template('index.html')

@app.route('/<cloudname>/view')
def viewcloud(cloudname):
    init_cloud(cloudname)
    wordcount = len(app.clouds[cloudname]['words'])

    if (app.clouds[cloudname]['regen'] or not app.clouds[cloudname]['image']) and wordcount > 0:
        wc = WordCloud(max_font_size=40, height=768, width=1024, background_color="grey").generate(' '.join(app.clouds[cloudname]['words']))
        image = wc.to_svg()
        app.clouds[cloudname]['image'] = image
        app.clouds[cloudname]['regen'] = False
    else:
        image = app.clouds[cloudname]['image']

    return render_template('viewcloud.html', cloudname=cloudname, wordcount=wordcount, image=app.clouds[cloudname]['image'])

@app.route('/<cloudname>')
def redir2view(cloudname):
    return redirect(url_for('viewcloud', cloudname=cloudname))
@app.route('/<cloudname>/')
def redir2view2(cloudname):
    return redirect(url_for('viewcloud', cloudname=cloudname))

@app.route('/<cloudname>/edit', methods=['GET', 'POST'])
def editcloud(cloudname):
    init_cloud(cloudname)

    if request.form.get('words', None):
        words = re.split(r'\s+|,',request.form.get('words'))
        app.clouds[cloudname]['words'] += words
        app.clouds[cloudname]['regen'] = True
    else:
        words = []

    return render_template('editcloud.html', cloudname=cloudname, added=len(words))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)