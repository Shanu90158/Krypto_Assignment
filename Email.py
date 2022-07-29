import requests
import psycopg2
import time
import smtplib


def sendemail(uid, aid, price, email):
    mailsrv = smtplib.SMTP('smtp.gmail.com', 587)
    mailsrv.starttls()
    mailsrv.login('pleaseuseurown@gmail.com ', '1234567890')
    body = 'Crypto Alert !! : ' + str(uid) + 'bitcoin alert: ' + str(
        aid) + ' is triggered!' + ' it has reached the price:' + str(price)
    print(body)
    mailsrv.sendmail("shanu", email, body)
    mailsrv.quit()


def readq():
    DBHOST = "http://127.0.0.1/"
    DBUSER = "postgres"
    DBPASS = "postgres"

    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="postgres",
        password="1234")

    cur = conn.cursor()
    cur.execute('SELECT uid,aid,price,email from public.alertq;')
    result = cur.fetchall()
    if (len(result) > 0):
        for r in result:
            uid = r[0]
            aid = r[1]
            price = r[2]
            email = r[3]
            qinput = (r[0], r[1], r[2])
            sendemail(uid, aid, price, email)
            cur.execute('Delete from public.alertq where uid=%s and aid=%s and price=%s;', qinput)
            conn.commit()
    else:
        print("No results found")
    cur.close()
    conn.close()


if __name__ == "__main__":
    sum = 0
    while (sum < 1000):
        readq()
        time.sleep(10)
        sum = sum + 1
