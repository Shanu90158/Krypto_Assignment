from flask import Flask, jsonify
import random
import psycopg2

app = Flask(__name__)


@app.route("/")
def start():
    return "go alert/create to add new alert \n go alert/delete to delete alert"


@app.route("/alert")
def hello_world():
    return "<p>ALERT!</p>"


@app.route("/alert/create/<int:c_uid>/<int:c_price>")
def createalert(c_uid, c_price):
    DBHOST = "http://172.0.0.1/"
    DBUSER = "postgres"
    DBPASS = "postgres"

    # conn = psycopg2.connect(dbname="postgres",user= DBUSER, password= DBPASS, host= DBHOST)
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres")

    cur = conn.cursor()
    cur.execute("select max(aid) from public.alert")
    aidr = cur.fetchone()
    aid = aidr[0] + 1
    data = (c_uid, aid, c_price)
    print(data)
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO public.alert(uid, aid, price, status, alerttime,coinid)VALUES (%s,%s,%s,false,now(),'BTC');", data)

    conn.commit()

    cur.close()
    conn.close()

    return "done. new alert created successfully "


@app.route("/alert/delete/<int:c_uid>/<int:aid>")
def deletealert(c_uid, aid):
    DBHOST = "http://127.0.0.1/"
    DBUSER = "postgres"
    DBPASS = "postgres"

    conn = psycopg2.connect(
        host="localhost",
        database="Krypto",
        user="postgres",
        password="1234")

    data = (aid, c_uid)
    cur = conn.cursor()
    cur.execute("DELETE FROM public.alert WHERE aid=%s and uid=%s;", data)
    conn.commit()
    cur.close()
    conn.close()

    return "alert deleted"


@app.route("/alert/myalert/<int:c_uid>")
def myalert(c_uid):
    DBHOST = "http://172.0.0.1/"
    DBUSER = "postgres"
    DBPASS = "postgres"

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="postgres")

    data = c_uid
    cur = conn.cursor()
    cur.execute("SELECT aid,coinid,price,status FROM public.alert WHERE uid=%s;", [c_uid])
    rv = cur.fetchall()
    print(rv)
    payload = []
    content = {}
    for result in rv:
        content = {'id': result[0], 'Coin': result[1], 'Price': result[2], 'Trigger Status': result[3]}
        payload.append(content)
        content = {}

    print(rv)
    return jsonify(payload)
    cur.close()
    conn.close()


app.run()