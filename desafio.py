#!/usr/bin/env python3
import requests
import json
import string
import hashlib

def save_json(data):
    with open('answer.json', 'w') as f:
        json.dump(data, f)


def get_json():
    json_content = requests.get("https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=72c65b2f3aeb075b528336bef916f27209b5c5b5").json()

    save_json(json_content)

    return json_content

def get_alphabet():
    alphabet = dict.fromkeys(string.ascii_lowercase, 0)

    i = 0

    for key in alphabet.keys():
        alphabet[key] = i
        i+=1

    return alphabet

def decrypt(text, n):
    alphabet = get_alphabet()
    letters = string.ascii_lowercase
    original = ""
    
    for letter in text:
        if letter in letters:
            e = alphabet[letter]
            o = e - n

            original+=letters[o]
        else:
            original+=letter
    
    return original

def sha1(text):
    m = hashlib.sha1()
    m.update(text.encode('utf-8'))

    return m.hexdigest()

def send_response(json_content):
    with open('answer.json', 'r') as f:
        files = {'answer': f}
        r = requests.post("https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=72c65b2f3aeb075b528336bef916f27209b5c5b5", files=files)


try:
    json_content = get_json()

    original = decrypt(json_content['cifrado'], json_content['numero_casas'])
    json_content['decifrado'] = original

    resumo = sha1(original)
    json_content['resumo_criptografico'] = resumo

    save_json(json_content)

    send_response(json_content)

    print('Desafio concluído')
except:
    print('Não foi possível completar o desafio')