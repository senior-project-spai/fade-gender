import json
from loguru import logger
import numpy as np
import requests
from requests.exceptions import ConnectionError


def prediction_call(target: str, data: np.ndarray):
    data = json.dumps(
            {
                'signature_name': 'serving_default',
                'instances': data.tolist()
            })
    headers = {'content_type': 'application/json'}
    target = f'{target}:predict'
    try:
        json_response = requests.post(target, data=data, headers=headers)
    except ConnectionError:
        logger.error(f"Cannot connect to tf-server {target}. FAILED.")
        raise ConnectionError
    try:
        predictions = json.loads(json_response.text)['predictions']
    except Exception as e:
        logger.error(f"Unable to obtain result: {str(type(e).__name__)}")
        logger.error(f"Dumps: {json_response.text}")
        raise Exception(json_response.text) from e
    return predictions
