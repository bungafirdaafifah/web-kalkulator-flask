from flask import render_template, current_app as app


@app.route('/')
def index():
    # contoh pengiriman variabel ke template
    return render_template('index.html', title='Beranda', message='Halo dari Flask + Jinja!')
