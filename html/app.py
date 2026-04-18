from flask import render_template
from flask import Flask

app = Flask(__name__)

@app.get("/")
def index():
    return render_template("control.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)