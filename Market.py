import requests
import psycopg2
import time


def fulltime():
    response = requests.get('https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false')
    data = response.json()
    print(data)

    marketprice = data['bitcoin']['usd']
    print(marketprice)

    DBHOST = "http://127.0.0.1/"
    DBUSER = "postgres"
    DBPASS = "postgres"

    conn = psycopg2.connect(
        host="localhost",
        database="Krypto",
        user="postgres",
        password="1234")

    cur = conn.cursor()
    # cur.execute('SELECT uid,aid,price from public.alert where price=%s and status=false',[marketprice])
    cur.execute(
        'SELECT alert.uid,alert.aid,alert.price, userdata.email from public.alert left join public.userdata on alert.uid=userdata.uid where price=%s and status=false',
        [50000])
    result = cur.fetchall()
    if (len(result) > 0):
        for r in result:
            price = r[2]
            data = (r[1], r[0])
            qinput = (r[0], r[1], r[2], r[3])
            cur.execute('UPDATE public.alert SET status= true, alerttime= now() WHERE aid=%s and uid=%s;', data)
            cur.execute('INSERT INTO public.alertq(uid, aid, price,email)VALUES (%s, %s, %s,%s);', qinput)

            conn.commit()

        else:
         print("Didn't found any alert")

    cur.close()
    conn.close()


if __name__ == "__main__":
    sum = 0
    while (sum < 1000):
        fulltime()
        time.sleep(10)
        sum = sum + 1
