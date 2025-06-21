from telegram.ext import Application, CommandHandler, CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
import vinted_scraper
import re
import time

TOKEN = "7964305003:AAFaaXLBWkL4Gm2vbFQw1P4asyVkHVkh9nA" #Deve ser colocado o ID do BOT
USER_IDS = {"Fred": 1499287034, "Chico": 6188292745, "Mário": 5139065584}  #Aqui pode colocar utilizadores que deseja usarem o seu BOT
# "{Username}": {user_ID}

def guardar_logs(mensagem, arquivo = 'logs.txt'):
    with open(arquivo, "a") as f:
        f.write(mensagem)

async def scrape_vinted(update: Update, context: CallbackContext):
    if update.effective_user.id not in USER_IDS.values():
        await update.message.reply_text("🚫 Acesso negado!")
        return
    
    # Verifica se há parâmetros (termo de busca) passados pelo usuário
    if context.args:
        search_text = " ".join(context.args)  # Junta os argumentos passados em um único texto
    else:
        await update.message.reply_text("You need to put something in front of it")
        search_text = "jnco jeans"  # Valor padrão, caso o usuário não passe nenhum parâmetro

    try:
        scraper = vinted_scraper.VintedScraper("https://www.vinted.pt")  # Inicializa o scraper com o URL base
        params = {
            "search_text": search_text  # Substitui o valor fixo por um valor dinâmico
        }
        
        # Obtenha a primeira página de itens
        items = scraper.search(params)
        
        responsavel = [nome for nome, id in USER_IDS.items() if id == update.effective_user.id]
        tempo = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        mensagem = f"[{tempo}] Encontrado(s) {len(items)} item(s) com a busca por '{search_text}' feita por {responsavel[0]}, {update.effective_user.id}\n"
        guardar_logs(mensagem)

        if items:
            
            
            # Envia cada item em uma mensagem separada
            for idx, item in enumerate(items, start=1): 
                #message = f"Item {idx}:\n"
                message = f"📌Título: {item.title}\n"
                message += f"💰Preço: {item.price}\n"
                message += f"🏷️marca: {item.brand.title}\n"
                message += f"📦Localização: {item.country}\n"
                message += f"✨Estado do Produto: {item.status}\n"
                message += f"💬Descrição: {item.description}\n"
                
                button = InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔗 Ver no Vinted", url=item.url)]
                ])

                imagem_url = None
                if item.photos:
                    match = re.search(r"url='(https?://[^']+)'", str(item.photos[0]))
                    if match:
                        imagem_url = match.group(1)

                if imagem_url:
                    await update.message.reply_photo(
                        photo=imagem_url,
                        caption=message,
                        reply_markup=button,
                        parse_mode="Markdown"
                    )
                else:
                    await update.message.reply_text(
                        message,
                        reply_markup=button,
                        parse_mode="Markdown"
                    )

        else:
            print(f"Nenhum item encontrado para a pesquisa '{search_text}'.")
            await update.message.reply_text(f"Nenhum item encontrado para a pesquisa '{search_text}'.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        await update.message.reply_text("🚫 Ocorreu um erro ao tentar buscar os itens.")

# Configuração do bot
app = Application.builder().token(TOKEN).build()

# Adiciona o comando /vinted
app.add_handler(CommandHandler("vinted", scrape_vinted))

# Inicia o bot
app.run_polling()
