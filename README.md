# 📧 SmartMail AI

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.0-000000?style=flat&logo=flask&logoColor=white)
![Gemini AI](https://img.shields.io/badge/Google%20Gemini-API-8E75B2?style=flat&logo=google&logoColor=white)

> **Acesse o projeto online:** [https://smartmailai.onrender.com](https://smartmailai.onrender.com).
> 
> *Nota: Como a hospedagem é gratuita, o site pode levar uns 50 segundos para abrir na primeira vez (tempo do servidor ligar).*


---

## 📸 Preview

![Animação](https://github.com/user-attachments/assets/6d06925f-bdeb-404c-a656-585d1890f89a)

---


## 📝 Sobre

Este projeto é uma aplicação web que ajuda a gerenciar e responder e-mails de forma rápida. O objetivo era criar uma ferramenta que lê o conteúdo (texto colado ou PDF anexado), entende o contexto usando Inteligência Artificial e gera uma sugestão de resposta pronta.


### O que ele faz:
* **Lê anexos:** Extrai texto de arquivos PDF automaticamente.
* **Classifica:** Diz se o e-mail é "Produtivo" (importante) ou "Improdutivo" (spam/promoção).
* **Responde:** A IA escreve um rascunho de resposta profissional baseado no contexto.
* **Filtra:** Possui validação para impedir envio de arquivos muito grandes.

---

## 🛠️ Tecnologias

* **Python 3.12** 
* **Flask** 
* **Google Gemini API** 
* **PyPDF2** 
* **HTML/CSS/JS** 
* **Render** (Hospedagem)

---

## 💻 Como rodar localmente


### 1. Clonar o repositório
Abra o terminal e rode:
```bash
git clone https://github.com/beatrizkloss/SmartMailAI.git
cd SmartMailAI
```
### 2. Criar e Ativar o Ambiente Virtual

No Windows:

```bash
python -m venv venv
.\venv\Scripts\activate

```
No Linux ou Mac:
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar as dependências


```bash
pip install -r requirements.txt
```
### 4. Configurar a Chave API 

Na pasta raiz do projeto, crie um arquivo novo chamado **.env**
abra o arquivo e cole a seguinte linha:
GEMINI_API_KEY="COLE_SUA_CHAVE_AQUI"

Nota: Você tem que gerar sua chave no Google AI Studio. https://aistudio.google.com/

### 5. Rodar o programa

```bash
python app.py
```

## 👩‍💻 Autora
Desenvolvido por Beatriz Kloss.
