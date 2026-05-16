from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "Halo, selamat datang di aplikasi web Flask pertama Anda!"

if __name__ == '__main__':
    app.run(debug=True)