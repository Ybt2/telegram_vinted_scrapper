# Telegram Vinted Scraper 🤖👗

Um bot Telegram para pesquisa automática no Vinted, com permissões por utilizador, envio de fotos, título, preço e marca via comandos.

---

## 🔧 Funcionalidades

- Comando `/vinted <termo>`: pesquisa no [Vinted.pt](https://www.vinted.pt) pelo termo indicado (ex.: `jnco jeans`).
- Envia, por item encontrado:
  - Foto
  - Título, preço, marca, localização, estado e descrição curta
  - Botão com link direto para o Vinted

- **Restrito a utilizadores autorizados** (ids configuráveis).
- Logging de atividade num ficheiro `logs.txt`
- Parâmetro de fallback se o utilizador não inserir texto

---

## 🛠️ Pré-requisitos

- Python ≥ 3.8  
- Dependências:

```txt
python-telegram-bot==20.7
vinted-scraper>=2.4.0
httpx>=0.23.0
```

---

## Instalação

```bash
git clone https://github.com/Ybt2/telegram_vinted_scrapper.git
```

No codigo main.py, substituir o TOKEN pelo o do vosso BOT, e adicionar ids permitidos junto do nome da pessoa
