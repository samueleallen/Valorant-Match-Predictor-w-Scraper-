from flask import Flask, render_template

app = Flask(__name__, template_folder="website/templates", static_folder="website/static")

@app.route("/")
def index():
    return render_template('index.html')

@app.route('/standings')
def standings():
    return render_template('standings.html')

if __name__ == '__main__':
    # Set debug=True for auto reloads during development
    app.run(debug=True)