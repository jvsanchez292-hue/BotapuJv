import os
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from models.poisson import PoissonModel
from models.value_bet import detectar_value_bet
from services.api_football import obtener_prediccion, buscar_fixture
from services.odds_api import obtener_cuotas
from services.bankroll import kelly_stake

logging.basicConfig(level=logging.INFO)
TOKEN = os.environ.get("TELEGRAM_TOKEN")
BANKROLL_INICIAL = float(os.environ.get("BANKROLL", "100"))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "⚽ *Bot de Apuestas Estadísticas*\n\n"
        "Comandos disponibles:\n"
        "/analizar Equipo1 vs Equipo2\n"
        "/value - Value bets del día\n"
        "/bankroll - Estado actual\n"
        "/historial - Últimas apuestas\n",
        parse_mode="Markdown"
    )

async def analizar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    args = context.args
    if len(args) < 3 or args[1].lower() != "vs":
        await update.message.reply_text("Uso: /analizar Real Madrid vs Barcelona")
        return

    local, visitante = args[0], args[2]
    await update.message.reply_text(f"🔍 Buscando {local} vs {visitante}...")

    try:
        fixture = buscar_fixture(local, visitante)
        if not fixture:
            await update.message.reply_text("❌ No encontré ese partido próximamente.")
            return

        pred = obtener_prediccion(fixture["id"])
        if not pred:
            await update.message.reply_text("❌ Sin predicción disponible.")
            return

        p_local = pred["predictions"]["percent"]["home"] / 100
        p_empate = pred["predictions"]["percent"]["draw"] / 100
        p_visit = pred["predictions"]["percent"]["away"] / 100

        cuotas = obtener_cuotas(local, visitante)
        if not cuotas:
            await update.message.reply_text("⚠️ Sin cuotas disponibles todavía.")
            return

        mensaje = f"📊 *{local} vs {visitante}*\n\n"
        mensaje += f"Probabilidades modelo:\n"
        mensaje += f"• Local: {p_local:.1%}\n"
        mensaje += f"• Empate: {p_empate:.1%}\n"
        mensaje += f"• Visitante: {p_visit:.1%}\n\n"

        for mercado, prob, cuota in [
            ("Local", p_local, cuotas.get("home")),
            ("Empate", p_empate, cuotas.get("draw")),
            ("Visitante", p_visit, cuotas.get("away")),
        ]:
            if not cuota:
                continue
            info = detectar_value_bet(prob, cuota)
            if info["es_value"]:
                stake = kelly_stake(prob, cuota, BANKROLL_INICIAL)
                mensaje += (
                    f"✅ *VALUE BET: {mercado}*\n"
                    f"Cuota: {cuota} | Prob: {prob:.1%}\n"
                    f"Edge: {info['edge']:.1%} | Stake: ${stake}\n\n"
                )

        await update.message.reply_text(mensaje, parse_mode="Markdown")

    except Exception as e:
        logging.error(f"Error: {e}")
        await update.message.reply_text(f"⚠️ Error: {e}")

async def bankroll(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        f"💰 Bankroll actual: ${BANKROLL_INICIAL:.2f}\n"
        f"(Configúralo en la variable BANKROLL de Railway)"
    )

async def historial(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📜 Historial en construcción.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("analizar", analizar))
    app.add_handler(CommandHandler("bankroll", bankroll))
    app.add_handler(CommandHandler("historial", historial))
    print("✅ Bot corriendo...")
    app.run_polling()
