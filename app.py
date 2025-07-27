import os
from dotenv import load_dotenv
import google.generativeai as genai
from flask import Flask, render_template, request, jsonify

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configura a chave de API do Gemini
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

print(f"DEBUG: GEMINI_API_KEY (primeiros 5 caracteres): {GEMINI_API_KEY[:5] if GEMINI_API_KEY else 'NÃO CARREGADA'}")

if not GEMINI_API_KEY:
    raise ValueError("A variável de ambiente 'GEMINI_API_KEY' não está configurada.")

genai.configure(api_key=GEMINI_API_KEY)

# Inicializa o modelo Gemini
# Você pode escolher outros modelos como 'gemini-pro' ou 'gemini-1.5-flash'
model = genai.GenerativeModel('gemini-2.0-flash')
chat = model.start_chat(history=[]) # Inicia um chat com histórico vazio

@app.route('/')
def index():
    """Renderiza a página inicial com o formulário de chat."""
    return render_template('index.html')

@app.route('/send_message', methods=['POST'])
def send_message():
    """
    Recebe a mensagem do usuário, envia para o Gemini e retorna a resposta.
    """
    user_message = request.json.get('message')
    if not user_message:
        return jsonify({"response": "Por favor, digite uma mensagem."}), 400

    try:
        # Envia a mensagem do usuário para o Gemini e obtém a resposta
        response = chat.send_message(user_message)
        # Retorna apenas a parte de texto da resposta
        gemini_response = response.text
        return jsonify({"response": gemini_response})
    except Exception as e:
        # --- ADIÇÃO PARA DEBUG: Imprime o tipo e a representação completa da exceção ---
        import traceback
        print(f"Erro ao se comunicar com o Gemini: {type(e).__name__} - {e}")
        traceback.print_exc()  # Imprime o traceback completo para mais detalhes
        # --- FIM DA ADIÇÃO PARA DEBUG ---
        #print(f"Erro ao se comunicar com o Gemini: {e}")
        return jsonify({"response": "Desculpe, não consegui processar sua solicitação no momento."}), 500

if __name__ == '__main__':
    app.run(debug=True) # debug=True para desenvolvimento, use Gunicorn/uWSGI para produção