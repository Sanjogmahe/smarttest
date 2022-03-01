from flask import Flask, redirect, url_for, render_template, request, Response
import pandas as pd
import time

app = Flask(__name__)

@app.route('/')
def welcome():
    return render_template('index.html')


@app.route('/login_popup', methods=['GET', 'POST'])
def login_popup():

    
#    movies = pd.read_excel('movies.xls')
#    headings = list(movies.columns.values.tolist())
#    data = movies.to_numpy()
    
#    return render_template('index.html', headings=headings, data=data)
     return render_template('index.html')


@app.route('/extract_button')
def on_click():
	return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)