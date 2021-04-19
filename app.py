from flask import Flask, render_template, request, redirect
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField
from wtforms.validators import DataRequired
import requests
import pandas as pd
import simplejson as json
import numpy as np
import os
from bokeh.layouts import gridplot
from bokeh.plotting import figure, show, output_file
from bokeh.embed import components

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(32)
bootstrap = Bootstrap(app)

def get_data (symbol):
  url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY' + '&symbol={}&apikey=Y1BD47K4VT0VB7BK'.format(symbol)
  return requests.get(url).json()

def construct_df(symbol):
  req = get_data(symbol)
  df = pd.DataFrame(req['Time Series (Daily)']).transpose()
  df['Date']=pd.to_datetime(df.index)
  return df

def datetime(x):
  return np.array(x, dtype=np.datetime64)

def construct_plot(symbol):
  df = construct_df(symbol)
  plt = figure(x_axis_type="datetime", title="Closing Prices")
  plt.grid.grid_line_alpha= 0.5
  plt.xaxis.axis_label = 'Date'
  plt.yaxis.axis_label = 'Price'
  plt.line(datetime(df['Date']), df['4. close'])
  
  return plt

class Input(FlaskForm):
  symbol = StringField('Please enter stock code', validators=[DataRequired()])
  submit = SubmitField('Submit to view closing price')

@app.route('/', methods=['GET','POST'])
def index():
  """form = Input()
  output = ""
  if form.validate_on_submit():
    symbol = form.symbol.data
    p = construct_plot(symbol)
    script, div = components(p)
    output = script + div"""

  return render_template('index.html')

@app.route('/about', methods=['POST'])
def about():
  symbol = request.form['tickerInput'].upper()
  plot = construct_plot(symbol)
  script, div = components(plot)

  return render_template('about.html', script=script, div=div)

if __name__ == '__main__':
  app.run(port=33507)
