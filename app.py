import os
import re
from flask import Flask, render_template, request
from google import genai  
from dotenv import load_dotenv
from PyPDF2 import PdfReader

load_dotenv()
chave_api = os.getenv("GEMINI_API_KEY")

if not chave_api:
    raise ValueError("Erro: A chave GEMINI_API_KEY não foi encontrada no arquivo .env")

client = genai.Client(api_key=chave_api)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024
@app.errorhandler(413)
def arquivo_muito_grande(error):
    return render_template('index.html', 
                           categoria="Erro de Upload", 
                           resposta="O arquivo enviado é muito grande. O limite máximo é de 2MB.",
                           email_anterior=""), 413

# lista dos modelos // fallback
MODELOS_IA = [
    "gemini-2.5-flash",        
    "gemini-2.5-flash-lite",   
]

def limpar_texto(texto):
    #remove caracteres especiais e espaços extras
    if not texto: return ""
    texto_limpo = re.sub(r'[^\w\s.,?!@]', '', texto)
    texto_limpo = re.sub(r'\s+', ' ', texto_limpo)
    return texto_limpo.strip().lower()

def ler_pdf(arquivo):
    # extrai o texto puro de um arquivo pdf
    try:
        pdf = PdfReader(arquivo)
        texto_completo = ""
        for pagina in pdf.pages:
            texto_completo += pagina.extract_text() or ""
        return texto_completo
    except Exception as e:
        print(f"Erro ao ler PDF: {e}")
        return None

@app.route('/', methods=['GET', 'POST'])
def index():
    categoria = None
    resposta_sugerida = None
    email_original = None
    texto_para_textarea = None 
    
    if request.method == 'POST':
        texto_colado = request.form.get('email_texto')
        arquivo_pdf = request.files.get('email_arquivo')

        if arquivo_pdf and arquivo_pdf.filename != '':
            email_original = ler_pdf(arquivo_pdf)
            texto_para_textarea = "" 
        else:
            email_original = texto_colado
            texto_para_textarea = texto_colado

        if email_original:
            email_processado = limpar_texto(email_original)
            sucesso = False
            
            prompt = f"""
            Você é um assistente corporativo inteligente.
            Analise o seguinte email recebido: "{email_processado}"
            
            Tarefas:
            1. Classifique como "Produtivo" ou "Improdutivo".
            2. Escreva uma resposta sugerida curta e profissional.
            
            REGRAS DE RESPOSTA:
            - Escreva a resposta em primeira pessoa (como se fosse o usuário humano respondendo).
            - JAMAIS assine com o nome da IA ou "Assistente".
            - Termine o email EXATAMENTE com: "Atenciosamente, [Seu Nome]" ou "[Nome da Empresa]".
            
            Responda APENAS seguindo este formato exato:
            Categoria: [Sua Classificação]
            Resposta: [Sua Resposta Sugerida]
            """

            # loop para tentar os modelos disponíveis
            for nome_modelo in MODELOS_IA:
                try:
                    response = client.models.generate_content(
                        model=nome_modelo, 
                        contents=prompt
                    )
                    texto_retorno = response.text
                    sucesso = True
                    break 
                    
                except Exception as e:
                    print(f"Modelo {nome_modelo} indisponível: {e}")
                    continue 

            # resposta pós tentativa de escolher o modelo disponível
            if sucesso:
                if "Categoria:" in texto_retorno and "Resposta:" in texto_retorno:
                    partes = texto_retorno.split("Resposta:")
                    categoria = partes[0].replace("Categoria:", "").strip()
                    resposta_sugerida = partes[1].strip()
                else:
                    categoria = "Análise Geral"
                    resposta_sugerida = texto_retorno
            else:
                categoria = "Erro no Sistema"
                resposta_sugerida = "O sistema atingiu o limite de uso diário da IA. Por favor, tente novamente amanhã."

    return render_template('index.html', 
                           categoria=categoria, 
                           resposta=resposta_sugerida, 
                           email_anterior=texto_para_textarea)

if __name__ == '__main__':
    app.run(debug=False)