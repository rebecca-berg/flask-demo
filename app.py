from flask import Flask, render_template, request, redirect
import datetime as dt
import requests
import pandas as pd
from scipy.signal import savgol_filter
from pandas import DataFrame,Series
import bokeh
from bokeh.layouts import row, column
from bokeh.models import ColumnDataSource, DataRange1d, Select, HoverTool
from bokeh.palettes import Blues4
from bokeh.plotting import figure, show
from bokeh.embed import components
import quandl 


quandl.ApiConfig.api_key = 'Vs3cWugn6dzDVsY6y9Jt'

app = Flask(__name__)    


def make_plot(stock_symb):
	# Build the Dataframe
	today = dt.date.today()
	today_str = "&end_date=" + today.strftime("%Y-%m-%d")

	month_ago = today - dt.timedelta(days=30)
	month_ago_str = "&start_date=" + month_ago.strftime("%Y-%m-%d")
	
	mydata = quandl.get("WIKI/%s"%(stock_symb), start_date=month_ago_str, end_date=today_str)
	mydata = mydata["Close"]
	mydata.reset_index(inplace=True)
	
	TOOLS = [HoverTool()]
	
	p= TimeSeries(mydata, x="Date", ylabel="Stock Prices at Closing", plot_height=300, tools=TOOLS)
	script, div = components(p)
	
	return script, div
	
@app.route('/')
def main():
	return redirect('/index')

@app.route('/index', methods=['GET','POST'])
def index():
	return render_template('index.html')

@app.route('/plotpage', methods=['POST'])
def plotpage():
	stock_symb = request.form['tickerText'].upper()
	try:

		script, div = make_plot(stock_symb)
		return render_template('plot.html', ticker = stock_symb, script = script, div = div )

	except:

		return render_template('plot.html', error = " <h2>Error \n Double-check the spelling "
													"of your ticker, not found in "
													"dataset.</h2>", ticker = stock_symb )

if __name__ == '__main__':
  app.run(port=33507)

