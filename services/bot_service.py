import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardRemove, CallbackQuery
from telegram.ext import ContextTypes, ConversationHandler
from database import Database
from utils.localization import get_text as _
from utils.maps import get_museum_map, get_route_map
from config import YANDEX_MAPS_API_KEY, ADMIN_USER_ID
from utils.localization import set_user_language
from services.admin_service import AdminService
from constants import ADMIN_BROADCAST, TYPING_REPLY

logger = logging.getLogger(__name__)

admin_service = AdminService()

class BotService:
    def __init__(self):
        self.db = Database()

    async def handle_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user = update.effective_user
        language = self.db.get_user_language(user.id)
        if not language:
            language = update.effective_user.language_code[:2]
            if language not in ['ru', 'en']:
                language = 'en'
            self.db.add_user(user.id, user.first_name, language)
        set_user_language(context, language)
        context.user_data['language'] = language  # Сохраняем язык в user_data
        await self.send_main_menu(update, context)

    async def handle_change_interests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.edit_message_text(
            text=_("enter_interests", context),
            reply_markup=InlineKeyboardMarkup([])
        )
        return TYPING_REPLY  # Возвращаем состояние для ConversationHandler

    async def handle_save_interests(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        interests = update.message.text
        user_id = update.effective_user.id
        self.db.update_user_interests(user_id, interests)
        await update.message.reply_text(
            _("interests_saved", context),
            reply_markup=ReplyKeyboardRemove()
        )
        await self.send_main_menu(update, context)
        return ConversationHandler.END  # Завершаем разговор

    async def handle_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query = update.callback_query
        await query.answer()
        data = query.data

        if data.startswith('lang_'):
            await self.change_language(query, context)
        elif data == 'info_museum':
            await self.send_museum_info(query, context)
        elif data == 'choose_quest':
            await self.choose_quest(query, context)
        elif data.startswith('quest_'):
            await self.start_quest(query, context)
        elif data == 'nearby_places':
            await self.send_nearby_places(query, context)
        elif data == 'settings':
            await self.show_settings(query, context)
        elif data == 'show_map':
            await self.show_map(query, context)
        elif data == 'back_to_menu':
            await self.send_main_menu(query, context)
        elif data == 'manage_notifications':
            await self.manage_notifications(query, context)
        elif data == 'change_language':
            await self.handle_change_language(query, context)
        elif data == 'exit_quest':
            await self.exit_quest(query, context)
        elif data == 'quest_hint':
            await self.provide_hint(query, context)
        elif data.startswith('route_'):
            await self.route_handler(query, context)
        elif data.startswith('admin_'):
            return await self.handle_admin_button(update, context)
        else:
            await query.edit_message_text(text=_("unknown_command", context))

    async def handle_change_language(self, query, context):
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data='lang_ru')],
            [InlineKeyboardButton("🇬🇧 English", callback_data='lang_en')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(_("choose_language", context), reply_markup=reply_markup)

    async def change_language(self, query, context):
        lang_code = query.data.split('_')[1]
        set_user_language(context, lang_code)
        self.db.update_user_language(query.from_user.id, lang_code)
        await query.edit_message_text(_("language_changed", context))
        await self.send_main_menu(query, context)

    async def send_main_menu(self, update_or_query, context):
        if isinstance(update_or_query, Update):
            user = update_or_query.effective_user
        elif isinstance(update_or_query, CallbackQuery):
            user = update_or_query.from_user
        else:
            user = None

        text = _("welcome", context).format(user.first_name if user else "Guest")
        keyboard = [
            [InlineKeyboardButton(_("info_museum", context), callback_data='info_museum')],
            [InlineKeyboardButton(_("interactive_quests", context), callback_data='choose_quest')],
            [InlineKeyboardButton(_("nearby_places", context), callback_data='nearby_places')],
            [InlineKeyboardButton(_("settings", context), callback_data='settings')],
        ]
        # Добавляем кнопку "Админ-панель" для администратора
        if user and user.id == ADMIN_USER_ID:
            keyboard.append([InlineKeyboardButton(_("admin_panel", context), callback_data='admin_panel')])

        reply_markup = InlineKeyboardMarkup(keyboard)
        text = _("welcome", context).format(user.first_name if user else "Guest")

        if isinstance(update_or_query, CallbackQuery):
            await update_or_query.edit_message_text(text, reply_markup=reply_markup)
        elif hasattr(update_or_query, 'message') and update_or_query.message:
            await update_or_query.message.reply_text(text, reply_markup=reply_markup)
        else:
            logger.warning("send_main_menu received unknown update type")

    async def send_museum_info(self, query, context):
        info_text = _("museum_info", context)
        keyboard = [
            [InlineKeyboardButton(_("show_map", context), callback_data='show_map')],
            [InlineKeyboardButton(_("back", context), callback_data='back_to_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=info_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def show_map(self, query, context):
        map_image = get_museum_map()
        if map_image:
            await query.message.reply_photo(
                photo=map_image,
                caption=_("museum_map_caption", context)
            )
        else:
            await query.message.reply_text(_("map_unavailable", context))
        await query.message.reply_text(_("use_map_instruction", context))

    async def choose_quest(self, query, context):
        text = _("choose_quest_text", context)
        keyboard = [
            [InlineKeyboardButton(_("historical_quest", context), callback_data='quest_historical')],
            [InlineKeyboardButton(_("technical_quest", context), callback_data='quest_technical')],
            [InlineKeyboardButton(_("entertainment_quest", context), callback_data='quest_entertainment')],
            [InlineKeyboardButton(_("back", context), callback_data='back_to_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(text=text, reply_markup=reply_markup)

    async def start_quest(self, query, context):
        quest_type = query.data.split('_')[1]
        context.user_data['quest_type'] = quest_type
        context.user_data['quest_step'] = 1

        # Получаем локализованное название квеста
        quest_type_localized = _("{}_quest_name".format(quest_type), context)

        quest_text = _("quest_intro", context).format(quest_type=quest_type_localized)
        keyboard = [
            [InlineKeyboardButton(_("hint", context), callback_data='quest_hint')],
            [InlineKeyboardButton(_("exit_quest", context), callback_data='exit_quest')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=quest_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def handle_quest_photos(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.user_data
        quest_type = user_data.get('quest_type')
        quest_step = user_data.get('quest_step')

        if quest_type and quest_step == 1:
            await update.message.reply_text(_("quest_photo_received", context))
            user_data['quest_step'] = 2
            await self.send_next_quest_step(update, context)
        else:
            await update.message.reply_text(_("please_use_menu", context))

    async def handle_quest_text(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        user_data = context.user_data
        quest_type = user_data.get('quest_type')
        quest_step = user_data.get('quest_step')
        answer = update.message.text.strip().lower()

        if quest_type and quest_step:
            correct = self.check_quest_answer(quest_type, quest_step, answer)
            if correct:
                if quest_step < 3:
                    await update.message.reply_text(_("correct_answer_next", context))
                    user_data['quest_step'] += 1
                    await self.send_next_quest_step(update, context)
                else:
                    await update.message.reply_text(_("quest_completed", context))
                    # Сохраняем язык перед очисткой данных
                    language = context.user_data.get('language')
                    context.user_data.clear()
                    context.user_data['language'] = language
                    await self.send_main_menu(update, context)
            else:
                await update.message.reply_text(_("incorrect_answer_try_again", context))
        else:
            await update.message.reply_text(_("please_use_menu", context))

    def check_quest_answer(self, quest_type, quest_step, answer):
        correct_answers = {
            'historical': {
                2: '1985',
                3: 'демократия'
            },
            'technical': {
                2: '3.14',
                3: 'технология'
            },
            'entertainment': {
                2: 'мона лиза',
                3: 'искусство'
            }
        }
        return answer == correct_answers.get(quest_type, {}).get(quest_step, '').lower()

    async def send_next_quest_step(self, update: Update, context):
        user_data = context.user_data
        quest_type = user_data.get('quest_type')
        quest_step = user_data.get('quest_step')

        quest_texts = {
            'historical': {
                2: _("historical_quest_step2", context),
                3: _("quest_final_step", context)
            },
            'technical': {
                2: _("technical_quest_step2", context),
                3: _("quest_final_step", context)
            },
            'entertainment': {
                2: _("entertainment_quest_step2", context),
                3: _("quest_final_step", context)
            }
        }

        quest_text = quest_texts.get(quest_type, {}).get(quest_step, '')
        keyboard = [
            [InlineKeyboardButton(_("hint", context), callback_data='quest_hint')],
            [InlineKeyboardButton(_("exit_quest", context), callback_data='exit_quest')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            text=quest_text,
            reply_markup=reply_markup
        )

    async def provide_hint(self, query, context):
        quest_type = context.user_data.get('quest_type')
        quest_step = context.user_data.get('quest_step')

        hints = {
            'historical': {
                1: _("historical_hint1", context),
                2: _("historical_hint2", context),
                3: _("historical_hint3", context)
            },
            'technical': {
                1: _("technical_hint1", context),
                2: _("technical_hint2", context),
                3: _("technical_hint3", context)
            },
            'entertainment': {
                1: _("entertainment_hint1", context),
                2: _("entertainment_hint2", context),
                3: _("entertainment_hint3", context)
            }
        }

        hint = hints.get(quest_type, {}).get(quest_step, _("no_hint_available", context))
        await query.answer(text=hint, show_alert=True)

    async def exit_quest(self, query, context):
        # Сохраняем язык пользователя
        language = context.user_data.get('language')
        # Очищаем данные, кроме языка
        context.user_data.clear()
        context.user_data['language'] = language

        await query.edit_message_text(
            text=_("quest_exited", context)
        )
        await self.send_main_menu(query, context)

    async def send_nearby_places(self, query, context):
        places_text = _("nearby_places_text", context)
        keyboard = [
            [InlineKeyboardButton(_("place_temple", context), callback_data='route_temple')],
            [InlineKeyboardButton(_("place_pond", context), callback_data='route_pond')],
            [InlineKeyboardButton(_("place_square", context), callback_data='route_square')],
            [InlineKeyboardButton(_("back", context), callback_data='back_to_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=places_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def route_handler(self, query, context):
        data = query.data
        place_mapping = {
            'route_temple': 'Храм-на-Крови',
            'route_pond': 'Плотинка',
            'route_square': 'Исторический сквер'
        }
        place = place_mapping.get(data)
        if place:
            map_image = get_route_map(place)
            if map_image:
                await query.message.reply_photo(
                    photo=map_image,
                    caption=_("route_to", context).format(place)
                )
            else:
                await query.message.reply_text(_("route_unavailable", context))
        else:
            await query.message.reply_text(_("unknown_place", context))

    async def show_settings(self, query, context):
        settings_text = _("settings_text", context)
        keyboard = [
            [InlineKeyboardButton(_("change_language", context), callback_data='change_language')],
            [InlineKeyboardButton(_("change_interests", context), callback_data='change_interests')],
            [InlineKeyboardButton(_("manage_notifications", context), callback_data='manage_notifications')],
            [InlineKeyboardButton(_("back", context), callback_data='back_to_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(
            text=settings_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )

    async def manage_notifications(self, query, context):
        await query.edit_message_text(
            text=_("notifications_unavailable", context),
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(_("back", context), callback_data='back_to_menu')]
            ])
        )

    async def handle_admin_button(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        query: CallbackQuery = update.callback_query
        if query.from_user.id != ADMIN_USER_ID:
            await query.answer("У вас нет прав доступа к этой функции.", show_alert=True)
            return ConversationHandler.END
        data = query.data

        if data == 'admin_panel':
            await self.send_admin_panel(update_or_query=query, context=context)
            return ConversationHandler.END
        elif data == 'admin_broadcast':
            await query.edit_message_text(_("enter_broadcast_message", context))
            return ADMIN_BROADCAST
        elif data == 'admin_view_stats':
            await admin_service.handle_show_stats(update_or_query=query, context=context)
            return ConversationHandler.END

    async def send_admin_panel(self, update_or_query, context):
        keyboard = [
            [InlineKeyboardButton(_("broadcast_message", context), callback_data='admin_broadcast')],
            [InlineKeyboardButton(_("view_stats", context), callback_data='admin_view_stats')],
            [InlineKeyboardButton(_("back", context), callback_data='back_to_menu')],
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        text = _("admin_panel_text", context)

        if isinstance(update_or_query, CallbackQuery):
            await update_or_query.edit_message_text(text, reply_markup=reply_markup)
        elif hasattr(update_or_query, 'message') and update_or_query.message:
            await update_or_query.message.reply_text(text, reply_markup=reply_markup)
        else:
            logger.warning("send_admin_panel received unknown update type")