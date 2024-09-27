# utils/localization.py
from telegram.ext import ContextTypes
import logging

logger = logging.getLogger(__name__)

texts = {
    'welcome': {
        'en': "Hello, {0}! I'm your assistant at the B.N. Yeltsin Museum. "
              "How can I help you?",
        'ru': "Привет, {0}! Я твой ассистент по музею Б.Н. Ельцина. "
              "Чем могу помочь?"
    },
    'choose_language': {
        'en': "Please choose your language:",
        'ru': "Пожалуйста, выберите язык:"
    },
    'language_changed': {
        'en': "Language changed successfully!",
        'ru': "Язык успешно изменён!"
    },
    'info_museum': {
        'en': "🕖 Museum Information",
        'ru': "🕖 Информация о музее"
    },
    'interactive_quests': {
        'en': "🎮 Interactive Quests",
        'ru': "🎮 Интерактивные квесты"
    },
    'nearby_places': {
        'en': "📍 Nearby Places",
        'ru': "📍 Достопримечательности рядом"
    },
    'settings': {
        'en': "⚙️ Settings",
        'ru': "⚙️ Настройки"
    },
    'museum_info': {
        'en': "🏛 **B.N. Yeltsin Museum**\n\n🕒 Opening hours: 10:00 to 20:00 daily."
              "\n💰 Ticket prices:\n - Adult: 300 rubles\n - Student: 200 rubles"
              "\n - Schoolchild: 150 rubles\n\n📍 Address: Yekaterinburg, "
              "Boris Yeltsin St., 3.",
        'ru': "🏛 **Музей Б.Н. Ельцина**\n\n🕒 Часы работы: с 10:00 до 20:00 "
              "ежедневно.\n💰 Стоимость билета:\n - Взрослый: 300 рублей\n - "
              "Студенческий: 200 рублей\n - Школьный: 150 рублей\n\n📍 Адрес: "
              "г. Екатеринбург, ул. Бориса Ельцина, 3."
    },
    'show_map': {
        'en': "🗺 Show Map",
        'ru': "🗺 Показать карту"
    },
    'back': {
        'en': "🔙 Back",
        'ru': "🔙 Назад"
    },
    'museum_map_caption': {
        'en': "🗺 Museum Map",
        'ru': "🗺 Карта музея"
    },
    'map_unavailable': {
        'en': "Sorry, the map is temporarily unavailable.",
        'ru': "Извините, карта временно недоступна."
    },
    'use_map_instruction': {
        'en': "Use the map to navigate through the museum halls.",
        'ru': "Используйте карту для навигации по залам музея."
    },
    'choose_quest_text': {
        'en': "Choose the quest you want to play:",
        'ru': "Выберите квест, который хотите пройти:"
    },
    'historical_quest': {
        'en': "🏛 Historical Quest",
        'ru': "🏛 Исторический квест"
    },
    'technical_quest': {
        'en': "🔬 Technical Quest",
        'ru': "🔬 Технический квест"
    },
    'entertainment_quest': {
        'en': "🎨 Entertainment Quest",
        'ru': "🎨 Развлекательный квест"
    },
    'quest_intro': {
        'en': "🎮 *{quest_type} Quest*\n\nTask 1: Find the 'Origins' hall and "
              "send me a photo of the exhibit you like the most.",
        'ru': "🎮 *{quest_type} квест*\n\nЗадание 1: Найдите зал 'Истоки' и "
              "отправьте мне фото экспоната, который вам больше всего "
              "понравился."
    },
    'historical_quest_step2': {
        'en': "Task 2: What significant event happened in 1985?",
        'ru': "Задание 2: Какое важное событие произошло в 1985 году?"
    },
    'technical_quest_step2': {
        'en': "Task 2: What is the approximate value of Pi?",
        'ru': "Задание 2: Какое приблизительное значение числа Пи?"
    },
    'entertainment_quest_step2': {
        'en': "Task 2: Name a famous painting by Leonardo da Vinci.",
        'ru': "Задание 2: Назовите известную картину Леонардо да Винчи."
    },
    'quest_final_step': {
        'en': "Final task: Send me the code word you will find in the last hall.",
        'ru': "Финальное задание: Отправьте мне кодовое слово, которое вы "
              "найдёте в последнем зале."
    },
    'hint': {
        'en': "💡 Hint",
        'ru': "💡 Подсказка"
    },
    'exit_quest': {
        'en': "❌ Exit Quest",
        'ru': "❌ Выйти из квеста"
    },
    'quest_photo_received': {
        'en': "Great photo! Let's move on to the next task.",
        'ru': "Отличное фото! Переходим к следующему заданию."
    },
    'correct_answer_next': {
        'en': "Correct! Moving on to the next task.",
        'ru': "Верно! Переходим к следующему заданию."
    },
    'incorrect_answer_try_again': {
        'en': "Incorrect answer. Please try again.",
        'ru': "Неправильный ответ. Попробуйте ещё раз."
    },
    'quest_completed': {
        'en': "Congratulations! You have successfully completed the quest and "
              "receive a virtual reward! 🏆",
        'ru': "Поздравляем! Вы успешно прошли квест и получаете виртуальную "
              "награду! 🏆"
    },
    'please_use_menu': {
        'en': "Please use the bot's menu.",
        'ru': "Пожалуйста, используйте меню бота."
    },
    'no_hint_available': {
        'en': "No hint available.",
        'ru': "Подсказка недоступна."
    },
    'quest_exited': {
        'en': "You have exited the quest. Returning to the main menu.",
        'ru': "Вы вышли из квеста. Возвращаюсь в главное меню."
    },
    'nearby_places_text': {
        'en': "📍 *Nearby Places:*\n\n1. Church on the Blood - 500 m\n2. "
              "Plotinka - 1 km\n3. Historical Square - 1.2 km\n\nSelect a place "
              "to get a route:",
        'ru': "📍 *Достопримечательности рядом:*\n\n1. Храм-на-Крови - 500 м\n2. "
              "Плотинка - 1 км\n3. Исторический сквер - 1.2 км\n\nВыберите место, "
              "чтобы получить маршрут:"
    },
    'place_temple': {
        'en': "🗺 Church on the Blood",
        'ru': "🗺 Храм-на-Крови"
    },
    'place_pond': {
        'en': "🗺 Plotinka",
        'ru': "🗺 Плотинка"
    },
    'place_square': {
        'en': "🗺 Historical Square",
        'ru': "🗺 Исторический сквер"
    },
    'route_to': {
        'en': "Route to {0}",
        'ru': "Маршрут до {0}"
    },
    'route_unavailable': {
        'en': "Sorry, the route is temporarily unavailable.",
        'ru': "Извините, не удалось построить маршрут."
    },
    'unknown_place': {
        'en': "Unknown place.",
        'ru': "Неизвестное место."
    },
    'settings_text': {
        'en': "⚙️ *Settings*\n\nYou can set your interests to receive "
              "personalized information.",
        'ru': "⚙️ *Настройки*\n\nВы можете настроить свои интересы для получения "
              "персонализированной информации."
    },
    'change_interests': {
        'en': "✏️ Change Interests",
        'ru': "✏️ Изменить интересы"
    },
    'manage_notifications': {
        'en': "🔔 Manage Notifications",
        'ru': "🔔 Управление уведомлениями"
    },
    'notifications_unavailable': {
        'en': "Notification management is currently unavailable.",
        'ru': "Управление уведомлениями пока недоступно."
    },
    'enter_interests': {
        'en': "Please enter your interests separated by commas:",
        'ru': "Пожалуйста, введите ваши интересы через запятую:"
    },
    'interests_saved': {
        'en': "Your interests have been updated!",
        'ru': "Ваши интересы обновлены!"
    },
    'unknown_command': {
        'en': "Sorry, I didn't understand your request.",
        'ru': "Извините, я не понял ваш запрос."
    },
    'stats_text': {
        'en': "📊 Bot Usage Statistics:\n\nTotal users: {total_users}\nTotal "
              "messages: {total_messages}",
        'ru': "📊 Статистика использования бота:\n\nВсего пользователей: "
              "{total_users}\nКоличество сообщений: {total_messages}"
    },
    'admin_panel_text': {
        'en': "Welcome to the admin panel. Choose an action:",
        'ru': "Добро пожаловать в админ-панель. Выберите действие:"
    },
    'broadcast_message': {
        'en': "📢 Broadcast Message",
        'ru': "📢 Рассылка сообщения"
    },
    'view_stats': {
        'en': "📈 View Statistics",
        'ru': "📈 Просмотр статистики"
    },
    'enter_broadcast_message': {
        'en': "Please enter the message to broadcast:",
        'ru': "Пожалуйста, введите сообщение для рассылки:"
    },
    'broadcast_completed': {
        'en': "Broadcast completed successfully. Message sent to {count} users.",
        'ru': "Рассылка успешно завершена. Сообщение отправлено {count} пользователям."
    },
    'change_language': {
        'en': "🌐 Change Language",
        'ru': "🌐 Сменить язык"
    },
    'admin_panel': {
        'en': "🛠 Admin Panel",
        'ru': "🛠 Админ-панель"
    },
    # Добавленные тексты для квестов и подсказок
    'historical_hint1': {
        'en': "Hint: The 'Origins' hall is on the first floor.",
        'ru': "Подсказка: Зал 'Истоки' находится на первом этаже."
    },
    'historical_hint2': {
        'en': "Hint: It was the beginning of major reforms in the USSR.",
        'ru': "Подсказка: Это было начало крупных реформ в СССР."
    },
    'historical_hint3': {
        'en': "Hint: The code word is 'Democracy'.",
        'ru': "Подсказка: Кодовое слово - 'Демократия'."
    },
    'technical_hint1': {
        'en': "Hint: You need to find the 'Innovations' hall.",
        'ru': "Подсказка: Вам нужно найти зал 'Инновации'."
    },
    'technical_hint2': {
        'en': "Hint: It's approximately 3.14.",
        'ru': "Подсказка: Это приблизительно 3.14."
    },
    'technical_hint3': {
        'en': "Hint: The code word is 'Technology'.",
        'ru': "Подсказка: Кодовое слово - 'Технология'."
    },
    'entertainment_hint1': {
        'en': "Hint: Look for the 'Art' hall.",
        'ru': "Подсказка: Ищите зал 'Искусство'."
    },
    'entertainment_hint2': {
        'en': "Hint: The painting features a woman with a mysterious smile.",
        'ru': "Подсказка: На картине изображена женщина с загадочной улыбкой."
    },
    'entertainment_hint3': {
        'en': "Hint: The code word is 'Art'.",
        'ru': "Подсказка: Кодовое слово - 'Искусство'."
    },
    'historical_quest_name': {
        'en': "Historical",
        'ru': "Исторический"
    },
    'technical_quest_name': {
        'en': "Technical",
        'ru': "Технический"
    },
    'entertainment_quest_name': {
        'en': "Entertainment",
        'ru': "Развлекательный"
    },
    # Добавьте другие текстовые строки и переводы по необходимости
}

def get_text(key, context: ContextTypes.DEFAULT_TYPE):
    lang = context.user_data.get('language', 'en')
    text = texts.get(key, {}).get(lang)
    if text is None:
        logger.warning(f"Missing localization for key '{key}' and language '{lang}'")
        return f"[{key}]"
    return text

def set_user_language(context: ContextTypes.DEFAULT_TYPE, language):
    context.user_data['language'] = language