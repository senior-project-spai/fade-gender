from services.Gender.gender_predict import predict_gender
from utils import s3_helper

from PIL import Image
import os
from json import dumps, loads
from kafka import KafkaProducer
from kafka import KafkaConsumer

# log
import logging
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(name)s - %(message)s'))
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Get Environment variables
KAFKA_HOST = os.environ['KAFKA_HOST']
KAFKA_PORT = os.environ['KAFKA_PORT']
KAFKA_TOPIC_IMAGE = os.environ['KAFKA_TOPIC_IMAGE']
KAFKA_TOPIC_GENDER_RESULT = os.environ['KAFKA_TOPIC_GENDER_RESULT']

# display environment variable
logger.info('KAFKA_HOST: {}'.format(KAFKA_HOST))
logger.info('KAFKA_PORT: {}'.format(KAFKA_PORT))
logger.info('KAFKA_TOPIC_IMAGE: {}'.format(KAFKA_TOPIC_IMAGE))
logger.info('KAFKA_TOPIC_GENDER_RESULT: {}'.format(KAFKA_TOPIC_GENDER_RESULT))


def main():
    # TODO: Kafka Config
    consumer = KafkaConsumer(KAFKA_TOPIC_IMAGE,
                             bootstrap_servers=[
                                 '{}:{}'.format(KAFKA_HOST, KAFKA_PORT)],
                             auto_offset_reset='earliest',
                             enable_auto_commit=True,
                             group_id='gender-detection-group')

    producer = KafkaProducer(
        bootstrap_servers=['{}:{}'.format(KAFKA_HOST, KAFKA_PORT)])

    logger.info('Ready for consuming messages')
    for message in consumer:
        # de-serialize
        input_json = loads(message.value.decode('utf-8'))
        logger.info('Input JSON: {}'.format(dumps(input_json, indent=2)))

        # Get image from S3
        img_stream = s3_helper.get_file_stream_s3(
            input_json['image_path'])

        # inference
        predicted, detail = predict_gender(img_stream)
        formatted = {'gender': predicted, 'detail': detail}

        # Response
        gender_result = {'image_id': input_json['image_id'],
                         **formatted}
        logger.info('Gender Result JSON: {}'.format(
            dumps(gender_result, indent=2)))

        # Send to Kafka
        producer.send(KAFKA_TOPIC_GENDER_RESULT,
                      value=dumps(gender_result).encode('utf-8'))

if __name__ == '__main__':
    main()
