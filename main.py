import asyncio
import json
from datetime import datetime
from pyrogram import Client, filters, enums
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from pymongo import MongoClient
import aiohttp
import phonenumbers

# ================= CONFIGURATION =================
API_ID = 30954859
API_HASH = "240537c89299fc2c94e8c78607229a21"
BOT_TOKEN = "8841502557:AAH7m1ezXQbK8DKHsGuY6T7H2IMPtRAeVq8"

GROUP_ID = -1002949251809
CHANNEL_ID = "@gmtusharxfiles"
OTP_GROUP_LINK = "https://t.me/trxxotp"

BOT_NAME = "𝗚𝗠𝘅𝗢𝗧𝗣"
ADMIN_IDS = [8430946490]
OWNER_USERNAME = "@Amarstarx"

# ================= DATABASE =================
MONGO_URI = "mongodb://tusharkumarin74_db_user:star%40123@ac-zborjum-shard-00-00.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-01.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-02.7jv0uuq.mongodb.net:27017/?ssl=true&replicaSet=atlas-qnvkfj-shard-0&authSource=admin&appName=Cluster"

try:
    db_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = db_client.numberx
    print("✅ Connected to MongoDB Successfully")
except Exception as err:
    print(f"❌ MongoDB Connection Failed: {err}")

# ================= PYROGRAM CLIENT =================
app = Client(
    "numberx_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=10,
    workers=50
)

# ================= ALL EMOJI IDs MAPPING =================
DEFAULT_EMOJIS = {
    # Service Emojis
    "whatsapp": "5264943818230214577",
    "facebook": "5454340696183943190",
    "telegram": "5454340696183943190",
    "instagram": "5264943818230214577",
    "tiktok": "5454351124364542651",
    
    # UI Control Icons
    "copy": "6053074925546118479",
    "refresh": "6053387526150823179",
    "close": "6052869226677410910",
    "arrow_right": "6246586201780786421",
    "verify_red": "6233392109492114295",
    "verify_blue": "6233232736140663096",
    "otp_group": "6052921672523061549",
    "fire": "6053163053980063912",
    "star": "6053229398339884957",
    "crown": "6338946058982267602",
    
    # Red Letter Alphabets
    "red_a": "6089331338651898690",
    "red_b": "6089185073540633441",
    "red_c": "6089243850168079288",
    "red_g": "6089328581282893987",
    "red_m": "6086808577941442721",
    "red_o": "6089038537846428469",
    "red_p": "6089086272112956355",
    "red_r": "6089093113995859575",
    "red_s": "6087009900238475312",
    "red_t": "6089331338651898690",
    "red_w": "6089093113995859575",
    "red_x": "6089086272112956355"
}

# Country Flag Telegram Custom Emoji IDs
COUNTRY_FLAG_EMOJIS = {
    "58": "5294476442854247878",   # Venezuela
    "91": "5291933173674957761",   # India
    "1": "5294244076533600593",    # USA / Canada
    "7": "5294335323113807278",    # Russia
    "55": "5291892229751723900",   # Brazil
    "92": "5291825606219029010",   # Pakistan
    "880": "5291824687096027834",  # Bangladesh
    "62": "5292045130587462814",   # Indonesia
    "44": "5293993521026453119",   # UK
}
DEFAULT_FLAG_ID = "5294007002928798927"

def e(key, fallback="✨"):
    """Get Custom Emoji HTML tag dynamically from DB or Defaults."""
    try:
        emoji_doc = db.emojis.find_one({"key": key.lower()})
        emoji_id = emoji_doc["id"] if emoji_doc else DEFAULT_EMOJIS.get(key.lower())
        if emoji_id:
            return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
    except Exception:
        pass
    return fallback

def get_country_flag(number):
    """Detects Country Code & Flag via Specific Emoji IDs & Global Fallback."""
    clean_num = number.replace("+", "").strip()
    
    # Check custom emoji map by calling code
    for code, emoji_id in COUNTRY_FLAG_EMOJIS.items():
        if clean_num.startswith(code):
            return f'<tg-emoji emoji-id="{emoji_id}">🏳️</tg-emoji>'
            
    # Try global ISO detection
    try:
        formatted = f"+{clean_num}"
        parsed = phonenumbers.parse(formatted)
        country_code = phonenumbers.region_code_for_number(parsed)
        if country_code:
            return "".join(chr(127397 + ord(c)) for c in country_code)
    except Exception:
        pass

    return f'<tg-emoji emoji-id="{DEFAULT_FLAG_ID}">🌐</tg-emoji>'

def make_red_title(text):
    """Converts text into Red Alphabet Custom Emojis."""
    result = ""
    for char in text.upper():
        key = f"red_{char.lower()}"
        if key in DEFAULT_EMOJIS:
            result += e(key, char) + " "
        else:
            result += f"<b>{char}</b> "
    return result.strip()

# ================= HELPERS & PANELS =================
user_states = {}

def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_banned(user_id):
    try:
        user = db.users.find_one({"user_id": user_id})
        return user and user.get("is_banned", False)
    except Exception:
        return False

def add_user(user_id, username, first_name):
    try:
        if not db.users.find_one({"user_id": user_id}):
            db.users.insert_one({
                "user_id": user_id,
                "username": username,
                "first_name": first_name,
                "joined_date": datetime.now(),
                "is_banned": False,
                "numbers_allocated": 0
            })
    except Exception as ex:
        print(f"Error adding user: {ex}")

def get_all_services():
    try:
        services_db = [s["name"] for s in db.services.find({}) if s.get("name")]
        return list(set(services_db))
    except Exception:
        return []

PANELS = [
    {
        "name": "KONEK",
        "url": "http://51.77.216.195/crapi/konek/viewstats",
        "otp_url": "http://51.77.216.195/crapi/konek/getotp",
        "token": "RFRXSjRSQmNccJFIWpN1e16XVIdYjGtlSGlphVVRUHpClnlginKV"
    },
    {
        "name": "GM Panel",
        "url": "http://147.135.212.197/crapi/st/viewstats",
        "otp_url": "http://147.135.212.197/crapi/st/getotp",
        "token": "SFBXRkFBUzSIiZZ8Y2FwSlqMb3yGkWOAi2lXW1JojFZbaFddaZRPdQ=="
    }
]

# ================= ALLOCATE NUMBERS =================
async def allocate_three_numbers(user_id, service):
    try:
        async with aiohttp.ClientSession() as session:
            async def fetch_panel(panel):
                try:
                    async with session.get(panel["url"], headers={"Authorization": panel["token"]}, timeout=5) as resp:
                        if resp.status == 200:
                            return await resp.json()
                except Exception:
                    pass
                return None
            
            tasks = [fetch_panel(panel) for panel in PANELS]
            results = await asyncio.gather(*tasks)
            
            for data in results:
                if data and data.get("numbers"):
                    numbers = data.get("numbers", [])
                    for num in numbers[:10]:
                        if not db.numbers.find_one({"number": str(num)}):
                            db.numbers.insert_one({
                                "number": str(num),
                                "status": "available",
                                "assigned_to": None,
                                "service": service
                            })
                    break
    except Exception as ex:
        print(f"Allocation API error: {ex}")
    
    try:
        number_docs = list(db.numbers.find({"status": "available", "service": service}).limit(3))
        if len(number_docs) < 1:
            return None, "Is service ke liye filhal koi numbers available nahi hain."
        
        numbers_list = []
        for doc in number_docs:
            db.numbers.update_one(
                {"_id": doc["_id"]},
                {"$set": {"status": "in_use", "assigned_to": user_id}}
            )
            numbers_list.append(doc["number"])
        
        db.users.update_one({"user_id": user_id}, {"$inc": {"numbers_allocated": len(numbers_list)}})
        return numbers_list, None
    except Exception as ex:
        return None, f"Database Error: {str(ex)}"

# ================= KEYBOARD BUILDERS =================
def build_numbers_inline_keyboard(numbers, service):
    buttons = []
    
    srv_emoji = e(service.lower(), e("verify_blue", "📱"))
    buttons.append([
        InlineKeyboardButton(f"{srv_emoji} {service}", callback_data="noop")
    ])
    
    copy_icon = e("copy", "📄")
    for num in numbers:
        formatted_num = num if num.startswith("+") else f"+{num}"
        flag_icon = get_country_flag(formatted_num)
        btn_text = f"{flag_icon}  {copy_icon}  {formatted_num}"
        buttons.append([
            InlineKeyboardButton(btn_text, callback_data=f"copy_{formatted_num}")
        ])
        
    refresh_icon = e("refresh", "🔄")
    shield_icon = e("otp_group", "🛡️")
    buttons.append([
        InlineKeyboardButton(f"{refresh_icon} Change Number", callback_data=f"change_{service}"),
        InlineKeyboardButton(f"{shield_icon} OTP Group", url=OTP_GROUP_LINK)
    ])
    
    close_icon = e("close", "❌")
    buttons.append([
        InlineKeyboardButton(f"{close_icon} Close", callback_data="close_menu")
    ])
    
    return InlineKeyboardMarkup(buttons)

user_keyboard = ReplyKeyboardMarkup([
    ["📱 Get Number", "🔍 Search Number"],
    ["📊 Traffic Stats", "🆘 Support / Owner"]
], resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup([
    ["➕ Add Service", "➖ Delete Service"],
    ["🎭 Manage Emojis", "📢 Broadcast"],
    ["🔙 Back to Main"]
], resize_keyboard=True)

# ================= BACKGROUND OTP LISTENER LOOP =================
async def background_otp_checker():
    """Background engine fetching OTPs from Panel APIs and forwarding to GROUP_ID."""
    while True:
        try:
            active_numbers = list(db.numbers.find({"status": "in_use"}))
            if active_numbers:
                async with aiohttp.ClientSession() as session:
                    for doc in active_numbers:
                        num = doc["number"]
                        service = doc.get("service", "Service")
                        
                        for panel in PANELS:
                            try:
                                url = f"{panel['otp_url']}?number={num}"
                                async with session.get(url, headers={"Authorization": panel["token"]}, timeout=4) as resp:
                                    if resp.status == 200:
                                        res = await resp.json()
                                        otp = res.get("otp") or res.get("code")
                                        if otp:
                                            flag = get_country_flag(num)
                                            msg = (
                                                f"📩 <b>NEW OTP RECEIVED</b>\n"
                                                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                                                f"<b>Service:</b> {service}\n"
                                                f"<b>Number:</b> {flag} <code>+{num}</code>\n"
                                                f"<b>OTP Code:</b> <code>{otp}</code>\n"
                                                f"━━━━━━━━━━━━━━━━━━━━━━━"
                                            )
                                            await app.send_message(GROUP_ID, msg, parse_mode=enums.ParseMode.HTML)
                                            db.numbers.update_one({"_id": doc["_id"]}, {"$set": {"status": "completed"}})
                            except Exception:
                                pass
        except Exception as ex:
            print(f"OTP Loop Exception: {ex}")
            
        await asyncio.sleep(5)

# ================= BOT COMMAND HANDLERS =================
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    
    add_user(user_id, message.from_user.username or "User", message.from_user.first_name or "User")
    if is_banned(user_id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
    header_title = make_red_title("WELCOME")
    
    await message.reply_text(
        text=(
            f"{e('verify_blue')} <b>{BOT_NAME}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"{header_title} {e('crown')}\n"
            f"Hello <b>{message.from_user.first_name}</b>, select an option below:\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        ),
        parse_mode=enums.ParseMode.HTML,
        reply_markup=keyboard
    )

@app.on_message(filters.regex("^🆘 Support / Owner$") | filters.command("owner"))
async def owner_info(client, message):
    owner_red_name = make_red_title("AMARSTARX")
    
    msg_text = (
        f"{e('crown')} <b>BOT OWNER & DEVELOPER INFO</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Developer:</b> {owner_red_name}\n"
        f"<b>Username:</b> {OWNER_USERNAME}\n"
        f"<b>Channel:</b> {CHANNEL_ID}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await message.reply_text(msg_text, parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.text & filters.private & filters.regex("^🔙 Back to Main$"))
async def back_to_main(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
    
    await message.reply_text(
        text=f"{e('verify_blue')} <b>Main Menu</b>\n━━━━━━━━━━━━━━━━━━━━━━━",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=keyboard
    )

# ================= USER SERVICE FLOW =================
@app.on_message(filters.text & filters.private & filters.regex("^📱 Get Number$"))
async def get_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    
    services = get_all_services()
    if not services:
        await message.reply_text("❌ Currently no services are available. Please ask Admin to add services!")
        return
        
    service_buttons = [[s] for s in services]
    service_buttons.append(["🔙 Back to Main"])
    user_states[user_id] = {"action": "select_service"}
    
    await message.reply_text(
        text=f"{e('fire')} <b>SELECT SERVICE BELOW:</b>",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True)
    )

# ================= ADMIN ACTIONS =================
@app.on_message(filters.text & filters.private & filters.regex("^➕ Add Service$"))
async def add_service_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "add_service_name"}
    await message.reply_text("✏️ Enter new Service Name (e.g. WhatsApp, Instagram, Telegram):")

@app.on_message(filters.text & filters.private & filters.regex("^➖ Delete Service$"))
async def delete_service_cmd(client, message):
    if not is_admin(message.from_user.id): return
    services = get_all_services()
    if not services:
        await message.reply_text("❌ No services to delete.")
        return
    user_states[message.from_user.id] = {"action": "delete_service_name"}
    await message.reply_text(f"🗑️ Send exact Service Name to delete:\nExisting: {', '.join(services)}")

@app.on_message(filters.text & filters.private & filters.regex("^🎭 Manage Emojis$"))
async def manage_emojis_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "update_emoji_key"}
    await message.reply_text(
        text=(
            f"{e('crown')} <b>EMOJI MANAGER</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Enter Emoji Key Name (e.g., <code>whatsapp</code>, <code>copy</code>, <code>refresh</code>, <code>close</code>):"
        ),
        parse_mode=enums.ParseMode.HTML
    )

# ================= CALLBACK QUERY =================
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    try:
        data = query.data
        user_id = query.from_user.id
        
        if data == "noop":
            await query.answer()
            
        elif data.startswith("copy_"):
            num = data.replace("copy_", "")
            await query.answer(f"Copied Number: {num}", show_alert=True)
            
        elif data.startswith("change_"):
            service = data.replace("change_", "")
            await query.answer("Fetching new numbers...")
            
            numbers, error = await allocate_three_numbers(user_id, service)
            if error:
                await query.message.edit_text(f"❌ {error}", parse_mode=enums.ParseMode.HTML)
                return
                
            await query.message.edit_reply_markup(reply_markup=build_numbers_inline_keyboard(numbers, service))
            
        elif data == "close_menu":
            await query.answer()
            await query.message.delete()
    except Exception as ex:
        print(f"Callback Query Error: {ex}")

# ================= STATE PROCESSOR =================
@app.on_message(filters.private & ~filters.command("start"))
async def central_state_handler(client, message):
    try:
        user_id = message.from_user.id
        text = message.text.strip() if message.text else ""

        if user_id not in user_states: return

        state = user_states[user_id]
        action = state.get("action")

        if action == "add_service_name" and is_admin(user_id):
            user_states.pop(user_id, None)
            db.services.update_one({"name": text}, {"$set": {"name": text}}, upsert=True)
            await message.reply_text(f"✅ Service <b>{text}</b> added successfully!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "delete_service_name" and is_admin(user_id):
            user_states.pop(user_id, None)
            db.services.delete_one({"name": text})
            await message.reply_text(f"🗑️ Service <b>{text}</b> removed!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "update_emoji_key" and is_admin(user_id):
            user_states[user_id] = {"action": "update_emoji_id", "key": text.lower()}
            await message.reply_text(f"Key <code>{text.lower()}</code> selected.\nSend Custom Emoji ID:", parse_mode=enums.ParseMode.HTML)

        elif action == "update_emoji_id" and is_admin(user_id):
            key = state.get("key")
            user_states.pop(user_id, None)
            db.emojis.update_one({"key": key}, {"$set": {"id": text}}, upsert=True)
            await message.reply_text(
                text=f"🎉 Emoji for <code>{key}</code> updated successfully!",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=admin_keyboard
            )

        elif action == "select_service":
            user_states.pop(user_id, None)
            if text == "🔙 Back to Main":
                await back_to_main(client, message)
                return
            
            numbers, error = await allocate_three_numbers(user_id, text)
            if error:
                await message.reply_text(f"❌ {error}", reply_markup=user_keyboard)
                return
                
            inline_kb = build_numbers_inline_keyboard(numbers, text)
            await message.reply_text(
                text=f"{e('verify_red')} Here are your requested numbers:",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=inline_kb
            )
    except Exception as ex:
        print(f"State Handler Error: {ex}")

# ================= ENGINE INITIALIZATION =================
async def main():
    await app.start()
    print(f"🚀 {BOT_NAME} Engine Started Successfully!")
    asyncio.create_task(background_otp_checker())
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
