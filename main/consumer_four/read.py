import pika
import time
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
import socket
import certifi
import pymongo
from pymongo.mongo_client import MongoClient

app = Flask(__name__)

uri = "mongodb+srv://adarsh_nayak:asn%40uk581314@cluster0.bnit9.mongodb.net/test"


client = MongoClient(uri,tlsCAFile=certifi.where())
db = client['studentdb']
collection = db["student"]
sleepTime = 20
time.sleep(sleepTime)
print('Consumer_four connecting to server ...')
connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
channel = connection.channel()
channel.queue_declare(queue='read_database', durable=True)


# def callback(ch, method, properties, body):
#     mydb = mysql.connector.connect(
#         host="localhost",
#         user="root",
#         password="password",
#         database="students"
#     )

#     mycursor = mydb.cursor()

#     mycursor.execute("SELECT * FROM student")

#     rows = mycursor.fetchall()
#     result = [{'name': row[0], 'srn': row[1], 'section': row[2]} for row in rows]

#     print(f"Retrieved {len(result)} records from the database"
#     ch.basic_ack(delivery_tag=method.delivery_tag)

def callback(ch, method, properties, body):
    ans = collection.find({})
    for document in ans:
        print(document)
    # ch.basic_publish(
    #     exchange='',
    #     routing_key=properties.reply_to,
    #     properties=pika.BasicProperties(correlation_id=properties.correlation_id),
    #     body=json.dumps(result)
    # )
    ch.basic_ack(delivery_tag=method.delivery_tag)
    return "Database read"

    
channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='read_database', on_message_callback=callback)
channel.start_consuming()