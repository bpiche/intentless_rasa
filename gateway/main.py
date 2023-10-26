"""
"""
import os
import re
import json
import requests
import pandas as pd
from dotenv import load_dotenv
from flask import Flask, request


app = Flask(__name__)
load_dotenv = ('.env')


ai_host = os.environ.get('AI_HOST')
ai_port = os.environ.get('AI_PORT')
ai_scheme = os.environ.get('AI_SCHEME', 'http')
ai_base_url = f'{ai_scheme}://{ai_host}:{ai_port}'

rasa_host = os.environ.get('RASA_HOST', '127.0.0.1')
rasa_port = os.environ.get('RASA_PORT', '5005')
rasa_scheme = os.environ.get('RASA_SCHEME', 'http')
rasa_base_url = f'{rasa_scheme}://{rasa_host}:{rasa_port}'
rasa_token = os.environ.get('RASA_TOKEN')


@app.route('/rasa_nlu', methods=['POST'])
def get_rasa_response():
    """
    """
    url = f'{rasa_base_url}/webhooks/rest/webhook?token={rasa_token}'
    app.logger.info(f'web hook: {url}')
    # sender = request.values.get('sender')
    sender = 'jumpstart user'
    message = request.values.get('text')
    api_payload = {'sender': sender, 'message': message}
    nlu_payload = {'text': '%s' % message}
    try:
        with requests.Session() as s:
            api_response = s.post(url, json=api_payload)
        r = api_response.text
        app.logger.info(f'web hook: {r}')
        result = json.loads(r)
        nlu_url = f'{rasa_base_url}/model/parse?token={rasa_token}'
        # TODO: dont use this var name twice, or at least do it in a function
        nlu_response = s.post(nlu_url, json=nlu_payload)
        r = nlu_response.text
        app.logger.info(f'rasa nlu: {nlu_url}')
        app.logger.info(f'rasa nlu: {r}')
        data = json.loads(r)
        retrieval_intent = data['intent']['name']
        app.logger.info(retrieval_intent)
        new_result = {'IntentType': retrieval_intent,
                      'Message': result[0]['text']}
    except Exception as e:
        app.logger.error(f'{e}:')
        return None
    return new_result


@app.route('/rasa_health', methods=['POST'])
def get_rasa_health():
    """
    """
    url = f'{rasa_base_url}/'
    try:
        with requests.Session() as s:
            response = s.post(url)
        r = response.text
        data = json.loads(r)
    except Exception as e:
        app.logger.error(f'{e}:')
        return None
    return data


@app.route('/rasa_status', methods=['POST'])
def get_rasa_status():
    """
    """
    url = f'{rasa_base_url}/status'
    try:
        with requests.Session() as s:
            response = s.post(url)
        r = response.text
        data = json.loads(r)
    except Exception as e:
        app.logger.error(f'{e}:')
        return None
    return data


@app.route('/similarity', methods=['POST'])
def get_similarity():
    """
    """
    url = f'{ai_base_url}/similarity'
    user_text = request.values.get('text')
    payload = {'text': '%s' % user_text}
    try:
        with requests.Session() as s:
            app.logger.info(f'url: {url}')
            response = s.post(url, json=json.dumps(payload))
        r = response.text
        app.logger.info(f'res: {r}')
        data = json.loads(r)
    except Exception as e:
        return e, 500
    return data


@app.route('/livez', methods=['GET'])
def live():
    """
    """
    return "Live", 200


@app.route('/readyz', methods=['GET'])
def ready():
    """
    """
    url = f'{rasa_base_url}/'
    try:
        with requests.Session() as s:
            response = s.get(url)
        r = response.text
        return "Ready", 200
    except Exception as e:
        app.logger.error(f'{e}:')
        return "", 503


if __name__ == "__main__":
    """
    """
    print('Running the server on port 5000')
    sslctx = 'adhoc' if (os.environ.get('SERVE_HTTPS') 
                         in ['true', 'True', 'TRUE', True]
                     ) else None;
    app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=sslctx)
    