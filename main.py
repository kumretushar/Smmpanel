import asyncio
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
LOG_CHANNEL_ID = -1004393777682
MUST_JOIN_CHANNEL = "@gmtusharxfiles"
OTP_GROUP_LINK = "https://t.me/trxxotp"

BOT_NAME = "GMxOTP"
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
    sleep_threshold=5,
    workers=100
)

# ================= HELPERS & UTILS =================
COUNTRY_MAPPING = {
    "AFGHANISTAN": "AF", "ALBANIA": "AL", "ALGERIA": "DZ", "ANDORRA": "AD", "ANGOLA": "AO",
    "ARGENTINA": "AR", "ARMENIA": "AM", "AUSTRALIA": "AU", "AUSTRIA": "AT", "AZERBAIJAN": "AZ",
    "BAHAMAS": "BS", "BAHRAIN": "BH", "BANGLADESH": "BD", "BARBADOS": "BB", "BELARUS": "BY",
    "BELGIUM": "BE", "BELIZE": "BZ", "BENIN": "BJ", "BHUTAN": "BT", "BOLIVIA": "BO",
    "BOSNIA AND HERZEGOVINA": "BA", "BOTSWANA": "BW", "BRAZIL": "BR", "BRUNEI": "BN", "BULGARIA": "BG",
    "BURKINA FASO": "BF", "BURUNDI": "BI", "CAMBODIA": "KH", "CAMEROON": "CM", "CANADA": "CA",
    "CAPE VERDE": "CV", "CENTRAL AFRICAN REPUBLIC": "CF", "CHAD": "TD", "CHILE": "CL", "CHINA": "CN",
    "COLOMBIA": "CO", "COMOROS": "KM", "CONGO": "CG", "COSTA RICA": "CR", "CROATIA": "HR",
    "CUBA": "CU", "CYPRUS": "CY", "CZECH REPUBLIC": "CZ", "DENMARK": "DK", "DJIBOUTI": "DJ",
    "DOMINICA": "DM", "DOMINICAN REPUBLIC": "DO", "ECUADOR": "EC", "EGYPT": "EG", "EL SALVADOR": "SV",
    "EQUATORIAL GUINEA": "GQ", "ERITREA": "ER", "ESTONIA": "EE", "ESWATINI": "SZ", "ETHIOPIA": "ET",
    "FIJI": "FJ", "FINLAND": "FI", "FRANCE": "FR", "GABON": "GA", "GAMBIA": "GM",
    "GEORGIA": "GE", "GERMANY": "DE", "GHANA": "GH", "GREECE": "GR", "GRENADA": "GD",
    "GUATEMALA": "GT", "GUINEA": "GN", "GUINEA-BISSAU": "GW", "GUYANA": "GY", "HAITI": "HT",
    "HONDURAS": "HN", "HUNGARY": "HU", "ICELAND": "IS", "INDIA": "IN", "INDONESIA": "ID",
    "IRAN": "IR", "IRAQ": "IQ", "IRELAND": "IE", "ISRAEL": "IL", "ITALY": "IT", "IVORY COAST": "CI",
    "JAMAICA": "JM", "JAPAN": "JP", "JORDAN": "JO", "KAZAKHSTAN": "KZ", "KENYA": "KE",
    "KIRIBATI": "KI", "KUWAIT": "KW", "KYRGYZSTAN": "KG", "LAOS": "LA", "LATVIA": "LV",
    "LEBANON": "LB", "LESOTHO": "LS", "LIBERIA": "LR", "LIBYA": "LY", "LIECHTENSTEIN": "LI",
    "LITHUANIA": "LT", "LUXEMBOURG": "LU", "MADAGASCAR": "MG", "MALAWI": "MW", "MALAYSIA": "MY",
    "MALDIVES": "MV", "MALI": "ML", "MALTA": "MT", "MAURITANIA": "MR", "MAURITIUS": "MU",
    "MEXICO": "MX", "MOLDOVA": "MD", "MONACO": "MC", "MONGOLIA": "MN", "MONTENEGRO": "ME",
    "MOROCCO": "MA", "MOZAMBIQUE": "MZ", "MYANMAR": "MM", "NAMIBIA": "NA", "NAURU": "NR",
    "NEPAL": "NP", "NETHERLANDS": "NL", "NEW ZEALAND": "NZ", "NICARAGUA": "NI", "NIGER": "NE",
    "NIGERIA": "NG", "NORTH KOREA": "KP", "NORTH MACEDONIA": "MK", "NORWAY": "NO", "OMAN": "OM",
    "PAKISTAN": "PK", "PALAU": "PW", "PANAMA": "PA", "PAPUA NEW GUINEA": "PG", "PARAGUAY": "PY",
    "PERU": "PE", "PHILIPPINES": "PH", "POLAND": "PL", "PORTUGAL": "PT", "QATAR": "QA",
    "ROMANIA": "RO", "RUSSIA": "RU", "RWANDA": "RW", "SAINT KITTS AND NEVIS": "KN", "SAINT LUCIA": "LC",
    "SAINT VINCENT AND THE GRENADINES": "VC", "SAMOA": "WS", "SAN MARINO": "SM", "SAO TOME AND PRINCIPE": "ST",
    "SAUDI ARABIA": "SA", "SENEGAL": "SN", "SERBIA": "RS", "SEYCHELLES": "SC", "SIERRA LEONE": "SL",
    "SINGAPORE": "SG", "SLOVAKIA": "SK", "SLOVENIA": "SI", "SOLOMON ISLANDS": "SB", "SOMALIA": "SO",
    "SOUTH AFRICA": "ZA", "SOUTH KOREA": "KR", "SOUTH SUDAN": "SS", "SPAIN": "ES", "SRI LANKA": "LK",
    "SUDAN": "SD", "SURINAME": "SR", "SWEDEN": "SE", "SWITZERLAND": "CH", "SYRIA": "SY",
    "TAIWAN": "TW", "TAJIKISTAN": "TJ", "TANZANIA": "TZ", "THAILAND": "TH", "TIMOR-LESTE": "TL",
    "TOGO": "TG", "TONGA": "TO", "TRINIDAD AND TOBAGO": "TT", "TUNISIA": "TN", "TURKEY": "TR",
    "TURKMENISTAN": "TM", "TUVALU": "TV", "UGANDA": "UG", "UKRAINE": "UA", "UNITED ARAB EMIRATES": "AE",
    "UAE": "AE", "UNITED KINGDOM": "GB", "UK": "GB", "UNITED STATES": "US", "USA": "US",
    "URUGUAY": "UY", "UZBEKISTAN": "UZ", "VANUATU": "VU", "VENEZUELA": "VE", "VIETNAM": "VN",
    "YEMEN": "YE", "ZAMBIA": "ZM", "ZIMBABWE": "ZW"
}

def get_flag_from_country_name(country_name):
    try:
        clean_name = str(country_name).upper().strip()
        cc = COUNTRY_MAPPING.get(clean_name)
        if not cc and len(clean_name) == 2:
            cc = clean_name
        if cc:
            return "".join(chr(127397 + ord(c)) for c in cc)
    except Exception:
        pass
    return "🌐"

def get_flag_from_number(number):
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
    clean_num = str(number).replace("+", "").strip()
    if len(clean_num) > 4:
        cc = clean_num[:2]
        last = clean_num[-2:]
        return f"+{cc}xxxx{last}"
    return f"+{clean_num}"

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

async def check_must_join(client, user_id):
    if is_admin(user_id):
        return True
    try:
        member = await client.get_chat_member(MUST_JOIN_CHANNEL, user_id)
        if member.status in [enums.ChatMemberStatus.OWNER, enums.ChatMemberStatus.ADMINISTRATOR, enums.ChatMemberStatus.MEMBER]:
            return True
    except Exception:
        pass
    return False

def get_all_services():
    try:
        services_db = [s["name"] for s in db.services.find({}) if s.get("name")]
        return list(set(services_db))
    except Exception:
        return []

def get_all_countries():
    try:
        countries_db = [c["name"] for c in db.countries.find({}) if c.get("name")]
        return list(set(countries_db))
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
    },
    {
        "name": "TIME Panel",
        "url": "http://147.135.212.197/crapi/time/viewstats",
        "otp_url": "http://147.135.212.197/crapi/time/getotp",
        "token": "Qk5WSjRSQmZUZZFnaWZxVYpXU4OIlFFiWU5TeohQUGhHjGZpfGhx"
    }
]

# ================= KEYBOARDS =================
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
        await app.send_message(LOG_CHANNEL_ID, f"📋 <b>[BOT LOG]</b>\n{msg_text}", parse_mode=enums.ParseMode.HTML)
    except Exception as ex:
        print(f"Log error: {ex}")

# ================= FAST ALLOCATE NUMBERS =================
async def allocate_three_numbers(user_id, service, country_name):
    try:
        query = {"status": "available", "service": service, "country": country_name}
        number_docs = list(db.numbers.find(query).limit(3))
        
        if len(number_docs) < 3:
            async with aiohttp.ClientSession() as session:
                async def fetch_panel(panel):
                    try:
                        async with session.get(panel["url"], headers={"Authorization": panel["token"]}, timeout=3) as resp:
                            if resp.status == 200:
                                return await resp.json()
                    except Exception:
                        pass
                    return None
                
                tasks = [fetch_panel(p) for p in PANELS]
                results = await asyncio.gather(*tasks)
                
                for data in results:
                    if data and data.get("numbers"):
                        for num in data.get("numbers", [])[:10]:
                            num_str = str(num)
                            parsed_country = country_name
                            try:
                                parsed = phonenumbers.parse(f"+{num_str.replace('+', '')}")
                                rc = phonenumbers.region_code_for_number(parsed)
                                if rc:
                                    for k, v in COUNTRY_MAPPING.items():
                                        if v == rc:
                                            parsed_country = k
                                            break
                            except Exception:
                                pass
                                
                            if not db.numbers.find_one({"number": num_str}):
                                db.numbers.insert_one({
                                    "number": num_str,
                                    "status": "available",
                                    "assigned_to": None,
                                    "service": service,
                                    "country": parsed_country,
                                    "otp_count": 0
                                })

            number_docs = list(db.numbers.find(query).limit(3))
            
        if not number_docs:
            return None, f"Is service/country ({country_name}) ke liye filhal numbers available nahi hain."
        
        numbers_list = []
        for doc in number_docs:
            db.numbers.update_one(
                {"_id": doc["_id"]},
                {"$set": {"status": "in_use", "assigned_to": user_id}}
            )
            numbers_list.append(doc["number"])
        
        db.users.update_one({"user_id": user_id}, {"$inc": {"numbers_allocated": len(numbers_list)}})
        await send_log(f"👤 User <code>{user_id}</code> got <b>{len(numbers_list)}</b> numbers for <b>{service}</b> ({country_name}).")
        
        return numbers_list, None
    except Exception as ex:
        return None, f"Database Error: {str(ex)}"

# ================= BACKGROUND OTP CHECKER =================
async def background_otp_checker():
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
                                async with session.get(url, headers={"Authorization": panel["token"]}, timeout=3) as resp:
                                    if resp.status == 200:
                                        res = await resp.json()
                                        otp = res.get("otp") or res.get("code")
                                        if otp:
                                            flag = get_flag_from_number(num)
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
                                            await send_log(f"🔑 OTP <code>{otp}</code> received for <code>{masked_num}</code> ({service}).")
                            except Exception:
                                pass
        except Exception as ex:
            print(f"OTP Loop Error: {ex}")
            
        await asyncio.sleep(4)

# ================= COMMAND HANDLERS =================
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    
    add_user(user_id, message.from_user.username or "User", message.from_user.first_name or "User")
    if is_banned(user_id):
        await message.reply_text("🚫 You are banned from using this bot.")
        return

    if not await check_must_join(client, user_id):
        await message.reply_text(
            f"⚠️ <b>Access Denied!</b>\n\nBot ko use karne ke liye aapko humara Official Channel <b>{MUST_JOIN_CHANNEL}</b> join karna zaroori hai.",
            parse_mode=enums.ParseMode.HTML,
            reply_markup=get_must_join_keyboard()
        )
        return

    await message.reply_text(
        text=(
            f"👑 <b>{BOT_NAME}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Hello <b>{message.from_user.first_name}</b>, welcome to OTP Bot.\n"
            f"Select an option below to get started:\n"
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
        text="🌐 <b>Main Menu</b>\n━━━━━━━━━━━━━━━━━━━━━━━",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=get_main_keyboard(user_id)
    )

@app.on_message(filters.regex("^🆘 Support / Owner$") | filters.command("owner"))
async def owner_info(client, message):
    msg_text = (
        f"👑 <b>BOT OWNER & DEVELOPER INFO</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"<b>Developer:</b> AMARSTARX\n"
        f"<b>Username:</b> {OWNER_USERNAME}\n"
        f"<b>Channel:</b> {MUST_JOIN_CHANNEL}\n"
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
            flag = get_flag_from_number(doc['number'])
            masked = mask_number_for_group(doc['number'])
            top_str += f"{idx}. {flag} <code>{masked}</code> - <b>{doc.get('otp_count', 0)} OTPs</b>\n"
    else:
        top_str = "No OTP data recorded yet.\n"
    
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
    if not await check_must_join(client, user_id):
        await message.reply_text("⚠️ Channel join karein pehle!", reply_markup=get_must_join_keyboard())
        return
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
    
    if not await check_must_join(client, user_id):
        await message.reply_text("⚠️ Channel join karein pehle!", reply_markup=get_must_join_keyboard())
        return
    
    services = get_all_services()
    if not services:
        await message.reply_text("❌ Currently no services are available. Please ask Admin to add services!")
        return
        
    service_buttons = [[s] for s in services]
    service_buttons.append(["🔙 Back to Main"])
    user_states[user_id] = {"action": "select_service"}
    
    await message.reply_text(
        text="✨ <b>SELECT SERVICE BELOW:</b>",
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

@app.on_message(filters.text & filters.private & filters.regex("^🌐 Manage Countries$"))
async def manage_countries_cmd(client, message):
    if not is_admin(message.from_user.id): return
    countries = get_all_countries()
    
    inline_kb = []
    row = []
    for c in countries:
        flag = get_flag_from_country_name(c)
        row.append(InlineKeyboardButton(f"❌ {flag} {c}", callback_data=f"del_country_{c}"))
        if len(row) == 2:
            inline_kb.append(row)
            row = []
    if row:
        inline_kb.append(row)
        
    inline_kb.append([InlineKeyboardButton("➕ Add New Country Name", callback_data="add_country_prompt")])
    
    country_list_str = ", ".join([f"{get_flag_from_country_name(c)} {c}" for c in countries]) if countries else "None Added Yet"
    await message.reply_text(
        text=f"🌍 <b>Manage Country Names</b>\nCurrent Added Countries:\n{country_list_str}",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(inline_kb)
    )

@app.on_message(filters.text & filters.private & filters.regex("^➕ Add Number$"))
async def add_number_cmd(client, message):
    if not is_admin(message.from_user.id): return
    services = get_all_services()
    if not services:
        await message.reply_text("❌ Pehle Service add karein tab numbers add honge!")
        return
    
    service_buttons = [[s] for s in services]
    service_buttons.append(["🔙 Back to Main"])
    user_states[message.from_user.id] = {"action": "add_num_select_service"}
    
    await message.reply_text(
        "🛠️ <b>Select Service jisme numbers add karne hain:</b>",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True)
    )

@app.on_message(filters.text & filters.private & filters.regex("^🗑️ Delete Country Stock$"))
async def delete_country_stock_cmd(client, message):
    if not is_admin(message.from_user.id): return
    services = get_all_services()
    if not services:
        await message.reply_text("❌ No services found.")
        return
        
    service_buttons = [[s] for s in services]
    service_buttons.append(["🔙 Back to Main"])
    user_states[message.from_user.id] = {"action": "del_stock_select_service"}
    
    await message.reply_text(
        "🗑️ <b>Select Service jiska country stock delete karna hai:</b>",
        parse_mode=enums.ParseMode.HTML,
        reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True)
    )

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

# ================= CALLBACK HANDLER =================
@app.on_callback_query()
async def callback_handler(client, query: CallbackQuery):
    try:
        data = query.data
        user_id = query.from_user.id
        
        if data == "check_join_sub":
            if await check_must_join(client, user_id):
                await query.answer("✅ Verification Successful!", show_alert=True)
                await query.message.delete()
                await app.send_message(
                    user_id,
                    f"🎉 Welcome to <b>{BOT_NAME}</b>.",
                    parse_mode=enums.ParseMode.HTML,
                    reply_markup=get_main_keyboard(user_id)
                )
            else:
                await query.answer("❌ You haven't joined the channel yet!", show_alert=True)

        elif data == "add_country_prompt":
            if not is_admin(user_id): return
            user_states[user_id] = {"action": "add_new_country_name"}
            await query.message.reply_text("✏️ Enter Full Country Name (e.g., India, United States, Russia):")
            await query.answer()

        elif data.startswith("del_country_"):
            if not is_admin(user_id): return
            c_name = data.replace("del_country_", "", 1)
            db.countries.delete_one({"name": c_name})
            await query.answer(f"Deleted Country {c_name}", show_alert=True)
            await query.message.delete()

        elif data.startswith("delstock_"):
            parts = data.split("_", 2)
            service = parts[1]
            country = parts[2]
            
            deleted_count = db.numbers.delete_many({"service": service, "country": country}).deleted_count
            await query.answer(f"Deleted {deleted_count} numbers!", show_alert=True)
            await query.message.edit_text(f"🗑️ Successfully deleted all stock for <b>{service} ({country})</b>. Total removed: {deleted_count}", parse_mode=enums.ParseMode.HTML)

        elif data.startswith("addnum_cc_"):
            parts = data.split("_", 2)
            service = parts[1]
            country_name = parts[2]
            
            user_states[user_id] = {
                "action": "add_numbers_text",
                "service": service,
                "country": country_name
            }
            await query.message.reply_text(
                f"📁 Service: <b>{service}</b> | Country: <b>{country_name}</b>\n\nAb apni <b>.txt file</b> upload karo ya direct numbers paste karo!",
                parse_mode=enums.ParseMode.HTML
            )
            await query.answer()

        elif data.startswith("country_"):
            parts = data.split("_", 2)
            service = parts[1]
            country_name = parts[2]
            
            await query.answer("Fetching numbers...", show_alert=False)
            
            numbers, error = await allocate_three_numbers(user_id, service, country_name=country_name)
            if error:
                await query.message.edit_text(f"❌ {error}", parse_mode=enums.ParseMode.HTML)
                return
                
            nums_text = ""
            for num in numbers:
                flag = get_flag_from_number(num)
                clean = str(num).replace("+", "").strip()
                nums_text += f"{flag} <code>+{clean}</code>\n"
                
            controls_inline = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{service}_{country_name}"),
                    InlineKeyboardButton("🛡️ OTP Group", url=OTP_GROUP_LINK)
                ],
                [InlineKeyboardButton("❌ Close", callback_data="close_menu")]
            ])
            
            await query.message.edit_text(
                text=(
                    f"💬 <b>{service}</b>\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{nums_text}"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"👇 Tap on any number to copy instantly!"
                ),
                parse_mode=enums.ParseMode.HTML,
                reply_markup=controls_inline
            )

        elif data.startswith("change_"):
            parts = data.split("_", 2)
            service = parts[1]
            country_name = parts[2]
            
            await query.answer("Fetching new numbers...", show_alert=False)
            
            numbers, error = await allocate_three_numbers(user_id, service, country_name=country_name)
            if error:
                await query.message.edit_text(f"❌ {error}", parse_mode=enums.ParseMode.HTML)
                return
                
            nums_text = ""
            for num in numbers:
                flag = get_flag_from_number(num)
                clean = str(num).replace("+", "").strip()
                nums_text += f"{flag} <code>+{clean}</code>\n"
                
            controls_inline = InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("🔄 Change Number", callback_data=f"change_{service}_{country_name}"),
                    InlineKeyboardButton("🛡️ OTP Group", url=OTP_GROUP_LINK)
                ],
                [InlineKeyboardButton("❌ Close", callback_data="close_menu")]
            ])
            
            await query.message.edit_text(
                text=(
                    f"💬 <b>{service}</b>\n"
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

# ================= DOCUMENT & STATE PROCESSOR =================
@app.on_message(filters.document & filters.private)
async def document_handler(client, message):
    try:
        user_id = message.from_user.id
        if not is_admin(user_id): return
        if user_id not in user_states: return

        state = user_states[user_id]
        if state.get("action") == "add_numbers_text":
            service = state.get("service")
            country_name = state.get("country")
            user_states.pop(user_id, None)

            file_path = await message.download()
            added_count = 0
            
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines:
                        clean_num = line.replace("+", "").strip()
                        if clean_num.isdigit():
                            db.numbers.update_one(
                                {"number": clean_num},
                                {
                                    "$set": {
                                        "number": clean_num,
                                        "status": "available",
                                        "assigned_to": None,
                                        "service": service,
                                        "country": country_name,
                                        "otp_count": 0
                                    }
                                },
                                upsert=True
                            )
                            added_count += 1
            except Exception as e:
                print(f"File read error: {e}")

            await message.reply_text(
                f"✅ <b>TXT File Successfully Processed!</b>\n"
                f"• Service: <b>{service}</b>\n"
                f"• Country: <b>{country_name}</b>\n"
                f"• Total Added from File: <b>{added_count}</b> numbers",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=admin_keyboard
            )
    except Exception as ex:
        print(f"Doc Handler Error: {ex}")

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

        elif action == "add_new_country_name" and is_admin(user_id):
            user_states.pop(user_id, None)
            c_name = text.title()
            db.countries.update_one({"name": c_name}, {"$set": {"name": c_name}}, upsert=True)
            flag = get_flag_from_country_name(c_name)
            await message.reply_text(f"✅ Country <b>{flag} {c_name}</b> added successfully!", parse_mode=enums.ParseMode.HTML, reply_markup=admin_keyboard)

        elif action == "add_num_select_service" and is_admin(user_id):
            if text == "🔙 Back to Main":
                user_states.pop(user_id, None)
                await back_to_main(client, message)
                return
            
            service_name = text
            countries = get_all_countries()
            
            inline_kb = []
            row = []
            for c in countries:
                flag = get_flag_from_country_name(c)
                row.append(InlineKeyboardButton(f"{flag} {c}", callback_data=f"addnum_cc_{service_name}_{c}"))
                if len(row) == 2:
                    inline_kb.append(row)
                    row = []
            if row:
                inline_kb.append(row)
            
            user_states.pop(user_id, None)
            await message.reply_text(
                f"🌍 <b>Selected Service: {service_name}</b>\nAb country select karein jisme numbers add karne hain:",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_kb)
            )

        elif action == "add_numbers_text" and is_admin(user_id):
            service = state.get("service")
            country_name = state.get("country")
            user_states.pop(user_id, None)
            
            lines = text.split("\n")
            added_count = 0
            for line in lines:
                clean_num = line.replace("+", "").strip()
                if clean_num.isdigit():
                    db.numbers.update_one(
                        {"number": clean_num},
                        {
                            "$set": {
                                "number": clean_num,
                                "status": "available",
                                "assigned_to": None,
                                "service": service,
                                "country": country_name,
                                "otp_count": 0
                            }
                        },
                        upsert=True
                    )
                    added_count += 1
            
            await message.reply_text(
                f"✅ <b>Successfully Added Numbers!</b>\n"
                f"• Service: <b>{service}</b>\n"
                f"• Country: <b>{country_name}</b>\n"
                f"• Total Added: <b>{added_count}</b> numbers",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=admin_keyboard
            )

        elif action == "del_stock_select_service" and is_admin(user_id):
            if text == "🔙 Back to Main":
                user_states.pop(user_id, None)
                await back_to_main(client, message)
                return
                
            service_name = text
            countries = get_all_countries()
            
            inline_kb = []
            row = []
            for c in countries:
                flag = get_flag_from_country_name(c)
                row.append(InlineKeyboardButton(f"🗑️ {flag} {c}", callback_data=f"delstock_{service_name}_{c}"))
                if len(row) == 2:
                    inline_kb.append(row)
                    row = []
            if row:
                inline_kb.append(row)
            
            user_states.pop(user_id, None)
            await message.reply_text(
                f"🗑️ <b>Service: {service_name}</b>\nKis country ka stock poora delete karna hai select karein:",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_kb)
            )

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
                flag = get_flag_from_number(clean_num)
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

        elif action == "select_service":
            user_states.pop(user_id, None)
            if text == "🔙 Back to Main":
                await back_to_main(client, message)
                return
            
            countries = get_all_countries()
            inline_kb = []
            row = []
            for c in countries:
                flag = get_flag_from_country_name(c)
                row.append(InlineKeyboardButton(f"{flag} {c}", callback_data=f"country_{text}_{c}"))
                if len(row) == 2:
                    inline_kb.append(row)
                    row = []
            if row:
                inline_kb.append(row)
            
            inline_kb.append([InlineKeyboardButton("❌ Cancel", callback_data="close_menu")])
            
            await message.reply_text(
                text=f"🌍 <b>Select Country for {text}:</b>",
                parse_mode=enums.ParseMode.HTML,
                reply_markup=InlineKeyboardMarkup(inline_kb)
            )

    except Exception as ex:
        print(f"State Handler Error: {ex}")

# ================= STARTUP ENGINE =================
async def main():
    await app.start()
    print(f"🚀 {BOT_NAME} Engine Started Successfully!")
    asyncio.create_task(background_otp_checker())
    await asyncio.Event().wait()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
