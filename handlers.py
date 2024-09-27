import logging
from telegram import Update
from telegram.ext import (
    CommandHandler, MessageHandler, CallbackQueryHandler,
    ConversationHandler, ContextTypes, Application
)
from telegram.ext import filters
from services.bot_service import BotService
from services.admin_service import AdminService
from config import ADMIN_USER_ID
from constants import CHOOSING, TYPING_REPLY, ADMIN_BROADCAST

bot_service = BotService()
admin_service = AdminService()
logger = logging.getLogger(__name__)

def setup_handlers(application: Application):
    # Обработчики команд
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('stats', show_stats))
    application.add_handler(CommandHandler('admin', admin_panel))

    # ConversationHandler для админских функций
    admin_conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(bot_service.handle_admin_button, pattern='^admin_.*$')],
        states={
            ADMIN_BROADCAST: [
                MessageHandler(filters.TEXT & (~filters.COMMAND), admin_service.handle_broadcast_message)
            ],
        },
        fallbacks=[CommandHandler('start', start)],
        per_chat=True,  # Устанавливаем per_chat=True
    )
    application.add_handler(admin_conv_handler)

    # ConversationHandler для изменения интересов
    conv_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(change_interests, pattern='^change_interests$')],
        states={
            TYPING_REPLY: [MessageHandler(filters.TEXT & (~filters.COMMAND), save_interests)],
        },
        fallbacks=[CommandHandler('start', start)],
        per_chat=True,  # Устанавливаем per_chat=True
    )
    application.add_handler(conv_handler)

    # Обработчики CallbackQuery
    application.add_handler(CallbackQueryHandler(button_handler))

    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.PHOTO, handle_quest_photos))
    application.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_quest_text))

    # Обработчик ошибок
    application.add_error_handler(error_handler)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot_service.handle_start(update, context)

async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_USER_ID:
        await admin_service.handle_show_stats(update, context)
    else:
        await update.message.reply_text("У вас нет прав доступа к этой команде.")

async def admin_panel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_USER_ID:
        await bot_service.send_admin_panel(update, context)
    else:
        await update.message.reply_text("У вас нет прав доступа к этой команде.")

async def change_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot_service.handle_change_interests(update, context)
    return TYPING_REPLY

async def save_interests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot_service.handle_save_interests(update, context)
    return ConversationHandler.END

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot_service.handle_button(update, context)

async def handle_quest_photos(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot_service.handle_quest_photos(update, context)

async def handle_quest_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await bot_service.handle_quest_text(update, context)

async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logger.error(msg="Exception while handling an update:", exc_info=context.error)
    # Уведомляем пользователя об ошибке
    if update and hasattr(update, 'message') and update.message:
        await update.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")
    elif update and hasattr(update, 'callback_query') and update.callback_query:
        await update.callback_query.message.reply_text("Произошла ошибка. Пожалуйста, попробуйте позже.")