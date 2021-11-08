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

def checkDataExist(array):
    for data in array:
        if data == '' or data == None:
            return False

    return True

def decrypt(keys, encrypts):
    decompress = None

    if encrypts != None:
        x = lzstring.LZString()
        key_hash = hashlib.sha256(keys.encode('utf-8')).digest()

        decryptor = AES.new(key_hash[0:32], AES.MODE_CBC, IV=key_hash[0:16])
        plain = decryptor.decrypt(base64.b64decode(encrypts))
        decompress = json.loads(x.decompressFromEncodedURIComponent(plain.decode('utf-8')))
        
    return decompress

def rest_bpjs(consid, secret, user_key, url, method, payload, timestamp):
    message = consid+"&"+timestamp
    signature = hmac.new(bytes(secret,'UTF-8'),bytes(message,'UTF-8'), hashlib.sha256).digest()
    encodeSignature = base64.b64encode(signature)

    headers = {'X-cons-id': consid, 'X-timestamp': timestamp, 'X-signature': encodeSignature.decode('UTF-8'), 'user_key': user_key, 'Content-Type': 'Application/x-www-form-urlencoded','Accept': '*/*'}

    if payload == '' and payload == None :
        payload = 0
    else:
        payload = json.dumps(payload)
    
    if method.lower() == 'post':
        if payload == 0:
            res = requests.post(url, headers=headers)
        else:
            res = requests.post(url, data=payload, headers=headers)

    elif method.lower() == 'put':
        if payload == 0:
            res = requests.put(url, headers=headers)
        else:
            res = requests.put(url, data=payload, headers=headers)
    elif method.lower() == 'delete':
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
        header_user_key = request.headers.get('x-user_key')
        header_is_encrypt = request.headers.get('x-is_encrypt')

        if checkDataExist([header_host, header_consid, header_secret, header_user_key, header_is_encrypt]):
            host = header_host
            consid = header_consid
            secret = header_secret
            user_key = header_user_key
            is_encrypt = header_is_encrypt            

        else:
            config = dotenv_values(".env")
            host = config['HOST_BPJS']
            consid = config['CONSID']
            secret = config['SECRET']

            if 'IS_ENCRYPT' in config:
                is_encrypt = config['IS_ENCRYPT']
            else:
                is_encrypt = 1

            if 'USER_KEY' in config:
                user_key = config['USER_KEY']
            else:
                user_key = ''

        is_json = False

        if request.headers.get('Content-Type') == 'application/json':
            is_json = True

        if is_json == False:
            data = {
                'metaData': {
                    'code': 400,
                    'message': "Pastikan format body json dan menggunakan header Content-Type: application/json",
                },
                'response': None
            }

            return jsonify(data), 400

        else:
            data_json = request.json

            if('url' not in data_json or 'method' not in data_json or 'payload' not in data_json):
                data = {
                    'metaData': {
                        'code': 400,
                        'message': "Pastikan untuk mengirim url, method dan payload. Jika tidak ada data yang dikirim, payload : '' (string kosong)",
                    },
                    'response': None
                }

                return jsonify(data), 400

            url = host + data_json['url']
            method = data_json['method']
            payload = data_json['payload']

        timestamp = str(int(datetime.today().timestamp()))

        res = rest_bpjs(consid, secret, user_key, url, method, payload, timestamp)

        if res.status_code != 404:
            keys = consid + secret + timestamp
            res = res.json()

            if 'metaData' in res:
                metadata = 'metaData'

            else:
                metadata = 'metadata'

            if res[metadata]['code'] == 0:
                data = {
                    'metaData': {
                        'code': 400,
                        'message': res[metadata]['message'],
                    },
                    'response': None
                }

                return jsonify(data), 400

            if int(is_encrypt) == 1:
                response = decrypt(keys, res['response'])

            else:
                response = res['response']

            data = {
                'metaData': {
                    'code': res[metadata]['code'],
                    'message': res[metadata]['message'],
                },
                'response': response
            }

            return jsonify(data), res[metadata]['code']

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
    