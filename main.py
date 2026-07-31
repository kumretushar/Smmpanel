import asyncio
import re
import aiohttp
import phonenumbers
from datetime import datetime, timedelta
from collections import Counter
from pyrogram import Client, filters, enums
from pyrogram.types import (
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    CallbackQuery
)
from pymongo import MongoClient

# ================= CONFIGURATION =================
API_ID = 30954859
API_HASH = "240537c89299fc2c94e8c78607229a21"
BOT_TOKEN = "8841502557:AAH7m1ezXQbK8DKHsGuY6T7H2IMPtRAeVq8"

GROUP_ID = -1002949251809
LOG_CHANNEL_ID = -1004393777682  # Ensure bot is admin in this channel

MUST_JOIN_CHANNEL = "@gmtusharxfiles"
OTP_GROUP_LINK = "https://t.me/trxxotp"

BOT_NAME = "GMxOTP"
ADMIN_IDS = [8430946490]
OWNER_USERNAME = "@Amarstarx"

# ================= EXTERNAL PANELS CONFIG =================
IVAS_CONFIG = {
    "login_url": "https://ivas.tempnum.qzz.io/login",
    "base_url": "https://ivas.tempnum.qzz.io",
    "sms_endpoint": "https://ivas.tempnum.qzz.io/portal/sms/received/getsms",
    "username": "your_email@gmail.com",
    "password": "your_password"
}

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
    },
    {
        "name": "TIME Panel",
        "url": "http://147.135.212.197/crapi/time/viewstats",
        "otp_url": "http://147.135.212.197/crapi/time/getotp",
        "token": "Qk5WSjRSQmZUZZFnaWZxVYpXU4OIlFFiWU5TeohQUGhHjGZpfGhx"
    }
]

# ================= DATABASE =================
MONGO_URI = "mongodb://tusharkumarin74_db_user:star%40123@ac-zborjum-shard-00-00.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-01.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-02.7jv0uuq.mongodb.net:27017/?ssl=true&replicaSet=atlas-qnvkfj-shard-0&authSource=admin&appName=Cluster"

try:
    db_client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = db_client.numberx
    print("✅ Connected to MongoDB Successfully")
except Exception as err:
    print(f"❌ MongoDB Connection Failed: {err}")

if db.settings.count_documents({"setting_id": "bot_config"}) == 0:
    db.settings.insert_one({"setting_id": "bot_config", "is_active": True})

# ================= PYROGRAM CLIENT =================
app = Client(
    "numberx_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=5,
    workers=100
)

# ================= WORLDWIDE COUNTRY MAPPING =================
COUNTRY_MAPPING = {
    "AFGHANISTAN": "AF", "ALBANIA": "AL", "ALGERIA": "DZ", "ANDORRA": "AD",
    "ANGOLA": "AO", "ARGENTINA": "AR", "ARMENIA": "AM", "AUSTRALIA": "AU",
    "AUSTRIA": "AT", "AZERBAIJAN": "AZ", "BAHAMAS": "BS", "BAHRAIN": "BH",
    "BANGLADESH": "BD", "BARBADOS": "BB", "BELARUS": "BY", "BELGIUM": "BE",
    "BELIZE": "BZ", "BENIN": "BJ", "BHUTAN": "BT", "BOLIVIA": "BO",
    "BOSNIA AND HERZEGOVINA": "BA", "BOTSWANA": "BW", "BRAZIL": "BR", "BRUNEI": "BN",
    "BULGARIA": "BG", "BURKINA FASO": "BF", "BURUNDI": "BI", "CAMBODIA": "KH",
    "CAMEROON": "CM", "CANADA": "CA", "CHILE": "CL", "CHINA": "CN",
    "COLOMBIA": "CO", "CONGO": "CG", "COSTA RICA": "CR", "CROATIA": "HR",
    "CUBA": "CU", "CYPRUS": "CY", "CZECH REPUBLIC": "CZ", "DENMARK": "DK",
    "DOMINICAN REPUBLIC": "DO", "ECUADOR": "EC", "EGYPT": "EG", "EL SALVADOR": "SV",
    "ESTONIA": "EE", "ETHIOPIA": "ET", "FINLAND": "FI", "FRANCE": "FR",
    "GEORGIA": "GE", "GERMANY": "DE", "GHANA": "GH", "GREECE": "GR",
    "GUATEMALA": "GT", "HAITI": "HT", "HONDURAS": "HN", "HONG KONG": "HK",
    "HUNGARY": "HU", "ICELAND": "IS", "INDIA": "IN", "INDONESIA": "ID",
    "IRAN": "IR", "IRAQ": "IQ", "IRELAND": "IE", "ISRAEL": "IL",
    "ITALY": "IT", "JAMAICA": "JM", "JAPAN": "JP", "JORDAN": "JO",
    "KAZAKHSTAN": "KZ", "KENYA": "KE", "KOREA": "KR", "KUWAIT": "KW",
    "KYRGYZSTAN": "KG", "LAOS": "LA", "LATVIA": "LV", "LEBANON": "LB",
    "LIBERIA": "LR", "LIBYA": "LY", "LITHUANIA": "LT", "LUXEMBOURG": "LU",
    "MADAGASCAR": "MG", "MALAYSIA": "MY", "MALDIVES": "MV", "MALI": "ML",
    "MALTA": "MT", "MAURITIUS": "MU", "MEXICO": "MX", "MOLDOVA": "MD", "MONACO": "MC",
    "MONGOLIA": "MN", "MONTENEGRO": "ME", "MOROCCO": "MA", "MOZAMBIQUE": "MZ",
    "MYANMAR": "MM", "NAMIBIA": "NA", "NEPAL": "NP", "NETHERLANDS": "NL",
    "NEW ZEALAND": "NZ", "NICARAGUA": "NI", "NIGER": "NE", "NIGERIA": "NG",
    "NORTH MACEDONIA": "MK", "NORWAY": "NO", "OMAN": "OM", "PAKISTAN": "PK",
    "PALESTINE": "PS", "PANAMA": "PA", "PARAGUAY": "PY", "PERU": "PE",
    "PHILIPPINES": "PH", "POLAND": "PL", "PORTUGAL": "PT", "QATAR": "QA",
    "ROMANIA": "RO", "RUSSIA": "RU", "RWANDA": "RW", "SAUDI ARABIA": "SA",
    "SENEGAL": "SN", "SERBIA": "RS", "SINGAPORE": "SG", "SLOVAKIA": "SK",
    "SLOVENIA": "SI", "SOMALIA": "SO", "SOUTH AFRICA": "ZA", "SPAIN": "ES",
    "SRI LANKA": "LK", "SUDAN": "SD", "SWEDEN": "SE", "SWITZERLAND": "CH",
    "SYRIA": "SY", "TAIWAN": "TW", "TAJIKISTAN": "TJ", "TANZANIA": "TZ",
    "THAILAND": "TH", "TUNISIA": "TN", "TURKEY": "TR", "TURKMENISTAN": "TM",
    "UGANDA": "UG", "UKRAINE": "UA", "UNITED ARAB EMIRATES": "AE", "UAE": "AE",
    "UNITED KINGDOM": "GB", "UK": "GB", "UNITED STATES": "US", "USA": "US",
    "URUGUAY": "UY", "UZBEKISTAN": "UZ", "VENEZUELA": "VE", "VIETNAM": "VN",
    "YEMEN": "YE", "ZAMBIA": "ZM", "ZIMBABWE": "ZW"
}

OTP_REGEX = r'\b(\d{4,8})\b'

# ================= UTILS & HELPERS =================
def is_bot_active():
    doc = db.settings.find_one({"setting_id": "bot_config"})
    return doc.get("is_active", True) if doc else True

def toggle_bot_status():
    current = is_bot_active()
    db.settings.update_one({"setting_id": "bot_config"}, {"$set": {"is_active": not current}}, upsert=True)
    return not current

def extract_otp_code(text):
    if not text: return None
    matches = re.findall(OTP_REGEX, str(text))
    return matches[0] if matches else None

def clean_number_str(num):
    if not num: return ""
    return re.sub(r'\D', '', str(num))

def detect_service(full_sms):
    if not full_sms: return "SMS SERVICE"
    sms_lower = str(full_sms).lower()
    service_keywords = {
        "facebook": "FACEBOOK", "fb": "FACEBOOK",
        "instagram": "INSTAGRAM", "insta": "INSTAGRAM",
        "tiktok": "TIKTOK", "twitter": "TWITTER", "x.com": "TWITTER",
        "snapchat": "SNAPCHAT", "snap": "SNAPCHAT",
        "whatsapp": "WHATSAPP", "telegram": "TELEGRAM",
        "discord": "DISCORD", "messenger": "MESSENGER",
        "linkedin": "LINKEDIN", "google": "GOOGLE", "gmail": "GOOGLE",
        "amazon": "AMAZON", "microsoft": "MICROSOFT",
        "paypal": "PAYPAL", "binance": "BINANCE", "spotify": "SPOTIFY",
        "netflix": "NETFLIX", "uber": "UBER", "apple": "APPLE"
    }

    for keyword, service_name in sorted(service_keywords.items(), key=lambda x: len(x[0]), reverse=True):
        if keyword in sms_lower:
            return service_name

    return "SMS SERVICE"

def get_flag_from_country_name(country_name):
    try:
        clean_name = str(country_name).upper().strip()
        cc = COUNTRY_MAPPING.get(clean_name)
        if not cc and len(clean_name) == 2: cc = clean_name
        if cc: return "".join(chr(127397 + ord(c)) for c in cc)
    except Exception: pass
    return "🌐"

def get_flag_from_number(number):
    clean_num = clean_number_str(number)
    try:
        formatted = f"+{clean_num}"
        parsed = phonenumbers.parse(formatted)
        country_code = phonenumbers.region_code_for_number(parsed)
        if country_code: return "".join(chr(127397 + ord(c)) for c in country_code)
    except Exception: pass
    return "🌐"

def mask_number_for_group(number):
    clean_num = clean_number_str(number)
    if len(clean_num) > 4:
        return f"+{clean_num[:2]}xxxx{clean_num[-2:]}"
    return f"+{clean_num}"

user_states = {}

def is_admin(user_id): return user_id in ADMIN_IDS

def is_banned(user_id):
    try:
        user = db.users.find_one({"user_id": user_id})
        return user and user.get("is_banned", False)
    except Exception: return False

def add_user(user_id, username, first_name):
    try:
        if not db.users.find_one({"user_id": user_id}):
            db.users.insert_one({
                "user_id": user_id,
                "username": username or "N/A",
                "first_name": first_name or "User",
                "joined_date": datetime.now(),
                "is_banned": False,
                "numbers_allocated": 0
            })
    except Exception as ex: print(f"Error adding user: {ex}")

async def check_must_join(client, user_id):
    if is_admin(user_id): return True
    try:
        member = await client.get_chat_member(MUST_JOIN_CHANNEL, user_id)
        if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.MEMBER]:
            return True
    except Exception: pass
    return False

def get_all_services():
    try: return list(set([s["name"] for s in db.services.find({}) if s.get("name")]))
    except Exception: return []

def get_all_countries():
    try: return list(set([c["name"] for c in db.countries.find({}) if c.get("name")]))
    except Exception: return []

# ================= KEYBOARDS =================
def get_main_keyboard(user_id):
    buttons = [
        ["📱 Get Number", "🔍 Search Number"],
        ["📊 Traffic Stats", "🆘 Support / Owner"]
    ]
    if is_admin(user_id):
        buttons.append(["⚙️ Admin Panel"])
    return ReplyKeyboardMarkup(buttons, resize_keyboard=True)

def get_admin_keyboard():
    status_str = "🟢 BOT ON" if is_bot_active() else "🔴 BOT OFF"
    return ReplyKeyboardMarkup([
        [f"⚡ Toggle Bot Status ({status_str})"],
        ["➕ Add Service", "➖ Delete Service"],
        ["➕ Add Number", "🗑️ Delete Country Stock"],
        ["🌐 Manage Countries"],
        ["🚫 Ban User", "✅ Unban User"],
        ["📈 Special Stats", "📋 Total Users"],
        ["📢 Broadcast", "🔙 Back to Main"]
    ], resize_keyboard=True)

def get_must_join_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/{MUST_JOIN_CHANNEL.replace('@', '')}")],
        [InlineKeyboardButton("✅ Joined / Verify", callback_data="check_join_sub")]
    ])

# ================= LOG SYSTEM =================
async def send_log(msg_text):
    try:
        await app.send_message(LOG_CHANNEL_ID, msg_text, parse_mode=enums.ParseMode.HTML)
    except Exception as e:
        print(f"Log Error: {e}")

# ================= OTP PROCESSOR =================
async def process_and_send_otp(number_doc, otp_code, full_sms=""):
    num = clean_number_str(number_doc["number"])
    detected_srv = detect_service(full_sms)
    service = number_doc.get("service", detected_srv)
    if service == "SMS SERVICE" and detected_srv != "SMS SERVICE":
        service = detected_srv

    country_name = number_doc.get("country", "UNKNOWN")
    assigned_user = number_doc.get("assigned_to", "Unknown")
    flag = get_flag_from_number(num)
    masked_num = mask_number_for_group(num)
    
    group_msg = (
        f"📩 <b>NEW OTP RECEIVED</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>User ID:</b> <code>{assigned_user}</code>\n"
        f"🛠️ <b>Service:</b> {service}\n"
        f"📱 <b>Number:</b> {flag} <code>{masked_num}</code>\n"
        f"🔑 <b>OTP Code:</b> <code>{otp_code}</code> (Tap to Copy)\n"
        f"📝 <b>Text:</b> <i>{full_sms}</i>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    try:
        await app.send_message(GROUP_ID, group_msg, parse_mode=enums.ParseMode.HTML)
    except Exception as ge:
        print(f"Failed to send OTP to Group: {ge}")

    # Record completed status & timestamp for Live Traffic calculation
    now = datetime.now()
    db.numbers.update_one(
        {"_id": number_doc["_id"]}, 
        {"$set": {"status": "completed", "completed_at": now}, "$inc": {"otp_count": 1}}
    )

    # Save traffic log entry
    db.traffic_logs.insert_one({
        "number": num,
        "country": country_name,
        "service": service,
        "user_id": assigned_user,
        "timestamp": now
    })

    await send_log(
        f"🔑 <b>OTP LOG DETECTED</b>\n"
        f"• User ID: <code>{assigned_user}</code>\n"
        f"• Service: <b>{service}</b>\n"
        f"• Country: <b>{country_name}</b>\n"
        f"• Phone: <code>+{num}</code>\n"
        f"• OTP Code: <code>{otp_code}</code>\n"
        f"• Text: <code>{full_sms}</code>"
    )

# ================= BACKGROUND OTP CHECKER =================
async def background_otp_checker():
    while True:
        try:
            if is_bot_active():
                active_numbers = list(db.numbers.find({"status": "in_use"}))
                
                if active_numbers:
                    async with aiohttp.ClientSession() as session:
                        try:
                            today_str = datetime.now().strftime("%Y-%m-%d")
                            ivas_url = f"{IVAS_CONFIG['sms_endpoint']}?date={today_str}"
                            
                            async with session.get(ivas_url, timeout=6) as ivas_resp:
                                if ivas_resp.status == 200:
                                    ivas_data = await ivas_resp.json()
                                    ivas_messages = ivas_data.get("otp_messages") or ivas_data.get("data") or []
                                    
                                    for msg_obj in ivas_messages:
                                        raw_phone = clean_number_str(msg_obj.get("phone_number") or msg_obj.get("number") or "")
                                        sms_content = msg_obj.get("otp_message") or msg_obj.get("sms") or ""
                                        
                                        for doc in active_numbers:
                                            db_num = clean_number_str(doc["number"])
                                            if db_num and (db_num in raw_phone or raw_phone in db_num):
                                                otp_code = extract_otp_code(sms_content) or "UNKNOWN"
                                                await process_and_send_otp(doc, otp_code, sms_content)
                        except Exception: pass

                        for doc in active_numbers:
                            num = clean_number_str(doc["number"])
                            for panel in PANELS:
                                try:
                                    url = f"{panel['otp_url']}?number={num}"
                                    headers = {"Authorization": panel["token"]}
                                    async with session.get(url, headers=headers, timeout=4) as resp:
                                        if resp.status == 200:
                                            res = await resp.json()
                                            raw_sms = res.get("otp") or res.get("code") or res.get("sms") or ""
                                            if raw_sms:
                                                otp_code = extract_otp_code(raw_sms) or raw_sms
                                                await process_and_send_otp(doc, otp_code, raw_sms)
                                except Exception: pass

        except Exception as ex: print(f"Loop Exception: {ex}")
        await asyncio.sleep(2)

# ================= NUMBER ALLOCATION =================
async def allocate_three_numbers(user_id, service, country_name):
    query = {"status": "available", "service": service, "country": country_name}
    number_docs = list(db.numbers.find(query).limit(3))
    
    if not number_docs:
        return None, f"Is service/country ({country_name}) ke liye stock empty hai."
    
    numbers_list = []
    for doc in number_docs:
        db.numbers.update_one(
            {"_id": doc["_id"]},
            {"$set": {"status": "in_use", "assigned_to": user_id, "allocated_at": datetime.now()}}
        )
        numbers_list.append(clean_number_str(doc["number"]))
    
    db.users.update_one({"user_id": user_id}, {"$inc": {"numbers_allocated": len(numbers_list)}})
    
    await send_log(
        f"📱 <b>NUMBER ALLOCATED</b>\n"
        f"• User ID: <code>{user_id}</code>\n"
        f"• Service: {service}\n"
        f"• Country: {country_name}\n"
        f"• Numbers: {', '.join(numbers_list)}"
    )
    return numbers_list, None

# ================= COMMAND HANDLERS =================
@app.on_message(filters.command("start"))
async def start(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    
    add_user(user_id, message.from_user.username or "N/A", message.from_user.first_name or "User")
    if is_banned(user_id): return

    if not is_bot_active() and not is_admin(user_id):
        await message.reply_text("🔴 <b>Bot Maintenance Mod par hai. Kripya thodi der baad try karein!</b>", parse_mode=enums.ParseMode.HTML)
        return

    if not await check_must_join(client, user_id):
        await message.reply_text(
            f"⚠️ <b>Access Denied!</b>\nJoin channel: {MUST_JOIN_CHANNEL}",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=get_must_join_keyboard()
        )
        return

    await message.reply_text(
        f"👑 Welcome to <b>{BOT_NAME}</b>",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=get_main_keyboard(user_id)
    )

# ================= TRAFFIC STATS (NEW UI) =================
@app.on_message(filters.regex("^📊 Traffic Stats$"))
async def traffic_stats_cmd(client, message):
    ten_mins_ago = datetime.now() - timedelta(minutes=10)
    
    # Query logs in last 10 minutes
    logs = list(db.traffic_logs.find({"timestamp": {"$gte": ten_mins_ago}}))
    results_sent = len(logs)
    
    country_counts = Counter([l.get("country", "UNKNOWN") for l in logs])
    total_logs = sum(country_counts.values())
    
    if total_logs > 0:
        top_country_name, top_count = country_counts.most_common(1)[0]
        top_flag = get_flag_from_country_name(top_country_name)
        top_country_str = f"{top_flag} {top_country_name.title()} 📱"
    else:
        top_country_str = "None 📱"

    country_list_text = ""
    if total_logs > 0:
        for idx, (cntry, cnt) in enumerate(country_counts.most_common(5), 1):
            pct = (cnt / total_logs) * 100
            c_flag = get_flag_from_country_name(cntry)
            country_list_text += f"{idx}. {c_flag} {cntry.title()} ➡️ {pct:.1f}% 📱\n"
    else:
        country_list_text = "No traffic recorded in last 10 minutes.\n"

    time_now_str = datetime.now().strftime("%H:%M:%S")

    stats_msg = (
        f"🟢 <b>Live Traffic</b>\n\n"
        f"📅 <b>Window:</b> Last 10 minutes\n"
        f"👁 <b>Results Sent:</b> {results_sent}\n"
        f"🔝 <b>Top Country:</b> {top_country_str}\n\n"
        f"🌍 <b>Top Countries:</b>\n"
        f"{country_list_text}\n"
        f"⏱ <b>Last Update:</b> {time_now_str}"
    )

    await message.reply_text(stats_msg, parse_mode=enums.ParseMode.HTML)

# ================= ADMIN ACTIONS & HANDLERS =================
@app.on_message(filters.regex("^⚙️ Admin Panel$"))
async def admin_panel_cmd(client, message):
    if not is_admin(message.from_user.id): return
    await message.reply_text("🛠️ <b>Welcome to Admin Control Panel</b>", parse_mode=enums.ParseMode.HTML, reply_markup=get_admin_keyboard())

@app.on_message(filters.regex(r"^⚡ Toggle Bot Status"))
async def toggle_bot_cmd(client, message):
    if not is_admin(message.from_user.id): return
    new_state = toggle_bot_status()
    state_str = "🟢 ONLINE / ACTIVE" if new_state else "🔴 OFFLINE / MAINTENANCE"
    await message.reply_text(f"⚙️ <b>Bot Status Updated:</b> {state_str}", parse_mode=enums.ParseMode.HTML, reply_markup=get_admin_keyboard())

@app.on_message(filters.regex("^➕ Add Service$"))
async def add_service_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "add_service"}
    await message.reply_text("✨ Service ka naam likho jise add karna hai:")

@app.on_message(filters.regex("^➖ Delete Service$"))
async def del_service_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "del_service"}
    await message.reply_text("🗑️ Service ka naam likho jise delete karna hai:")

@app.on_message(filters.regex("^🌐 Manage Countries$"))
async def add_country_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "add_country"}
    await message.reply_text("🌍 Country ka name type karo (Eg: India, Sudan):")

@app.on_message(filters.regex("^➕ Add Number$"))
async def add_number_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "add_number"}
    await message.reply_text("📱 Format me enter karo:\n<code>SERVICE | COUNTRY | NUMBER</code>\n\nExample:\n<code>WhatsApp | SUDAN | 249912345678</code>", parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.regex("^🗑️ Delete Country Stock$"))
async def del_stock_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "del_stock"}
    await message.reply_text("🗑️ Country name likho jiska poora stock delete karna hai:")

@app.on_message(filters.regex("^🚫 Ban User$"))
async def ban_user_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "ban_user"}
    await message.reply_text("🚫 User ID type karo jisko BAN karna hai:")

@app.on_message(filters.regex("^✅ Unban User$"))
async def unban_user_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "unban_user"}
    await message.reply_text("✅ User ID type karo jisko UNBAN karna hai:")

@app.on_message(filters.regex("^📋 Total Users$"))
async def total_users_cmd(client, message):
    if not is_admin(message.from_user.id): return
    count = db.users.count_documents({})
    banned = db.users.count_documents({"is_banned": True})
    await message.reply_text(f"📊 <b>Total Users:</b> {count}\n🚫 <b>Banned Users:</b> {banned}", parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.regex("^📈 Special Stats$"))
async def special_stats_cmd(client, message):
    total_nums = db.numbers.count_documents({})
    available = db.numbers.count_documents({"status": "available"})
    in_use = db.numbers.count_documents({"status": "in_use"})
    completed = db.numbers.count_documents({"status": "completed"})
    
    msg = (
        f"📊 <b>STOCK & SYSTEM STATS</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 Total Stock: {total_nums}\n"
        f"✅ Available: {available}\n"
        f"⏳ In Use: {in_use}\n"
        f"🔑 Completed OTPs: {completed}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    await message.reply_text(msg, parse_mode=enums.ParseMode.HTML)

@app.on_message(filters.regex("^📢 Broadcast$"))
async def broadcast_cmd(client, message):
    if not is_admin(message.from_user.id): return
    user_states[message.from_user.id] = {"action": "broadcast"}
    await message.reply_text("📢 Message type karo sabhi users ko bhejne ke liye:")

@app.on_message(filters.regex("^🔙 Back to Main$"))
async def back_main_cmd(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    await message.reply_text("🔙 Back to Main Menu", reply_markup=get_main_keyboard(user_id))

@app.on_message(filters.regex("^🆘 Support / Owner$"))
async def support_cmd(client, message):
    await message.reply_text(f"🆘 Contact Owner: {OWNER_USERNAME}")

# ================= GENERAL USER & ADMIN TEXT INPUT HANDLER =================
@app.on_message(filters.regex("^📱 Get Number$"))
async def get_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id): return
    
    if not is_bot_active() and not is_admin(user_id):
        await message.reply_text("🔴 <b>Bot Maintenance par hai!</b>", parse_mode=enums.ParseMode.HTML)
        return

    services = get_all_services()
    if not services:
        await message.reply_text("❌ Currently no services are available.")
        return
        
    service_buttons = [[s] for s in services] + [["🔙 Back to Main"]]
    user_states[user_id] = {"action": "select_service"}
    
    await message.reply_text("✨ Select Service:", parse_mode=enums.ParseMode.HTML, reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True))

@app.on_message(filters.text & ~filters.command("start"))
async def text_handler(client, message):
    user_id = message.from_user.id
    text = message.text.strip()
    
    if user_id not in user_states: return
    state = user_states[user_id]
    action = state.get("action")

    # ----- User Selection -----
    if action == "select_service":
        user_states.pop(user_id, None)
        if text == "🔙 Back to Main": return
        
        countries = get_all_countries()
        if not countries:
            await message.reply_text("❌ No countries configured.")
            return

        inline_kb = []
        for c in countries:
            flag = get_flag_from_country_name(c)
            inline_kb.append([InlineKeyboardButton(f"{flag} {c}", callback_data=f"country_{text}___{c}")])
        
        await message.reply_text(f"🌍 Select Country for <b>{text}</b>:", parse_mode=enums.ParseMode.HTML, reply_markup=InlineKeyboardMarkup(inline_kb))

    # ----- Admin Actions Processing -----
    elif action == "add_service" and is_admin(user_id):
        user_states.pop(user_id, None)
        db.services.insert_one({"name": text})
        await message.reply_text(f"✅ Service <b>{text}</b> added successfully!", parse_mode=enums.ParseMode.HTML)

    elif action == "del_service" and is_admin(user_id):
        user_states.pop(user_id, None)
        db.services.delete_many({"name": text})
        await message.reply_text(f"🗑️ Service <b>{text}</b> removed!", parse_mode=enums.ParseMode.HTML)

    elif action == "add_country" and is_admin(user_id):
        user_states.pop(user_id, None)
        db.countries.insert_one({"name": text.upper()})
        await message.reply_text(f"🌍 Country <b>{text.upper()}</b> added successfully!", parse_mode=enums.ParseMode.HTML)

    elif action == "add_number" and is_admin(user_id):
        user_states.pop(user_id, None)
        try:
            srv, cntry, num = [x.strip() for x in text.split("|")]
            db.numbers.insert_one({
                "service": srv,
                "country": cntry.upper(),
                "number": clean_number_str(num),
                "status": "available",
                "assigned_to": None,
                "created_at": datetime.now()
            })
            await message.reply_text(f"✅ Number <b>+{clean_number_str(num)}</b> added for {srv} ({cntry})!", parse_mode=enums.ParseMode.HTML)
        except Exception:
            await message.reply_text("❌ Invalid Format! Use: <code>Service | Country | Number</code>", parse_mode=enums.ParseMode.HTML)

    elif action == "del_stock" and is_admin(user_id):
        user_states.pop(user_id, None)
        res = db.numbers.delete_many({"country": text.upper()})
        await message.reply_text(f"🗑️ Deleted {res.deleted_count} numbers from {text.upper()}")

    elif action == "ban_user" and is_admin(user_id):
        user_states.pop(user_id, None)
        try:
            uid = int(text)
            db.users.update_one({"user_id": uid}, {"$set": {"is_banned": True}}, upsert=True)
            await message.reply_text(f"🚫 User <code>{uid}</code> Banned!", parse_mode=enums.ParseMode.HTML)
        except Exception:
            await message.reply_text("❌ Invalid User ID!")

    elif action == "unban_user" and is_admin(user_id):
        user_states.pop(user_id, None)
        try:
            uid = int(text)
            db.users.update_one({"user_id": uid}, {"$set": {"is_banned": False}})
            await message.reply_text(f"✅ User <code>{uid}</code> Unbanned!", parse_mode=enums.ParseMode.HTML)
        except Exception:
            await message.reply_text("❌ Invalid User ID!")

    elif action == "broadcast" and is_admin(user_id):
        user_states.pop(user_id, None)
        users = db.users.find({})
        count = 0
        for u in users:
            try:
                await app.send_message(u["user_id"], text)
                count += 1
                await asyncio.sleep(0.05)
            except Exception: pass
        await message.reply_text(f"📢 Broadcast sent to {count} users!")

# ================= CALLBACK HANDLER =================
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    if data.startswith("copy_num_"):
        num_to_copy = data.replace("copy_num_", "")
        await query.answer(f"Copied: +{num_to_copy}", show_alert=False)
        return

    if data.startswith("country_"):
        if not is_bot_active() and not is_admin(user_id):
            await query.answer("🔴 Bot is currently OFF for maintenance!", show_alert=True)
            return

        raw = data.replace("country_", "", 1)
        service, country_name = raw.split("___", 1)
        
        await query.answer("Fetching numbers...")
        numbers, error = await allocate_three_numbers(user_id, service, country_name)
        
        if error:
            await query.message.edit_text(f"❌ {error}")
            return
            
        inline_buttons = []
        msg_text = f"💬 <b>{service.upper()}</b>\n"
        msg_text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
        
        for n in numbers:
            flag = get_flag_from_number(n)
            msg_text += f"{flag} <code>+{n}</code>\n"
            inline_buttons.append([InlineKeyboardButton(f"📋 Copy: +{n}", callback_data=f"copy_num_{n}")])
            
        msg_text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
        msg_text += "👇 Tap number to copy or click below"

        inline_buttons.append([
            InlineKeyboardButton("🔄 Change Number", callback_data=f"country_{service}___{country_name}"),
            InlineKeyboardButton("🛡️ OTP Group", url=OTP_GROUP_LINK)
        ])
        inline_buttons.append([InlineKeyboardButton("❌ Close", callback_data="close_panel")])
        
        await query.message.edit_text(
            msg_text,
            parse_mode=enums.ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(inline_buttons)
        )

    elif data == "close_panel":
        await query.message.delete()

# ================= STARTUP ENGINE =================
async def main():
    await app.start()
    print("🚀 Engine Started Successfully!")
    asyncio.create_task(background_otp_checker())
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
