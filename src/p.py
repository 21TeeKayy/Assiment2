from ctypes import addressof
from genericpath import exists
from pickle import TRUE
from sqlite3 import dbapi2
import requests
import hashlib
from flask import Flask, render_template, request, flash, redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:04120412@localhost:5433/NFT'
app.config['SECRET_KEY'] = 'fdsffghffgdsfghjfdghfjk'
db = SQLAlchemy(app)

class Users(db.Model):
    username = db.Column(db.String,primary_key=True)
    pswd = db.Column(db.String)

    def __init__(self, username, pswd):
        self.username = username
        self.pswd = pswd
    
class NFT(db.Model):
    addres = db.Column(db.String,primary_key=True)
    nft_name = db.Column(db.String)
    inf = db.Column(db.String)
    url = db.Column(db.String)

    def __init__(self, addres, nft_name, inf, url):
        self.addres = addres
        self.nft_name = nft_name
        self.inf = inf
        self.url = url

@app.route('/')
def my_form_reg():
    return render_template('registr.html')
@app.route('/',methods=['POST'])
def my_form_reg2():
    username2 = request.form['username']
    psw = request.form['psw']
    x = Users.query.filter_by(username=username2).first()
    if x is None:
        salt = '5gzg1f2g'
        dataBase_password = psw+salt
        hashed = hashlib.md5(dataBase_password.encode())
        user = Users(username = username2, pswd = hashed.hexdigest())
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('nftsearching'))
    flash('NOT VALID INPUT')
    return render_template('registr.html')
@app.route('/login')
def my_form_log():
    return render_template('login.html')
@app.route('/login',methods=['POST'])
def my_form_log2():
    username = request.form['username']
    psw = request.form['psw']
    x = Users.query.filter_by(username=username).first()
    if x is None:
        flash('WRONG PASSWORD OR USERNAME')
        return render_template('login.html')
    x = Users.query.filter_by(username=username).first()
    password = x.pswd
    salt = '5gzg1f2g'
    dataBase_password = psw+salt
    hashed = hashlib.md5(dataBase_password.encode())
    if password != hashed.hexdigest():
        flash('WRONG PASSWORD OR USERNAME')
        return render_template('login.html')
    return redirect(url_for('nftsearching'))
@app.route('/nftsearching')
def nftsearching():
    return render_template('index.html')
@app.route('/nftsearching', methods=['POST'])
def my_form_address2():
    ans = ''
    nft = request.form['text']
    x = NFT.query.filter_by(addres=nft).first()
    if x is None:
        url = f"https://solana-gateway.moralis.io/nft/mainnet/{nft}/metadata"
        headers = {
            "accept": "application/json",
            "X-API-Key": "S77RJTmiMoBbTQTEed5MExSDfHQ2HolnDEXy7GZRoo3Eah6t1YAR20dfdGIJASaT"
        }    
        response = requests.get(url, headers=headers)
        ans = response.text
        index = ans.find("name")
        index2 = 0
        for element in range(index+7, len(ans)):
            if ans[element] == '"':
                index2 = element
                break
        name = ans[index+7:index2]
        index = ans.find("metadataUri")
        index2 = 0
        for element in range(index+14, len(ans)):
            if ans[element] == '"':
                index2 = element
                break
        url = ans[index+14:index2]
        z = NFT(addres = nft , nft_name = name, inf = response.text, url = url)
        db.session.add(z)
        db.session.commit()
    x = NFT.query.filter_by(addres=nft).first()
    info = x.inf
    url = x.url
    name = x.nft_name
    return render_template('index2.html', add = nft, n = name ,inf = info, u = url)
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)

