from flask import Flask, request, jsonify
from dotenv import dotenv_values
from Crypto.Cipher import AES
from datetime import datetime
from flask_cors import CORS
import lzstring
import requests
import hashlib
import base64
import hmac
import json

app = Flask(__name__)
cors = CORS(app)

def setNoneIfEmpty(data):
    if data == '':
        return None

    return data

def decrypt(keys, encrypts):
    decompress = None

    if encrypts != None:
        x = lzstring.LZString()
        key_hash = hashlib.sha256(keys.encode('utf-8')).digest()

        decryptor = AES.new(key_hash[0:32], AES.MODE_CBC, IV=key_hash[0:16])
        plain = decryptor.decrypt(base64.b64decode(encrypts))
        decompress = json.loads(x.decompressFromEncodedURIComponent(plain.decode('utf-8')))
        
    return decompress

def rest_bpjs(consid, secret, url, method, payload, timestamp):
    message = consid+"&"+timestamp
    signature = hmac.new(bytes(secret,'UTF-8'),bytes(message,'UTF-8'), hashlib.sha256).digest()
    encodeSignature = base64.b64encode(signature)

    headers = {'X-cons-id': consid, 'X-timestamp': timestamp, 'X-signature': encodeSignature.decode('UTF-8'), 'Content-Type': 'Application/x-www-form-urlencoded','Accept': '*/*'}

    if payload == '' and payload == None :
        payload = 0
    else:
        payload = json.dumps(payload)
    
    if method == 'post':
        if payload == 0:
            res = requests.post(url, headers=headers)
        else:
            res = requests.post(url, data=payload, headers=headers)
    elif method == 'put':
        if payload == 0:
            res = requests.put(url, headers=headers)
        else:
            res = requests.put(url, data=payload, headers=headers)
    elif method == 'delete':
        if payload == 0:
            res = requests.delete(url, headers=headers)
        else:
            res = requests.delete(url, data=payload, headers=headers)
    else:
        if payload == 0:
            res = requests.get(url, headers=headers)
        else:
            res = requests.get(url, data=payload, headers=headers)

    return res

@app.route("/", methods=['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH'])
def bridging():
    if(request.method == 'POST'):
        header_host = request.headers.get('x-host')
        header_consid = request.headers.get('x-consid')
        header_secret = request.headers.get('x-secret')

        if setNoneIfEmpty(header_host) == None or setNoneIfEmpty(header_consid) == None or setNoneIfEmpty(header_secret) == None:
            config = dotenv_values(".env")
            host = config['HOST_BPJS']
            consid = config['CONSID']
            secret = config['SECRET']

        else:
            host = header_host
            consid = header_consid
            secret = header_secret

        is_json = False

        if request.headers.get('Content-Type') == 'application/json':
            is_json = True

        if is_json == False:
            url = host + request.form.get('url')
            method = request.form.get('method')
            payload = request.form.get('payload')

        else:
            data_json = request.json
            url = host + data_json['url']
            method = data_json['method']
            payload = data_json['payload']

        timestamp = str(int(datetime.today().timestamp()))

        if(not url or not method):
            data = {
                'metaData': {
                    'code': 400,
                    'message': "Pastikan untuk mengirim url, method dan/atau payload",
                },
                'response': None
            }

            return jsonify(data), 400

        res = rest_bpjs(consid, secret, url, method, payload, timestamp)

        if res.status_code != 404:
            keys = consid + secret + timestamp
            res = res.json()

            data = {
                'metaData': {
                    'code': res['metaData']['code'],
                    'message': res['metaData']['message'],
                },
                'response': decrypt(keys, res['response'])
            }

            return jsonify(data), res['metaData']['code']

        else:
            data = {
                'metaData': {
                    'code': 404,
                    'message': "URL tidak ditemukan",
                },
                'response': None
            }

            return jsonify(data), 404
    
    else:
        data = {
            'metaData': {
                'code': 405,
                'message': "Method dilarang, gunakan method POST",
            },
            'response': None
        }

        return jsonify(data), 405
    