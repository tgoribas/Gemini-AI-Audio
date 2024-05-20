# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os
import re

load_dotenv() # Carrega as variaveis .env

endPontAppScript = os.getenv('ENPOINT_APPSCRIPT')

# Configura Gemini
google_api_key = os.getenv('GOOGLE_API_KEY')
genai.configure(api_key=google_api_key)

generative_config = {
    'candidate_count': 1,
    "temperature": 0.5
}

safety_settings = {
    "HARASSMENT": "BLOCK_MEDIUM_AND_ABOVE",
    "HATE": "BLOCK_MEDIUM_AND_ABOVE",
    "SEXUAL": "BLOCK_MEDIUM_AND_ABOVE",
    "DANGEROUS": "BLOCK_MEDIUM_AND_ABOVE"
}

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generative_config,
                              safety_settings=safety_settings)

# Flask
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "Google AI"
@app.route('/upload', methods=['POST'])
def upload_file():
    # Verifica se a requisição contém um JSON
    if request.is_json:
        data = request.get_json() # Obtém o JSON enviado na requisição
        pattern = r"([^/]+\.ogg)$"

        # Aqui você pode adicionar o código para processar os dados recebidos
        print("Recebendo:")
        print(data)

        fileUrl = data['fileUrl']
        audio_url = fileUrl  # URL do arquivo de áudio

        # Nome do arquivo de áudio local
        audio_name = re.search(pattern, audio_url)
        audioName = audio_name.group(1)
        local_filename = f"audio/{audioName}"

        # Baixe o arquivo de áudio da URL
        response = requests.get(audio_url, stream=True)

        # Verifique se o download foi bem-sucedido
        if response.status_code == 200:
            # Salve o arquivo de áudio baixado
            with open(local_filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)

            # Transcreva o arquivo de áudio local para texto e envie para o Gemini AI
            # (Utilize o código Python anterior para transcrição e envio)
            convo = model.start_chat(history=[
            {
                "role": "user",
                "parts": [genai.upload_file(local_filename)]
            }
            ])

            # Converte o Audio em Texto
            convo.send_message("Converta esse audio para texto")
            audioToText = convo.last.text
            # Detalhe o Audio
            response = convo.send_message("Imaginando que você é um atendente de supote de um sistema ERP, baseado neses audio me faço um comentario geral sobre ele e me passa qual o sentimento da pessoa.")
            emotionAudio = convo.last.text

            print(audioToText)
            print(emotionAudio)

            #Deleta Arquivo
            deletaArquivo(local_filename)

            jsonReturn = {"status": 200, "audioToText": audioToText, "emotionAudio": emotionAudio, "idTicket": data["idTicket"], "idMessage": data["idMensagem"]}

            sendAppScript(jsonReturn)
            # Endpoint AppScript
            # 

            return jsonify(jsonReturn), 200
        else:
            print("Erro ao baixar o arquivo de áudio:", response.status_code)
            return jsonify({"status": 400, "mensagem": "Dados recebidos com sucesso!", "url": fileUrl}), 200
    else:
        return jsonify({"status": "erro", "mensagem": "Formato de requisição inválido. JSON esperado."}), 400

def deletaArquivo(localArquivo):
    try:
        os.remove(localArquivo)
        print(f"O arquivo {localArquivo} foi deletado com sucesso.")
    except FileNotFoundError:
        print(f"O arquivo {localArquivo} não foi encontrado.")
    except PermissionError:
        print(f"Permissão negada para deletar o arquivo {localArquivo}.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar deletar o arquivo {localArquivo}: {e}")


def sendAppScript(json):
    print(f"URL: {endPontAppScript}")
    url = endPontAppScript
    headers = {'Content-Type': 'application/json'}
    payload = json
    
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        print('Dados enviados com sucesso!')
    else:
        print(f'Falha ao enviar dados. Status code: {response.status_code}')
        print('Response:', response.text)


if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
