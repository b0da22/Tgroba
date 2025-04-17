import telebot
from telebot import types

TOKEN = '7742479143:AAHzp86TrQwLngS7BPko2xcWRpmY3HW-cIo'
ADMIN_ID = 6662120440  # استبدل برقم ID الأدمن

bot = telebot.TeleBot(TOKEN)
orders = {}
temp_order = {}

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("➕ إنشاء شحنة", "🚚 تتبع شحنة")
    if message.chat.id == ADMIN_ID:
        markup.add("🛠 لوحة تحكم الأدمن")
    bot.send_message(message.chat.id, "مرحباً بك في نظام شركة الشحن ShahenX!
اختر الخدمة المطلوبة:", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_id = message.chat.id

    if message.text == "➕ إنشاء شحنة":
        bot.send_message(user_id, "من فضلك أرسل رقم الشحنة لتتبعها.")
    elif message.text == "🚚 تتبع شحنة":
        bot.send_message(user_id, "أرسل رقم الشحنة لتتبع حالتها.")
    elif message.text == "🛠 لوحة تحكم الأدمن" and user_id == ADMIN_ID:
        admin_panel(message)
    elif message.text == "📦 إضافة شحنة" and user_id == ADMIN_ID:
        temp_order[user_id] = {}
        bot.send_message(user_id, "الرجاء إدخال اسم العميل:")
        bot.register_next_step_handler(message, get_customer_name)
    else:
        bot.send_message(user_id, "رجاء اختر خيار من القائمة.")

def admin_panel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("📦 إضافة شحنة", "✏️ تحديث حالة شحنة", "❌ حذف شحنة", "📋 عرض كل الشحنات", "⬅️ رجوع")
    bot.send_message(message.chat.id, "لوحة تحكم الأدمن:", reply_markup=markup)

def get_customer_name(message):
    temp_order[message.chat.id]['name'] = message.text
    bot.send_message(message.chat.id, "أدخل رقم الهاتف:")
    bot.register_next_step_handler(message, get_phone_number)

def get_phone_number(message):
    temp_order[message.chat.id]['phone'] = message.text
    bot.send_message(message.chat.id, "أدخل عنوان العميل:")
    bot.register_next_step_handler(message, get_address)

def get_address(message):
    temp_order[message.chat.id]['address'] = message.text
    bot.send_message(message.chat.id, "أدخل رقم تتبع الطلب:")
    bot.register_next_step_handler(message, get_tracking_number)

def get_tracking_number(message):
    temp_order[message.chat.id]['tracking'] = message.text
    order_id = len(orders) + 1
    orders[order_id] = temp_order[message.chat.id]
    bot.send_message(message.chat.id, f"✅ تم حفظ الطلب بنجاح! رقم الطلب هو: {order_id}")

bot.polling()
