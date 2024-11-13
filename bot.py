import datetime
import json
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes


async def save_user_data(user_id, username, name, text):
    data_file = "users.json"
    try:
        # Load existing data
        with open(data_file, "r") as file:
            users_data = json.load(file)
    except FileNotFoundError:
        # If file doesn't exist, initialize an empty dictionary
        users_data = {}

    # Prepare the current time and new data entry
    time = datetime.datetime.now().strftime("%c")
    new_entry = {
        "username": username,
        "name": name,
        "time": time,
        "text": text,
    }

    # Append the new entry under the user's ID (as a list of records per user)
    if str(user_id) not in users_data:
        users_data[str(user_id)] = []
    users_data[str(user_id)].append(new_entry)

    # Save the updated data back to the file
    with open(data_file, "w") as file:
        json.dump(users_data, file, indent=4)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user

    buttons = [
        ["ID", "Name"],
        ["Username", "About"],
    ]
    reply_markup = ReplyKeyboardMarkup(buttons, one_time_keyboard=False, resize_keyboard=True)
    await update.message.reply_text("Welcome", reply_markup=reply_markup)

async def about(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Bu bot foydalanuvchi haqida ma'lumot beradi va turli xil funksiyalarni bajaradi.")

async def user_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    await update.message.reply_text(f"Sizning ID: {user_id}")

async def name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    first_name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name or ""
    await update.message.reply_text(f"Sizning ism: {first_name} {last_name}".strip())

async def username(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = update.message.from_user.username
    if username:
        await update.message.reply_text(f"Sizning username: @{username}")
    else:
        await update.message.reply_text("Siz username o'rnatmagansiz.")


async def unknown_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_sticker("https://telegrambots.github.io/book/docs/sticker-fred.webp")


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    await save_user_data(update.effective_user.id, update.effective_user.username, update.effective_user.first_name, text)

    if text == "ID":
        await user_id(update, context)
    elif text == "Name":
        await name(update, context)
    elif text == "Username":
        await username(update, context)
    elif text == "About":
        await about(update, context)
    else:
        await update.message.reply_animation("https://telegrambots.github.io/book/docs/sticker-fred.webp")


def main():
    try:
        TOKEN = "TOKEN HERE"
        application = Application.builder().token(TOKEN).build()
    except Exception as e:
        print(f"Xatooo\n\n{e}")
    else:
        application.add_handler(CommandHandler("start", start))
        application.add_handler(CommandHandler("about", about))
        application.add_handler(MessageHandler(filters.TEXT, button_handler))

        application.run_polling()

if __name__ == "__main__":
    main()
