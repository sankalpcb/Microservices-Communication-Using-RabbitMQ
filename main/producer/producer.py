from flask import Flask
import pika

app = Flask(__name__)



RABBITMQ_HOST = "172.18.0.2"
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = "health_check"
RABBITMQ_EXCHANGE = "student_exchange"
RABBITMQ_ROUTING_KEY = "health_check"


@app.route('/')
def index():
    return 'Eureka!'


@app.route('/healthcheck')
def Ack():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='health_check', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='health_check',
        body="Health check message sent",
        properties=pika.BasicProperties(
            delivery_mode=2,  # persistent
        ))
    connection.close()
    print("Health check message sent")
    return "Health check message sent\n"

# @app.route('/health_check')
# def health_check():
#     message = "RabbitMQ connection is healthy"
#     send_message_to_rabbitmq(RABBITMQ_QUEUE, message)
#     return "Health check message sent to RabbitMQ"

@app.route('/insert_record/<SRN>/<Name>/<Section>', methods=["POST"])
def insert_record(SRN,Name,Section):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    b= SRN+"."+Name+"."+Section
    channel = connection.channel()
    channel.queue_declare(queue='insert_record', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='insert_record',
        body= b,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        ))
    connection.close()
    print(" Message to insert record sent")
    return " Message to insert record sent " 

@app.route('/delete_record/<SRN>', methods=["GET"])
def delete_record(SRN):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    b= SRN
    channel = connection.channel()
    channel.queue_declare(queue='delete_record', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='delete_record',
        body= b,
        properties=pika.BasicProperties(
            delivery_mode=2, 
        ))
    connection.close()
    print(" Message to delete record sent")
    return " Message to delete record sent " 

@app.route('/read_database/', methods=["GET"])
def read_database():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='read_database', durable=True)
    channel.basic_publish(
        exchange='',
        routing_key='read_database',
        body="Read Database message sent",
        properties=pika.BasicProperties(
            delivery_mode=2,  
        ))
    connection.close()
    print(" Message to retrieve all records sent")
    return " Message to retrieve all records sent " 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
    # app.run(debug=True, host='127.0.0.1')
