# -*- coding: utf-8 -*-
import pika
import json
import sqlite3
import datetime

config = configparser.ConfigParser()
config.read('config.ini')

cwuser = config['API']['USER']
cwpass = config['API']['PASS']
cwqueue = config['API']['QUEUE']

credentials = pika.PlainCredentials(cwuser, cwpass)
parameters = pika.ConnectionParameters(host='api.chtwrs.com',
                                       port=5673,
                                       virtual_host='/',
                                       credentials=credentials,
                                       ssl=True,
                                       socket_timeout=5)

connection = pika.BlockingConnection(parameters)
channel = connection.channel()

def saveRaw(store_list):
    conn = sqlite3.connect('finance.db')
    cursor = conn.cursor()
    result = cursor.execute('SELECT Count(*) FROM Resources').fetchone()
    if result[0] >= 8640:
        cursor.execute('DELETE FROM Resources WHERE rowid IN (SELECT rowid FROM Resources limit 1)')
    cursor.execute('INSERT INTO Resources \
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', \
        (datetime.datetime.now().strftime('%m-%d %H:%M'), \
        store_list['Thread']  if 'Thread' in store_list else 0, store_list['Stick']  if 'Stick' in store_list else 0, \
        store_list['Pelt'] if 'Pelt' in store_list else 0, store_list['Bone'] if 'Bone' in store_list else 0, \
        store_list['Coal'] if 'Coal' in store_list else 0, store_list['Charcoal'] if 'Charcoal' in store_list else 0, \
        store_list['Powder'] if 'Powder' in store_list else 0, store_list['Iron ore'] if 'Iron ore' in store_list else 0,\
        store_list['Cloth'] if 'Cloth' in store_list else 0, store_list['Silver ore'] if 'Silver ore' in store_list else 0,
        store_list['Magic stone'] if 'Magic stone' in store_list else 0, store_list['Sapphire'] if 'Sapphire' in store_list else 0, \
        store_list['Solvent'] if 'Solvent' in store_list else 0, store_list['Ruby'] if 'Ruby' in store_list else 0,\
        store_list['Hardener'] if 'Hardener' in store_list else 0, store_list['Steel'] if 'Steel' in store_list else 0, \
        store_list['Leather'] if 'Leather' in store_list else 0, store_list['Bone powder'] if 'Bone powder' in store_list else 0, \
        store_list['String'] if 'String' in store_list else 0, store_list['Coke'] if 'Coke' in store_list else 0, \
        store_list['Rope'] if 'Rope' in store_list else 0, store_list['Metal plate'] if 'Metal plate' in store_list else 0))
    conn.commit()
    conn.close()

def parcing(recieved):
    json_array = json.loads(recieved)
    store_list = {}
    for item in json_array:
        try:
            store_list[item['name']] = item['prices'][0]
        except KeyError:
            pass
    saveRaw(store_list)

number = 0
def callback(ch, method, properties, body):
    global number
    number += 1
    parcing(body)
    print(" [x] Received %r" % number)

channel.basic_consume(callback,
                      queue=cwqueue,
                      no_ack=True)
try:
    channel.start_consuming()
except KeyboardInterrupt:
    channel.stop_consuming()
connection.close()
