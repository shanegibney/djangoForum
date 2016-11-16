from flask import Flask, render_template, Response
from json import dumps

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/searchForm')
def searchForm():
	return render_template("searchForm.html")


@app.route('/showMeAjax')
def woohoo():
    return render_template('shanelayout.html')

@app.route('/hello')
def hello():
    return "Hello There"


@app.route('/search')
def search():
	data = [
		{'date': "12/27/2012", 'http_404': 2, 'http_200': 190, 'http_302': 100},
		{'date': "12/28/2012", 'http_404': 2, 'http_200': 10, 'http_302': 100},
		{'date': "12/29/2012", 'http_404': 1, 'http_200': 300, 'http_302': 200},
		{'date': "12/30/2012", 'http_404': 2, 'http_200': 90, 'http_302': 0},
		{'date': "12/31/2012", 'http_404': 2, 'http_200': 90, 'http_302': 0},
		{'date': "01/01/2013", 'http_404': 2, 'http_200': 90, 'http_302': 0},
		{'date': "01/02/2013", 'http_404': 1, 'http_200': 10, 'http_302': 1},
		{'date': "01/03/2013", 'http_404': 2, 'http_200': 90, 'http_302': 0},
		{'date': "01/04/2013", 'http_404': 2, 'http_200': 90, 'http_302': 0},
		{'date': "01/05/2013", 'http_404': 2, 'http_200': 90, 'http_302': 0},
		{'date': "01/06/2013", 'http_404': 2, 'http_200': 200, 'http_302': 1},
		{'date': "01/26/2013", 'http_404': 1, 'http_200': 200, 'http_302': 100},
		{'date': "09/05/2014", 'http_404': 2, 'http_200': 47, 'http_302': 23},
		{'date': "05/04/2014", 'http_404': 19, 'http_200': 147, 'http_302': 0},
		{'date': "07/06/2015", 'http_404': 2, 'http_200': 66, 'http_302': 67},
		{'date': "01/07/2015", 'http_404': 100, 'http_200': 12, 'http_302': 88}
		]

	dat = dumps(data)
	resp = Response(response=dat, status=200)
	resp.headers['Content-Type'] = 'application/json; charset=utf-8'
	resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp





if __name__ == '__main__':
    app.run(debug=True)
