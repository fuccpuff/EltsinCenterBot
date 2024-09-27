import logging
from telegram import Update
from telegram.ext import ContextTypes, ConversationHandler
from database import Database
from utils.localization import get_text as _

logger = logging.getLogger(__name__)

class AdminService:
    def __init__(self):
        self.db = Database()

    async def handle_show_stats(self, update_or_query, context: ContextTypes.DEFAULT_TYPE):
        stats = self.db.get_statistics()
        text = _("stats_text", context).format(
            total_users=stats['total_users'],
            total_messages=stats['total_messages']
        )
        if hasattr(update_or_query, 'message') and update_or_query.message:
            await update_or_query.message.reply_text(text)
        else:
            await update_or_query.edit_message_text(text)

    async def handle_broadcast_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        message = update.message.text
        users = self.db.get_all_users()
        success_count = 0
        for user in users:
            try:
                await context.bot.send_message(chat_id=user['user_id'], text=message)
                success_count += 1
            except Exception as e:
                logger.error(f"Failed to send message to {user['user_id']}: {e}")
        await update.message.reply_text(
            _("broadcast_completed", context).format(count=success_count)
        )
        return ConversationHandler.END  # Обязательно завершаем разговор