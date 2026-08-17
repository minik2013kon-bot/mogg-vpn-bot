import asyncio
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F, types
from aiogram.filters import Command, CommandStart
from aiogram.types import (
    InlineKeyboardMarkup, InlineKeyboardButton,
    ReplyKeyboardMarkup, KeyboardButton,
    Message, CallbackQuery
)
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import database as db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", 0))

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# ══════════════════════════════════
# СОСТОЯНИЯ
# ══════════════════════════════════
class Form(StatesGroup):
    waiting_photo = State()

# ══════════════════════════════════
# КЛАВИАТУРЫ
# ══════════════════════════════════
def main_menu():
    kb = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="💎 ТАРИФЫ"), KeyboardButton(text="👤 МОЙ АККАУНТ")],
            [KeyboardButton(text="👑 MOGGERS RATING")],
            [KeyboardButton(text="🎁 РЕФЕРАЛЫ"), KeyboardButton(text="💬 ПОДДЕРЖКА")],
            [KeyboardButton(text="ℹ️ О СЕРВИСЕ")]
        ],
        resize_keyboard=True
    )
    return kb

def tariffs_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🥉 БАЗОВЫЙ — 249₽", callback_data="buy_basic")],
        [InlineKeyboardButton(text="🥈 ПРО — 449₽", callback_data="buy_pro")],
        [InlineKeyboardButton(text="🥇 MOGGER 👑 — 799₽", callback_data="buy_mogger")],
    ])
    return kb

def payment_menu(tariff):
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="💳 Карта РФ", callback_data=f"pay_card_{tariff}")],
        [InlineKeyboardButton(text="₿ Крипта", callback_data=f"pay_crypto_{tariff}")],
        [InlineKeyboardButton(text="⭐ Telegram Stars", callback_data=f"pay_stars_{tariff}")],
        [InlineKeyboardButton(text="← Назад", callback_data="back_tariffs")],
    ])
    return kb

def rating_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="😬 SUB3", callback_data="rate_sub3"),
            InlineKeyboardButton(text="😐 SUB5", callback_data="rate_sub5"),
        ],
        [
            InlineKeyboardButton(text="🙂 LTN", callback_data="rate_ltn"),
            InlineKeyboardButton(text="😎 MTN", callback_data="rate_mtn"),
        ],
        [
            InlineKeyboardButton(text="🔥 HTN", callback_data="rate_htn"),
            InlineKeyboardButton(text="💪 CHAD", callback_data="rate_chad"),
        ],
        [
            InlineKeyboardButton(text="👑 TRUE ADAM", callback_data="rate_true_adam"),
        ],
        [
            InlineKeyboardButton(text="⏭ Пропустить", callback_data="rate_skip"),
        ],
    ])
    return kb

def moggers_menu():
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📸 ЗАГРУЗИТЬ СВОЁ ФОТО", callback_data="upload_photo")],
        [InlineKeyboardButton(text="⚡ ОЦЕНИВАТЬ ДРУГИХ", callback_data="rate_others")],
        [InlineKeyboardButton(text="📊 МОИ ОЦЕНКИ", callback_data="my_ratings")],
        [InlineKeyboardButton(text="ℹ️ Что за оценки?", callback_data="rating_info")],
    ])
    return kb

# ══════════════════════════════════
# СТАРТ
# ══════════════════════════════════
@dp.message(CommandStart())
async def start_handler(message: Message):
    args = message.text.split()
    referrer_id = None
    if len(args) > 1 and args[1].startswith("ref_"):
        try:
            referrer_id = int(args[1].split("_")[1])
        except:
            pass
    
    await db.add_user(message.from_user.id, message.from_user.username, referrer_id)
    
    text = (
        "👑 <b>Добро пожаловать в MOGG VPN!</b>\n\n"
        "Ты в шаге от того, чтобы стать настоящим MOGGER 🔥\n\n"
        "💎 Что мы предлагаем:\n"
        "├ ⚡ Максимальная скорость\n"
        "├ 🌍 50+ стран мира\n"
        "├ 🔒 Полная анонимность\n"
        "└ 👑 Статус MOGGER\n\n"
        "🎯 <b>Специальная фишка:</b>\n"
        "Оценивай других моггеров и получай оценки от них!\n"
        "Проверь насколько ты близок к TRUE ADAM 👑\n\n"
        "Выбирай что интересно ⬇️"
    )
    
    await message.answer(text, reply_markup=main_menu(), parse_mode="HTML")

# ══════════════════════════════════
# ТАРИФЫ
# ══════════════════════════════════
@dp.message(F.text == "💎 ТАРИФЫ")
async def tariffs_handler(message: Message):
    text = (
        "💎 <b>ВЫБЕРИ СВОЙ УРОВЕНЬ:</b>\n\n"
        "🥉 <b>БАЗОВЫЙ</b> — 249₽/мес\n"
        "├ 1 устройство\n"
        "├ 15 стран\n"
        "├ 50 Мбит/с\n"
        "└ Обход блокировок\n\n"
        "🥈 <b>ПРО</b> — 449₽/мес\n"
        "├ 3 устройства\n"
        "├ 30+ стран\n"
        "├ 200 Мбит/с\n"
        "└ Netflix, ChatGPT\n\n"
        "🥇 <b>MOGGER</b> 👑 — 799₽/мес\n"
        "├ 10 устройств\n"
        "├ 50+ стран\n"
        "├ БЕЗ лимитов скорости\n"
        "├ Приватные серверы\n"
        "├ Статус MOGGER\n"
        "├ Закрытый чат\n"
        "└ VIP поддержка 24/7\n\n"
        "🔥 <b>MOGGER — топ выбор!</b>"
    )
    await message.answer(text, reply_markup=tariffs_menu(), parse_mode="HTML")

# ══════════════════════════════════
# ПОКУПКА
# ══════════════════════════════════
@dp.callback_query(F.data.startswith("buy_"))
async def buy_handler(callback: CallbackQuery):
    tariff = callback.data.split("_")[1]
    tariffs = {
        "basic": ("🥉 БАЗОВЫЙ", "249₽"),
        "pro": ("🥈 ПРО", "449₽"),
        "mogger": ("🥇 MOGGER 👑", "799₽")
    }
    name, price = tariffs[tariff]
    
    text = (
        f"<b>{name}</b> — {price}/мес\n\n"
        f"Выбери способ оплаты 👇"
    )
    await callback.message.edit_text(text, reply_markup=payment_menu(tariff), parse_mode="HTML")

@dp.callback_query(F.data.startswith("pay_"))
async def payment_handler(callback: CallbackQuery):
    parts = callback.data.split("_")
    method = parts[1]
    tariff = parts[2]
    
    text = (
        "⚠️ <b>Оплата пока в разработке</b>\n\n"
        "Скоро подключим:\n"
        "💳 Карты РФ\n"
        "₿ Криптовалюту\n"
        "⭐ Telegram Stars\n\n"
        f"Ты выбрал: <b>{tariff.upper()}</b>\n"
        f"Способ: <b>{method}</b>\n\n"
        "Напиши в поддержку @moggvpn_support для ручной оплаты"
    )
    await callback.message.edit_text(text, parse_mode="HTML")

@dp.callback_query(F.data == "back_tariffs")
async def back_tariffs(callback: CallbackQuery):
    text = "💎 <b>ВЫБЕРИ СВОЙ УРОВЕНЬ:</b>\n\nНажми на тариф ниже ⬇️"
    await callback.message.edit_text(text, reply_markup=tariffs_menu(), parse_mode="HTML")

# ══════════════════════════════════
# МОЙ АККАУНТ
# ══════════════════════════════════
@dp.message(F.text == "👤 МОЙ АККАУНТ")
async def account_handler(message: Message):
    user = await db.get_user(message.from_user.id)
    ratings = await db.get_user_ratings(message.from_user.id)
    
    tariff = user[2] if user and user[2] != 'none' else "нет подписки"
    photo_status = "✅ Загружено" if user and user[4] else "❌ Не загружено"
    
    ratings_text = ""
    if ratings:
        emoji_map = {
            "sub3": "😬 SUB3", "sub5": "😐 SUB5", "ltn": "🙂 LTN",
            "mtn": "😎 MTN", "htn": "🔥 HTN", "chad": "💪 CHAD",
            "true_adam": "👑 TRUE ADAM"
        }
        ratings_text = "\n\n📊 <b>Твои оценки:</b>\n"
        for rating, count in ratings:
            ratings_text += f"{emoji_map.get(rating, rating)}: {count}\n"
    
    text = (
        f"👤 <b>ТВОЙ ПРОФИЛЬ</b>\n\n"
        f"🆔 ID: <code>{message.from_user.id}</code>\n"
        f"👤 Username: @{message.from_user.username or 'не указан'}\n"
        f"💎 Тариф: <b>{tariff}</b>\n"
        f"📸 Фото в рейтинге: {photo_status}"
        f"{ratings_text}"
    )
    
    await message.answer(text, parse_mode="HTML")

# ══════════════════════════════════
# MOGGERS RATING
# ══════════════════════════════════
@dp.message(F.text == "👑 MOGGERS RATING")
async def moggers_handler(message: Message):
    text = (
        "👑 <b>MOGGERS RATING</b>\n\n"
        "🔥 Оценивай других и получай оценки!\n\n"
        "📊 <b>Шкала оценок:</b>\n"
        "😬 SUB3 — ниже среднего\n"
        "😐 SUB5 — среднячок\n"
        "🙂 LTN — Low Tier Normie\n"
        "😎 MTN — Mid Tier Normie\n"
        "🔥 HTN — High Tier Normie\n"
        "💪 CHAD — красавец\n"
        "👑 TRUE ADAM — легенда\n\n"
        "Выбери что делать ⬇️"
    )
    await message.answer(text, reply_markup=moggers_menu(), parse_mode="HTML")

@dp.callback_query(F.data == "upload_photo")
async def upload_photo_handler(callback: CallbackQuery, state: FSMContext):
    text = (
        "📸 <b>Загрузи своё фото</b>\n\n"
        "⚠️ Правила:\n"
        "├ Только твоё лицо\n"
        "├ Хорошее освещение\n"
        "├ Без масок и очков\n"
        "└ Одно фото\n\n"
        "Отправь фото следующим сообщением 👇"
    )
    await callback.message.answer(text, parse_mode="HTML")
    await state.set_state(Form.waiting_photo)

@dp.message(Form.waiting_photo, F.photo)
async def save_photo_handler(message: Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await db.save_photo(message.from_user.id, photo_id)
    await state.clear()
    
    text = (
        "✅ <b>Фото загружено!</b>\n\n"
        "Теперь другие моггеры смогут тебя оценить 🔥\n\n"
        "Не забудь оценивать других — тогда и тебя будут оценивать чаще!"
    )
    await message.answer(text, reply_markup=moggers_menu(), parse_mode="HTML")

@dp.message(Form.waiting_photo)
async def wrong_photo(message: Message):
    await message.answer("❌ Отправь именно фото, а не текст!")

@dp.callback_query(F.data == "rate_others")
async def rate_others_handler(callback: CallbackQuery):
    photo_data = await db.get_random_photo(callback.from_user.id)
    
    if not photo_data:
        text = (
            "😔 <b>Пока нет фото для оценки</b>\n\n"
            "Приходи позже когда моггеры загрузят свои фото!\n\n"
            "А пока загрузи своё 📸"
        )
        await callback.message.answer(text, reply_markup=moggers_menu(), parse_mode="HTML")
        return
    
    user_id, username, photo_id = photo_data
    caption = f"👤 Оцени этого MOGGER'а:\n@{username or 'anon'}\n\nВыбери оценку ⬇️"
    
    await callback.message.answer_photo(
        photo=photo_id,
        caption=caption,
        reply_markup=rating_menu()
    )
    # Сохраняем user_id в callback_data через хак
    global current_rating_target
    if not hasattr(rate_others_handler, 'targets'):
        rate_others_handler.targets = {}
    rate_others_handler.targets[callback.from_user.id] = user_id

@dp.callback_query(F.data.startswith("rate_"))
async def rating_handler(callback: CallbackQuery):
    rating = callback.data.replace("rate_", "")
    
    if rating == "skip":
        await callback.message.delete()
        await rate_others_handler(callback)
        return
    
    if not hasattr(rate_others_handler, 'targets') or callback.from_user.id not in rate_others_handler.targets:
        await callback.answer("❌ Ошибка. Начни заново", show_alert=True)
        return
    
    target_id = rate_others_handler.targets[callback.from_user.id]
    success = await db.add_rating(target_id, callback.from_user.id, rating)
    
    if success:
        await callback.answer(f"✅ Оценка засчитана!", show_alert=False)
        # Уведомляем оценённого
        emoji_map = {
            "sub3": "😬 SUB3", "sub5": "😐 SUB5", "ltn": "🙂 LTN",
            "mtn": "😎 MTN", "htn": "🔥 HTN", "chad": "💪 CHAD",
            "true_adam": "👑 TRUE ADAM"
        }
        try:
            await bot.send_message(
                target_id,
                f"🔔 Тебя оценили: <b>{emoji_map.get(rating, rating)}</b>\n\nПосмотри статистику в 👤 МОЙ АККАУНТ",
                parse_mode="HTML"
            )
        except:
            pass
        
        await callback.message.delete()
        # Следующее фото
        await rate_others_handler(callback)
    else:
        await callback.answer("❌ Ты уже оценивал этого моггера", show_alert=True)

@dp.callback_query(F.data == "my_ratings")
async def my_ratings_handler(callback: CallbackQuery):
    ratings = await db.get_user_ratings(callback.from_user.id)
    
    if not ratings:
        text = (
            "📊 <b>У тебя пока нет оценок</b>\n\n"
            "Загрузи фото и жди пока другие оценят!\n\n"
            "💡 Совет: оценивай других чаще — тогда и тебя будут оценивать!"
        )
    else:
        emoji_map = {
            "sub3": "😬 SUB3", "sub5": "😐 SUB5", "ltn": "🙂 LTN",
            "mtn": "😎 MTN", "htn": "🔥 HTN", "chad": "💪 CHAD",
            "true_adam": "👑 TRUE ADAM"
        }
        text = "📊 <b>ТВОИ ОЦЕНКИ:</b>\n\n"
        total = sum(count for _, count in ratings)
        for rating, count in ratings:
            percent = (count / total) * 100
            text += f"{emoji_map.get(rating, rating)}: <b>{count}</b> ({percent:.0f}%)\n"
        text += f"\n📈 <b>Всего оценок:</b> {total}"
    
    await callback.message.answer(text, parse_mode="HTML")

@dp.callback_query(F.data == "rating_info")
async def rating_info(callback: CallbackQuery):
    text = (
        "📊 <b>ШКАЛА ОЦЕНОК MOGGERS:</b>\n\n"
        "😬 <b>SUB3</b> — нужно много работать\n"
        "😐 <b>SUB5</b> — ниже среднего\n"
        "🙂 <b>LTN</b> (Low Tier Normie) — обычный\n"
        "😎 <b>MTN</b> (Mid Tier Normie) — норм\n"
        "🔥 <b>HTN</b> (High Tier Normie) — красавчик\n"
        "💪 <b>CHAD</b> — уже моггаешь!\n"
        "👑 <b>TRUE ADAM</b> — легенда, топ 1%\n\n"
        "🎯 Загрузи фото и узнай свой tier!"
    )
    await callback.message.answer(text, parse_mode="HTML")

# ══════════════════════════════════
# РЕФЕРАЛЫ
# ══════════════════════════════════
@dp.message(F.text == "🎁 РЕФЕРАЛЫ")
async def referrals_handler(message: Message):
    ref_link = f"https://t.me/{(await bot.me()).username}?start=ref_{message.from_user.id}"
    text = (
        "🎁 <b>РЕФЕРАЛЬНАЯ ПРОГРАММА</b>\n\n"
        "Приведи друга → получи <b>30%</b> с каждого его платежа НАВСЕГДА\n\n"
        "💰 <b>Твоя реф. ссылка:</b>\n"
        f"<code>{ref_link}</code>\n\n"
        "📊 Приглашено: <b>0 человек</b>\n"
        "💵 Заработано: <b>0₽</b>\n\n"
        "💸 Вывод от 500₽ (карта/крипта/stars)"
    )
    await message.answer(text, parse_mode="HTML")

# ══════════════════════════════════
# ПОДДЕРЖКА
# ══════════════════════════════════
@dp.message(F.text == "💬 ПОДДЕРЖКА")
async def support_handler(message: Message):
    text = (
        "💬 <b>ПОДДЕРЖКА MOGG VPN</b>\n\n"
        "Напиши нам:\n"
        "👉 @moggvpn_support\n\n"
        "⏰ Отвечаем в течение 1-2 часов\n\n"
        "📋 <b>Частые вопросы:</b>\n"
        "• Как подключить VPN? → инструкция придёт после покупки\n"
        "• Оплата не прошла? → напиши в поддержку\n"
        "• Хочу вернуть деньги? → до 3 дней при проблемах"
    )
    await message.answer(text, parse_mode="HTML")

# ══════════════════════════════════
# О СЕРВИСЕ
# ══════════════════════════════════
@dp.message(F.text == "ℹ️ О СЕРВИСЕ")
async def about_handler(message: Message):
    users_count = await db.count_users()
    text = (
        "👑 <b>MOGG VPN</b>\n\n"
        "VPN для настоящих MOGGERS 🔥\n\n"
        "⚡ Максимальная скорость\n"
        "🌍 50+ стран мира\n"
        "🔒 Полная анонимность\n"
        "👑 Статус MOGGER\n\n"
        f"👥 Нас уже: <b>{users_count}</b> моггеров\n\n"
        "📢 Канал: @moggvpn_official\n"
        "🎬 TikTok: @moggvpn\n"
        "📸 Instagram: @moggvpn"
    )
    await message.answer(text, parse_mode="HTML")

# ══════════════════════════════════
# ADMIN
# ══════════════════════════════════
@dp.message(Command("admin"))
async def admin_handler(message: Message):
    if message.from_user.id != ADMIN_ID:
        return
    users = await db.count_users()
    text = (
        f"🔧 <b>АДМИН ПАНЕЛЬ</b>\n\n"
        f"👥 Всего юзеров: {users}\n"
    )
    await message.answer(text, parse_mode="HTML")

# ══════════════════════════════════
# ЗАПУСК
# ══════════════════════════════════
async def main():
    await db.init_db()
    print("🚀 MOGG VPN Bot запущен!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
