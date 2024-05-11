# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import google.generativeai as genai
import requests
import os

load_dotenv() # Carrega as variaveis .env

# Configura Gemini
google_api_key = secret_key = os.getenv('GOOGLE_API_KEY')
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
        # Obtém o JSON enviado na requisição
        data = request.get_json()

        # Aqui você pode adicionar o código para processar os dados recebidos
        print("Recebendo:")
        print(data)
        print(f'URL do arquivo: {data["fileUrl"]}')
        print(f'ID do Ticket: {data["idTicket"]}')
        print(f'ID da Mensagem: {data["idMensagem"]}')

        fileUrl = data['fileUrl']

        # URL do arquivo de áudio
        audio_url = fileUrl

        # Nome do arquivo de áudio local
        local_filename = "audio/ogg663ccf6bb5a8c.ogg"

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
            print(audioToText)
            # Detalhe o Audio
            response = convo.send_message("Imaginando que você é um atendente de supote de um sistema ERP, baseado neses audio me faço um comentario geral sobre ele e me passa qual o sentimento da pessoa.")
            emotionAudio = convo.last.text
            print(emotionAudio)

            return jsonify({"status": 200, "audioToText": audioToText, "emotionAudio": emotionAudio, "idTicket": data["idTicket"], "idMessage": data["idMensagem"]}), 200
        else:
            print("Erro ao baixar o arquivo de áudio:", response.status_code)
            return jsonify({"status": 400, "mensagem": "Dados recebidos com sucesso!", "url": fileUrl}), 200
    else:
        return jsonify({"status": "erro", "mensagem": "Formato de requisição inválido. JSON esperado."}), 400

if __name__ == '__main__':
    app.run(debug=True)
