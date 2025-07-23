from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return "ربات در حال اجراست"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
