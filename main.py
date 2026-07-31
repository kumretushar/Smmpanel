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

# ================= DEFAULT EMOJIS MAPPING =================
DEFAULT_EMOJIS = {
    "red_a": "6089331338651898690",
    "red_b": "6089185073540633441",
    "red_c": "6089243850168079288",
    "red_m": "6086808577941442721",
    "red_r": "6089093113995859575",
    "red_s": "6087009900238475312",
    "red_t": "6089331338651898690",
    "red_x": "6089086272112956355",
    "crown": "6338946058982267602",
    "verify_blue": "6233232736140663096"
}

def e(key, fallback="✨"):
    """Get Custom Emoji HTML tag for Message Body."""
    try:
        emoji_doc = db.emojis.find_one({"key": key.lower()})
        emoji_id = emoji_doc["id"] if emoji_doc else DEFAULT_EMOJIS.get(key.lower())
        if emoji_id:
            return f'<tg-emoji emoji-id="{emoji_id}">{fallback}</tg-emoji>'
    except Exception:
        pass
    return fallback

def get_country_flag_unicode(number):
    """Detects Country Code & Returns Flag."""
    clean_num = str(number).replace("+", "").strip()
    try:
        formatted = f"+{clean_num}"
        parsed = phonenumbers.parse(formatted)
        country_code = phonenumbers.region_code_for_number(parsed)
        if country_code:
            return "".join(chr(127397 + ord(c)) for c in country_code)
    except Exception:
        pass
    return "🌐"

def mask_number_for_group(number):
    """Masks phone number into +91xxxx10 format for OTP Group."""
    clean_num = str(number).replace("+", "").strip()
    if len(clean_num) > 4:
        cc = clean_num[:2]
        last = clean_num[-2:]
        return f"+{cc}xxxx{last}"
    return f"+{clean_num}"

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

# ================= KEYBOARD BUILDERS =================
def get_main_keyboard(user_id):
    buttons = [
        ["📱 Get Number", "🔍 Search Number"],
        ["📊 Traffic Stats", "🆘 Support / Owner"]
    ]
    if is_admin(user_id):
        buttons.append(["⚙️ Admin Panel"])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup([
    ["➕ Add Service", "➖ Delete Service"],
    ["➕ Add Number", "➖ Remove Number"],
    ["🚫 Ban User", "✅ Unban User"],
    ["📈 Special Stats", "📋 Total Users"],
    ["🎭 Manage Emojis", "📢 Broadcast"],
    ["🔙 Back to Main"]
], resize_keyboard=True)

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
                                "service": service,
                                "otp_count": 0
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

# ================= BACKGROUND OTP LISTENER =================
async def background_otp_checker():
    """Background Engine checking OTPs and sending MASKED number to OTP Group."""
    while True:
        try:
            active_numbers = list(db.numbers.find({"status": "in_use"}))
            if active_numbers:
                async with aiohttp.ClientSession() as session:
                    for doc in active_numbers:
                        num = doc["number"]
                        service = doc.get("service", "Service")
                        assigned_user = doc.get("assigned_to", "Unknown")
                        
                        for panel in PANELS:
                            try:
                                url = f"{panel['otp_url']}?number={num}"
                                async with session.get(url, headers={"Authorization": panel["token"]}, timeout=4) as resp:
                                    if resp.status == 200:
                                        res = await resp.json()
                                        otp = res.get("otp") or res.get("code")
                                        if otp:
                                            flag = get_country_flag_unicode(num)
                                            # Group ke liye masked number (+91xxxx88)
                                            masked_num = mask_number_for_group(num)
                                            
                                            msg = (
                                                f"📩 <b>NEW OTP RECEIVED</b>\n"
                                                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                                                f"👤 <b>User ID:</b> <code>{assigned_user}</code>\n"
                                                f"🛠️ <b>Service:</b> {service}\n"
                                                f"📱 <b>Number:</b> {flag} <code>{masked_num}</code>\n"
                                                f"🔑 <b>OTP Code:</b> <code>{otp}</code> (Tap to Copy)\n"
                                                f"━━━━━━━━━━━━━━━━━━━━━━━"
                                            )
                                            await app.send_message(GROUP_ID, msg, parse_mode=enums.ParseMode.HTML)
                                            db.numbers.update_one(
                                                {"_id": doc["_id"]}, 
                                                {
                                                    "$set": {"status": "completed"},
                                                    "$inc": {"otp_count": 1}
                                                }
                                            )
                            except Exception:
                                pass
        except Exception as ex:
            print(f"OTP Loop Exception: {ex}")
            
        await asyncio.sleep(5)

# ================= BOT HANDLERS =================
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    
    add_user(user_id, message.from_user.username or "User", message.from_user.first_name or "User")
    if is_banned(user_id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

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
        reply_markup=get_main_keyboard(user_id)
    )

@app.on_message(filters.text & filters.private & filters.regex("^⚙️ Admin Panel$"))
async def admin_panel_cmd(client, message):
    if not is_admin(message.from_user.id): return
    await message.reply_text(
        "🛠️ <b>Welcome to Admin Panel</b>",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=admin_keyboard
    )

@app.on_message(filters.text & filters.private & filters.regex("^🔙 Back to Main$"))
async def back_to_main(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    await message.reply_text(
        text=f"{e('verify_blue')} <b>Main Menu</b>\n━━━━━━━━━━━━━━━━━━━━━━━",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=get_main_keyboard(user_id)
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

@app.on_message(filters.regex("^📊 Traffic Stats$"))
async def traffic_stats(client, message):
    total_users = db.users.count_documents({})
    total_nums = db.numbers.count_documents({})
    completed = db.numbers.count_documents({"status": "completed"})
    
    top_numbers = list(db.numbers.find({"otp_count": {"$gt": 0}}).sort("otp_count", -1).limit(5))
    top_str = ""
    if top_numbers:
        for idx, doc in enumerate(top_numbers, 1):
            flag = get_country_flag_unicode(doc['number'])
            masked = mask_number_for_group(doc['number'])
            top_str += f"{idx}. {flag} <code>{masked}</code> - <b>{doc.get('otp_count', 0)} OTPs</b>\n"
    else:
        top_str = "No OTP data yet.\n"
    
    msg = (
        f"📊 <b>BOT TRAFFIC STATS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>Total Users:</b> {total_users}\n"
        f"📱 <b>Numbers Processed:</b> {total_nums}\n"
        f"✅ <b>OTPs Delivered:</b> {completed}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔥 <b>TOP OTP RECEIVING NUMBERS:</b>\n"
        f"{top_str}"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await message.reply_text(msg, parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.text & filters.private & filters.regex("^🔍 Search Number$"))
async def search_number_cmd(client, message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    user_states[user_id] = {"action": "search_number"}
    await message.reply_text("🔍 Enter phone number to search (e.g., +919876543210):")

@app.on_message(filters.text & filters.private & filters.regex("^📈 Special Stats$"))
async def special_stats_admin(client, message):
    if not is_admin(message.from_user.id): return
    
    total_users = db.users.count_documents({})
    banned_users = db.users.count_documents({"is_banned": True})
    active_users = total_users - banned_users
    
    total_services = db.services.count_documents({})
    total_nums = db.numbers.count_documents({})
    available_nums = db.numbers.count_documents({"status": "available"})
    in_use_nums = db.numbers.count_documents({"status": "in_use"})
    completed_nums = db.numbers.count_documents({"status": "completed"})
    
    top_users = list(db.users.find({}).sort("numbers_allocated", -1).limit(5))
    user_str = ""
    for idx, u in enumerate(top_users, 1):
        user_str += f"{idx}. <code>{u['user_id']}</code> (@{u.get('username', 'N/A')}) - <b>{u.get('numbers_allocated', 0)} Nums</b>\n"
        
    msg = (
        f"📈 <b>ADMIN SPECIAL ANALYTICS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 <b>Users:</b> Total: {total_users} | Active: {active_users} | Banned: {banned_users}\n"
        f"🛠️ <b>Active Services:</b> {total_services}\n\n"
        f"📱 <b>Numbers Breakdown:</b>\n"
        f"• Total DB Numbers: {total_nums}\n"
        f"• Available: {available_nums}\n"
        f"• In-Use: {in_use_nums}\n"
        f"• Completed (OTPs Received): {completed_nums}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 <b>TOP ACTIVE USERS:</b>\n"
        f"{user_str}"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await message.reply_text(msg, parse_mode=enums.ParseMode.HTML)

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
        text="🔥 <b>SELECT SERVICE BELOW:</b>",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True)
    )

# ================= ADMIN ACTIONS =================
@app.on_message(filters.text & filters.private & filters.regex("^➕ Add Service$"))
async def add_service_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "add_service_name"}
    await message.reply_text("✏️ Enter new Service Name:")

@app.on_message(filters.text & filters.private & filters.regex("^➖ Delete Service$"))
async def delete_service_cmd(client, message):
    if not is_admin(message.from_user.id): return
    services = get_all_services()
    if not services:
        await message.reply_text("❌ No services to delete.")
        return
    user_states[message.from_user.id] = {"action": "delete_service_name"}
    await message.reply_text(f"🗑️ Send exact Service Name to delete:\nExisting: {', '.join(services)}")

@app.on_message(filters.text & filters.private & filters.regex("^➕ Add Number$"))
async def add_number_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "add_number_manual"}
    await message.reply_text("✏️ Send Phone Number with Country Code (e.g. +919876543210):")

@app.on_message(filters.text & filters.private & filters.regex("^➖ Remove Number$"))
async def remove_number_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "remove_number_manual"}
    await message.reply_text("🗑️ Send Phone Number to remove:")

@app.on_message(filters.text & filters.private & filters.regex("^🚫 Ban User$"))
async def ban_user_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "ban_user"}
    await message.reply_text("🚫 Send User ID to ban:")

@app.on_message(filters.text & filters.private & filters.regex("^✅ Unban User$"))
async def unban_user_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "unban_user"}
    await message.reply_text("✅ Send User ID to unban:")

@app.on_message(filters.text & filters.private & filters.regex("^📢 Broadcast$"))
async def broadcast_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "broadcast_msg"}
    await message.reply_text("📢 Send the message you want to broadcast to all users:")

@app.on_message(filters.text & filters.private & filters.regex("^📋 Total Users$"))
async def total_users_cmd(client, message):
    if not is_admin(message.from_user.id): return
    users = list(db.users.find({}).limit(50))
    msg = f"📋 <b>TOTAL USERS ({len(users)} shown):</b>\n━━━━━━━━━━━━━━━━━━━━━━━\n"
    for u in users:
        msg += f"• <code>{u['user_id']}</code> - @{u.get('username', 'N/A')}\n"
    await message.reply_text(msg, parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.text & filters.private & filters.regex("^🎭 Manage Emojis$"))
async def manage_emojis_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "update_emoji_key"}
    await message.reply_text(
        text=(
            f"{e('crown')} <b>EMOJI MANAGER</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Enter Emoji Key Name (e.g., <code>red_a</code>, <code>crown</code>):"
        ),
        parse_mode=enums.ParseMode.HTML
    )

# ================= CALLBACK HANDLER =================
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    try:
        data = query.data
        user_id = query.from_user.id
        
        if data.startswith("change_"):
            service = data.replace("change_", "")
            await query.answer("Fetching new numbers...")
            
            numbers, error = await allocate_three_numbers(user_id, service)
            if error:
                await query.message.edit_text(f"❌ {error}", parse_mode=enums.ParseMode.HTML)
                return
                
            nums_text = ""
            for num in numbers:
                flag = get_country_flag_unicode(num)
                # User PM ke liye FULL number tap to copy (+919876543210)
                clean = str(num).replace("+", "").strip()
                nums_text += f"{flag} <code>+{clean}</code> (Tap to Copy)\n"
                
            controls_inline = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{service}"), InlineKeyboardButton("🛡️ OTP Group", url=OTP_GROUP_LINK)],
                [InlineKeyboardButton("❌ Close", callback_data="close_menu")]
            ])
            
            await query.message.edit_text(
                text=(
                    f"{e('verify_blue')} <b>Your requested numbers for {service}:</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{nums_text}"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👇 Tap on any number to copy instantly!"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=controls_inline
            )
            
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
            await message.reply_text(f"✅ Service <b>{text}</b> added!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "delete_service_name" and is_admin(user_id):
            user_states.pop(user_id, None)
            db.services.delete_one({"name": text})
            await message.reply_text(f"🗑️ Service <b>{text}</b> removed!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "add_number_manual" and is_admin(user_id):
            user_states.pop(user_id, None)
            clean_num = text.replace("+", "").strip()
            db.numbers.update_one({"number": clean_num}, {"$set": {"number": clean_num, "status": "available", "assigned_to": None, "otp_count": 0}}, upsert=True)
            await message.reply_text(f"✅ Number <code>+{clean_num}</code> added to DB!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "remove_number_manual" and is_admin(user_id):
            user_states.pop(user_id, None)
            clean_num = text.replace("+", "").strip()
            db.numbers.delete_one({"number": clean_num})
            await message.reply_text(f"🗑️ Number <code>+{clean_num}</code> removed!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "ban_user" and is_admin(user_id):
            user_states.pop(user_id, None)
            target_id = int(text)
            db.users.update_one({"user_id": target_id}, {"$set": {"is_banned": True}})
            await message.reply_text(f"🚫 User <code>{target_id}</code> banned!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "unban_user" and is_admin(user_id):
            user_states.pop(user_id, None)
            target_id = int(text)
            db.users.update_one({"user_id": target_id}, {"$set": {"is_banned": False}})
            await message.reply_text(f"✅ User <code>{target_id}</code> unbanned!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "broadcast_msg" and is_admin(user_id):
            user_states.pop(user_id, None)
            users = db.users.find({"is_banned": False})
            success = 0
            for u in users:
                try:
                    await message.copy(u["user_id"])
                    success += 1
                except Exception:
                    pass
            await message.reply_text(f"📢 Broadcast sent to <b>{success}</b> users!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "search_number":
            user_states.pop(user_id, None)
            clean_num = text.replace("+", "").strip()
            doc = db.numbers.find_one({"number": clean_num})
            if doc:
                flag = get_country_flag_unicode(clean_num)
                await message.reply_text(
                    f"🔍 <b>Number Found:</b>\n"
                    f"• Phone: {flag} <code>+{clean_num}</code>\n"
                    f"• Status: <b>{doc.get('status', 'unknown')}</b>\n"
                    f"• Service: <b>{doc.get('service', 'N/A')}</b>\n"
                    f"• Total OTPs: <b>{doc.get('otp_count', 0)}</b>",
                    parse_mode=enums.ParseMode.HTML,
                    reply_markup=get_main_keyboard(user_id)
                )
            else:
                await message.reply_text("❌ Number not found in database.", reply_markup=get_main_keyboard(user_id))

        elif action == "update_emoji_key" and is_admin(user_id):
            user_states[user_id] = {"action": "update_emoji_id", "key": text.lower()}
            await message.reply_text(f"Key <code>{text.lower()}</code> selected.\nSend Custom Emoji ID:", parse_mode=enums.ParseMode.HTML)

        elif action == "update_emoji_id" and is_admin(user_id):
            key = state.get("key")
            user_states.pop(user_id, None)
            db.emojis.update_one({"key": key}, {"$set": {"id": text}}, upsert=True)
            await message.reply_text(f"🎉 Emoji for <code>{key}</code> updated!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "select_service":
            user_states.pop(user_id, None)
            if text == "🔙 Back to Main":
                await back_to_main(client, message)
                return
            
            numbers, error = await allocate_three_numbers(user_id, text)
            if error:
                await message.reply_text(f"❌ {error}", reply_markup=get_main_keyboard(user_id))
                return
                
            nums_text = ""
            for num in numbers:
                flag = get_country_flag_unicode(num)
                # User PM me FULL number dikhayega (+919876543210) taaki ek tap me copy ho sake
                clean = str(num).replace("+", "").strip()
                nums_text += f"{flag} <code>+{clean}</code> (Tap to Copy)\n"
                
            controls_inline = InlineKeyboardMarkup([
                [InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{text}"), InlineKeyboardButton("🛡️ OTP Group", url=OTP_GROUP_LINK)],
                [InlineKeyboardButton("❌ Close", callback_data="close_menu")]
            ])
            
            await message.reply_text(
                text=(
                    f"{e('verify_blue')} <b>Your requested numbers for {text}:</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{nums_text}"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👇 Tap on any number to copy instantly!"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=controls_inline
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
