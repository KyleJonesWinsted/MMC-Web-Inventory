from flask import Flask, render_template
import view_controllers.browse
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('homepage.html')

@app.route('/browse')
def browse():
    return view_controllers.browse.setupView()
    

@app.route('/adjustments')
def adjustments():
    return render_template('adjustments.html')

@app.route('/settings')
def settings():
    return render_template('settings.html')

@app.route('/search')
@app.route('/search/<search_string>')
def search(search_string=""):
    return render_template('search.html', search_string=search_string)

if __name__ == '__main__':
    app.run(debug=True)
