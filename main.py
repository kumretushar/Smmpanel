import asyncio
import re
import json
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton, Document
from pymongo import MongoClient
import aiohttp
import io

# ---------- CONFIG ----------
API_ID = 30954859
API_HASH = "240537c89299fc2c94e8c78607229a21"
BOT_TOKEN = "8841502557:AAH7m1ezXQbK8DKHsGuY6T7H2IMPtRAeVq8"
GROUP_ID = -1002949251809
CHANNEL_ID = "@gmtusharxfiles"
OTP_GROUP_LINK = "https://t.me/trxxotp"

BOT_NAME = "𝗚𝗠𝘅𝗢𝗧𝗣 ✉️"

# ---------- MONGODB ----------
MONGO_URI = "mongodb://tusharkumarin74_db_user:star%40123@ac-zborjum-shard-00-00.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-01.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-02.7jv0uuq.mongodb.net:27017/?ssl=true&replicaSet=atlas-qnvkfj-shard-0&authSource=admin&appName=Cluster"

db_client = MongoClient(MONGO_URI)
db = db_client.numberx

ADMIN_IDS = [8430946490]

# ---------- CLIENT ----------
app = Client(
    "numberx_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=0,
    workers=100
)

# ---------- CACHE & STATES ----------
user_cache = {}
user_states = {}

def get_user_cached(user_id):
    if user_id in user_cache:
        return user_cache[user_id]
    user = db.users.find_one({"user_id": user_id})
    user_cache[user_id] = user
    return user

def clear_cache():
    user_cache.clear()

# ---------- FULL COUNTRIES ----------
COUNTRIES = {
    "93": {"flag": "🇦🇫", "name": "Afghanistan"},
    "355": {"flag": "🇦🇱", "name": "Albania"},
    "213": {"flag": "🇩🇿", "name": "Algeria"},
    "376": {"flag": "🇦🇩", "name": "Andorra"},
    "244": {"flag": "🇦🇴", "name": "Angola"},
    "54": {"flag": "🇦🇷", "name": "Argentina"},
    "374": {"flag": "🇦🇲", "name": "Armenia"},
    "61": {"flag": "🇦🇺", "name": "Australia"},
    "43": {"flag": "🇦🇹", "name": "Austria"},
    "994": {"flag": "🇦🇿", "name": "Azerbaijan"},
    "1242": {"flag": "🇧🇸", "name": "Bahamas"},
    "973": {"flag": "🇧🇭", "name": "Bahrain"},
    "880": {"flag": "🇧🇩", "name": "Bangladesh"},
    "375": {"flag": "🇧🇾", "name": "Belarus"},
    "32": {"flag": "🇧🇪", "name": "Belgium"},
    "501": {"flag": "🇧🇿", "name": "Belize"},
    "229": {"flag": "🇧🇯", "name": "Benin"},
    "975": {"flag": "🇧🇹", "name": "Bhutan"},
    "591": {"flag": "🇧🇴", "name": "Bolivia"},
    "387": {"flag": "🇧🇦", "name": "Bosnia"},
    "267": {"flag": "🇧🇼", "name": "Botswana"},
    "55": {"flag": "🇧🇷", "name": "Brazil"},
    "673": {"flag": "🇧🇳", "name": "Brunei"},
    "359": {"flag": "🇧🇬", "name": "Bulgaria"},
    "226": {"flag": "🇧🇫", "name": "Burkina Faso"},
    "257": {"flag": "🇧🇮", "name": "Burundi"},
    "855": {"flag": "🇰🇭", "name": "Cambodia"},
    "237": {"flag": "🇨🇲", "name": "Cameroon"},
    "1": {"flag": "🇨🇦", "name": "Canada"},
    "238": {"flag": "🇨🇻", "name": "Cape Verde"},
    "236": {"flag": "🇨🇫", "name": "Central African Republic"},
    "235": {"flag": "🇹🇩", "name": "Chad"},
    "56": {"flag": "🇨🇱", "name": "Chile"},
    "86": {"flag": "🇨🇳", "name": "China"},
    "57": {"flag": "🇨🇴", "name": "Colombia"},
    "269": {"flag": "🇰🇲", "name": "Comoros"},
    "242": {"flag": "🇨🇬", "name": "Congo"},
    "506": {"flag": "🇨🇷", "name": "Costa Rica"},
    "385": {"flag": "🇭🇷", "name": "Croatia"},
    "53": {"flag": "🇨🇺", "name": "Cuba"},
    "357": {"flag": "🇨🇾", "name": "Cyprus"},
    "420": {"flag": "🇨🇿", "name": "Czech Republic"},
    "45": {"flag": "🇩🇰", "name": "Denmark"},
    "253": {"flag": "🇩🇯", "name": "Djibouti"},
    "1767": {"flag": "🇩🇲", "name": "Dominica"},
    "1809": {"flag": "🇩🇴", "name": "Dominican Republic"},
    "593": {"flag": "🇪🇨", "name": "Ecuador"},
    "20": {"flag": "🇪🇬", "name": "Egypt"},
    "503": {"flag": "🇸🇻", "name": "El Salvador"},
    "240": {"flag": "🇬🇶", "name": "Equatorial Guinea"},
    "291": {"flag": "🇪🇷", "name": "Eritrea"},
    "372": {"flag": "🇪🇪", "name": "Estonia"},
    "251": {"flag": "🇪🇹", "name": "Ethiopia"},
    "679": {"flag": "🇫🇯", "name": "Fiji"},
    "358": {"flag": "🇫🇮", "name": "Finland"},
    "33": {"flag": "🇫🇷", "name": "France"},
    "241": {"flag": "🇬🇦", "name": "Gabon"},
    "220": {"flag": "🇬🇲", "name": "Gambia"},
    "995": {"flag": "🇬🇪", "name": "Georgia"},
    "49": {"flag": "🇩🇪", "name": "Germany"},
    "233": {"flag": "🇬🇭", "name": "Ghana"},
    "30": {"flag": "🇬🇷", "name": "Greece"},
    "502": {"flag": "🇬🇹", "name": "Guatemala"},
    "224": {"flag": "🇬🇳", "name": "Guinea"},
    "245": {"flag": "🇬🇼", "name": "Guinea-Bissau"},
    "592": {"flag": "🇬🇾", "name": "Guyana"},
    "509": {"flag": "🇭🇹", "name": "Haiti"},
    "504": {"flag": "🇭🇳", "name": "Honduras"},
    "36": {"flag": "🇭🇺", "name": "Hungary"},
    "354": {"flag": "🇮🇸", "name": "Iceland"},
    "91": {"flag": "🇮🇳", "name": "India"},
    "62": {"flag": "🇮🇩", "name": "Indonesia"},
    "98": {"flag": "🇮🇷", "name": "Iran"},
    "964": {"flag": "🇮🇶", "name": "Iraq"},
    "353": {"flag": "🇮🇪", "name": "Ireland"},
    "972": {"flag": "🇮🇱", "name": "Israel"},
    "39": {"flag": "🇮🇹", "name": "Italy"},
    "225": {"flag": "🇨🇮", "name": "Ivory Coast"},
    "81": {"flag": "🇯🇵", "name": "Japan"},
    "962": {"flag": "🇯🇴", "name": "Jordan"},
    "7": {"flag": "🇰🇿", "name": "Kazakhstan"},
    "254": {"flag": "🇰🇪", "name": "Kenya"},
    "686": {"flag": "🇰🇮", "name": "Kiribati"},
    "965": {"flag": "🇰🇼", "name": "Kuwait"},
    "996": {"flag": "🇰🇬", "name": "Kyrgyzstan"},
    "856": {"flag": "🇱🇦", "name": "Laos"},
    "371": {"flag": "🇱🇻", "name": "Latvia"},
    "961": {"flag": "🇱🇧", "name": "Lebanon"},
    "266": {"flag": "🇱🇸", "name": "Lesotho"},
    "231": {"flag": "🇱🇷", "name": "Liberia"},
    "218": {"flag": "🇱🇾", "name": "Libya"},
    "423": {"flag": "🇱🇮", "name": "Liechtenstein"},
    "370": {"flag": "🇱🇹", "name": "Lithuania"},
    "352": {"flag": "🇱🇺", "name": "Luxembourg"},
    "261": {"flag": "🇲🇬", "name": "Madagascar"},
    "265": {"flag": "🇲🇼", "name": "Malawi"},
    "60": {"flag": "🇲🇾", "name": "Malaysia"},
    "960": {"flag": "🇲🇻", "name": "Maldives"},
    "223": {"flag": "🇲🇱", "name": "Mali"},
    "356": {"flag": "🇲🇹", "name": "Malta"},
    "692": {"flag": "🇲🇭", "name": "Marshall Islands"},
    "222": {"flag": "🇲🇷", "name": "Mauritania"},
    "230": {"flag": "🇲🇺", "name": "Mauritius"},
    "52": {"flag": "🇲🇽", "name": "Mexico"},
    "691": {"flag": "🇫🇲", "name": "Micronesia"},
    "373": {"flag": "🇲🇩", "name": "Moldova"},
    "377": {"flag": "🇲🇨", "name": "Monaco"},
    "976": {"flag": "🇲🇳", "name": "Mongolia"},
    "382": {"flag": "🇲🇪", "name": "Montenegro"},
    "212": {"flag": "🇲🇦", "name": "Morocco"},
    "258": {"flag": "🇲🇿", "name": "Mozambique"},
    "95": {"flag": "🇲🇲", "name": "Myanmar"},
    "264": {"flag": "🇳🇦", "name": "Namibia"},
    "674": {"flag": "🇳🇷", "name": "Nauru"},
    "977": {"flag": "🇳🇵", "name": "Nepal"},
    "31": {"flag": "🇳🇱", "name": "Netherlands"},
    "64": {"flag": "🇳🇿", "name": "New Zealand"},
    "505": {"flag": "🇳🇮", "name": "Nicaragua"},
    "227": {"flag": "🇳🇪", "name": "Niger"},
    "234": {"flag": "🇳🇬", "name": "Nigeria"},
    "850": {"flag": "🇰🇵", "name": "North Korea"},
    "47": {"flag": "🇳🇴", "name": "Norway"},
    "968": {"flag": "🇴🇲", "name": "Oman"},
    "92": {"flag": "🇵🇰", "name": "Pakistan"},
    "680": {"flag": "🇵🇼", "name": "Palau"},
    "970": {"flag": "🇵🇸", "name": "Palestine"},
    "507": {"flag": "🇵🇦", "name": "Panama"},
    "675": {"flag": "🇵🇬", "name": "Papua New Guinea"},
    "595": {"flag": "🇵🇾", "name": "Paraguay"},
    "51": {"flag": "🇵🇪", "name": "Peru"},
    "63": {"flag": "🇵🇭", "name": "Philippines"},
    "48": {"flag": "🇵🇱", "name": "Poland"},
    "351": {"flag": "🇵🇹", "name": "Portugal"},
    "974": {"flag": "🇶🇦", "name": "Qatar"},
    "40": {"flag": "🇷🇴", "name": "Romania"},
    "7": {"flag": "🇷🇺", "name": "Russia"},
    "250": {"flag": "🇷🇼", "name": "Rwanda"},
    "685": {"flag": "🇼🇸", "name": "Samoa"},
    "378": {"flag": "🇸🇲", "name": "San Marino"},
    "966": {"flag": "🇸🇦", "name": "Saudi Arabia"},
    "221": {"flag": "🇸🇳", "name": "Senegal"},
    "381": {"flag": "🇷🇸", "name": "Serbia"},
    "248": {"flag": "🇸🇨", "name": "Seychelles"},
    "232": {"flag": "🇸🇱", "name": "Sierra Leone"},
    "65": {"flag": "🇸🇬", "name": "Singapore"},
    "421": {"flag": "🇸🇰", "name": "Slovakia"},
    "386": {"flag": "🇸🇮", "name": "Slovenia"},
    "677": {"flag": "🇸🇧", "name": "Solomon Islands"},
    "252": {"flag": "🇸🇴", "name": "Somalia"},
    "27": {"flag": "🇿🇦", "name": "South Africa"},
    "82": {"flag": "🇰🇷", "name": "South Korea"},
    "34": {"flag": "🇪🇸", "name": "Spain"},
    "94": {"flag": "🇱🇰", "name": "Sri Lanka"},
    "249": {"flag": "🇸🇩", "name": "Sudan"},
    "597": {"flag": "🇸🇷", "name": "Suriname"},
    "268": {"flag": "🇸🇿", "name": "Swaziland"},
    "46": {"flag": "🇸🇪", "name": "Sweden"},
    "41": {"flag": "🇨🇭", "name": "Switzerland"},
    "963": {"flag": "🇸🇾", "name": "Syria"},
    "886": {"flag": "🇹🇼", "name": "Taiwan"},
    "992": {"flag": "🇹🇯", "name": "Tajikistan"},
    "255": {"flag": "🇹🇿", "name": "Tanzania"},
    "66": {"flag": "🇹🇭", "name": "Thailand"},
    "228": {"flag": "🇹🇬", "name": "Togo"},
    "676": {"flag": "🇹🇴", "name": "Tonga"},
    "1868": {"flag": "🇹🇹", "name": "Trinidad and Tobago"},
    "216": {"flag": "🇹🇳", "name": "Tunisia"},
    "90": {"flag": "🇹🇷", "name": "Turkey"},
    "993": {"flag": "🇹🇲", "name": "Turkmenistan"},
    "688": {"flag": "🇹🇻", "name": "Tuvalu"},
    "256": {"flag": "🇺🇬", "name": "Uganda"},
    "380": {"flag": "🇺🇦", "name": "Ukraine"},
    "971": {"flag": "🇦🇪", "name": "United Arab Emirates"},
    "44": {"flag": "🇬🇧", "name": "United Kingdom"},
    "1": {"flag": "🇺🇸", "name": "United States"},
    "598": {"flag": "🇺🇾", "name": "Uruguay"},
    "998": {"flag": "🇺🇿", "name": "Uzbekistan"},
    "678": {"flag": "🇻🇺", "name": "Vanuatu"},
    "379": {"flag": "🇻🇦", "name": "Vatican City"},
    "58": {"flag": "🇻🇪", "name": "Venezuela"},
    "84": {"flag": "🇻🇳", "name": "Vietnam"},
    "967": {"flag": "🇾🇪", "name": "Yemen"},
    "260": {"flag": "🇿🇲", "name": "Zambia"},
    "263": {"flag": "🇿🇼", "name": "Zimbabwe"}
}

def get_country_info(code):
    if str(code).startswith('+'):
        code = str(code)[1:]
    code = str(code)
    if code in COUNTRIES:
        return COUNTRIES[code]
    for country_code, info in COUNTRIES.items():
        if code.startswith(country_code):
            return info
    return {"flag": "🏳️", "name": "Unknown"}

def mask_number(number):
    if len(number) <= 4:
        return number
    country_code = ""
    for i in range(1, min(5, len(number))):
        if number[i].isdigit():
            country_code += number[i]
        else:
            break
    country_code = "+" + country_code if country_code else ""
    last_4 = number[-4:] if len(number) >= 4 else number
    middle_len = len(number) - len(country_code) - 4
    masked = "x" * min(middle_len, 4) if middle_len > 0 else ""
    return f"{country_code}{masked}{last_4}"

# ---------- PANELS ----------
PANELS = [
    {
        "name": "KONEK",
        "url": "http://51.77.216.195/crapi/konek/viewstats",
        "token": "RFRXSjRSQmNccJFIWpN1e16XVIdYjGtlSGlphVVRUHpClnlginKV",
        "records": 20
    },
    {
        "name": "GM Panel",
        "url": "http://147.135.212.197/crapi/st/viewstats",
        "token": "SFBXRkFBUzSIiZZ8Y2FwSlqMb3yGkWOAi2lXW1JojFZbaFddaZRPdQ==",
        "records": 20
    }
]

# ---------- HELPERS ----------
def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_banned(user_id):
    user = get_user_cached(user_id)
    return user and user.get("is_banned", False)

def add_user(user_id, username, first_name):
    if not get_user_cached(user_id):
        db.users.insert_one({
            "user_id": user_id,
            "username": username,
            "first_name": first_name,
            "joined_date": datetime.now(),
            "is_banned": False,
            "used_numbers": [],
            "total_otp": 0,
            "numbers_allocated": 0
        })
        clear_cache()

def get_all_services():
    services_from_num = db.numbers.distinct("service")
    services_from_db = [s["name"] for s in db.services.find({}) if s.get("name")]
    all_srv = list(set(services_from_num + services_from_db))
    return [s for s in all_srv if s and s != "SYSTEM"]

# ---------- KEYBOARDS ----------
user_keyboard = ReplyKeyboardMarkup([
    ["📱 Get Number", "🔍 Search Number"],
    ["📊 Traffic Stats", "🆘 Support"],
    ["❓ Help", "ℹ️ About"]
], resize_keyboard=True)

admin_keyboard = ReplyKeyboardMarkup([
    ["📊 Admin Panel", "📢 Broadcast"],
    ["📈 Stats", "🔧 Manage Numbers"],
    ["👥 Users List", "🌍 Country Rank"],
    ["🔙 Back to Main"]
], resize_keyboard=True)

admin_panel_keyboard = ReplyKeyboardMarkup([
    ["➕ Add Number", "➖ Remove Number"],
    ["➕ Create Service", "➖ Remove Service"],
    ["🚫 Ban User", "✅ Unban User"],
    ["📋 Services", "📢 Broadcast"],
    ["📋 OTP Logs", "🔧 Force Join Settings"],
    ["🗑️ Delete Numbers", "🗑️ Delete Services"],
    ["🗑️ Delete Logs", "🔙 Back to Main"]
], resize_keyboard=True)

# ---------- ALLOCATE NUMBERS ----------
async def allocate_three_numbers(user_id, service="WhatsApp"):
    async with aiohttp.ClientSession() as session:
        async def fetch_panel(panel):
            try:
                async with session.get(panel["url"], headers={"Authorization": panel["token"]}) as resp:
                    if resp.status == 200:
                        return await resp.json()
            except:
                pass
            return None
        
        tasks = [fetch_panel(panel) for panel in PANELS]
        results = await asyncio.gather(*tasks)
        
        for data in results:
            if data and data.get("numbers"):
                numbers = data.get("numbers", [])
                for num in numbers[:10]:
                    if not db.numbers.find_one({"number": num}):
                        country_info = get_country_info(num)
                        db.numbers.insert_one({
                            "number": num,
                            "country": country_info["name"],
                            "country_code": num[:3] if num.startswith("+") else num[:3],
                            "flag": country_info["flag"],
                            "status": "available",
                            "assigned_to": None,
                            "otp_received": [],
                            "otp_count": 0,
                            "service": service
                        })
                break
    
    number_docs = list(db.numbers.find({"status": "available", "service": service}).limit(3))
    if len(number_docs) < 3:
        number_docs = list(db.numbers.find({"status": "available"}).limit(3))
        
    if len(number_docs) < 3:
        return None, f"Only {len(number_docs)} numbers available."
    
    numbers_list = []
    for doc in number_docs:
        db.numbers.update_one(
            {"_id": doc["_id"]},
            {"$set": {"status": "in_use", "assigned_to": user_id}}
        )
        numbers_list.append(doc["number"])
    
    db.users.update_one(
        {"user_id": user_id},
        {
            "$push": {"used_numbers": {"$each": numbers_list}},
            "$inc": {"numbers_allocated": 3}
        }
    )
    clear_cache()
    
    return numbers_list, None

def format_numbers(numbers, service):
    text = "━━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "📱 YOUR NUMBERS\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for num in numbers:
        info = get_country_info(num)
        text += f"{info['flag']} Number: {num}\n"
        text += f"📌 Service: {service}\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"\n⏳ Auto-Change in 2s...\n"
    text += f"🔄 New numbers incoming!\n\n"
    text += f"🔹 OTP Group: {OTP_GROUP_LINK}\n"
    text += "━━━━━━━━━━━━━━━━━━━━━━━"
    return text

# ---------- START ----------
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    
    username = message.from_user.username or "NoUsername"
    first_name = message.from_user.first_name or "User"
    add_user(user_id, username, first_name)
    
    if is_banned(user_id):
        await message.reply("🚫 You are banned. Contact admin.")
        return
    
    keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
    welcome_text = f"👑 Welcome Admin {first_name}!" if is_admin(user_id) else f"👋 Hello {first_name}!"
    
    await message.reply(
        f"{BOT_NAME}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{welcome_text}\n"
        f"📌 Choose an option below.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━",
        reply_markup=keyboard
    )

# ---------- BACK TO MAIN ----------
@app.on_message(filters.text & filters.private & filters.regex("^🔙 Back to Main$"))
async def back_to_main(client, message):
    user_id = message.from_user.id
    user_states.pop(user_id, None)
    keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
    await message.reply(
        f"✅ Main Menu\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 Choose an option below.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━",
        reply_markup=keyboard
    )

# ---------- USER BUTTONS ----------
@app.on_message(filters.text & filters.private & filters.regex("^📱 Get Number$"))
async def get_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        await message.reply("🚫 You are banned.")
        return
    
    services = get_all_services()
    if not services:
        services = ["WhatsApp", "Telegram"]
    
    service_buttons = []
    for s in services[:6]:
        service_buttons.append([s])
    service_buttons.append(["🔙 Back to Main"])
    
    user_states[user_id] = {"action": "select_service"}
    
    await message.reply(
        f"📱 SELECT SERVICE\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 Available: {', '.join(services)}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Choose a service:",
        reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True)
    )

@app.on_message(filters.text & filters.private & filters.regex("^🔍 Search Number$"))
async def search_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        await message.reply("🚫 You are banned.")
        return
    
    user_states[user_id] = {"action": "search_number"}
    await message.reply(
        f"🔍 SEARCH NUMBERS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send country code (e.g., 91, 1, 44):\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

@app.on_message(filters.text & filters.private & filters.regex("^📊 Traffic Stats$"))
async def traffic_stats(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        await message.reply("🚫 You are banned.")
        return
    
    total_otp = db.numbers.aggregate([{"$group": {"_id": None, "total": {"$sum": "$otp_count"}}}])
    total_otp = list(total_otp)
    total_otp = total_otp[0]["total"] if total_otp else 0
    
    pipeline = [
        {"$group": {"_id": "$country", "total_otp": {"$sum": "$otp_count"}}},
        {"$sort": {"total_otp": -1}},
        {"$limit": 10}
    ]
    results = list(db.numbers.aggregate(pipeline))
    
    if not results or total_otp == 0:
        await message.reply(
            f"📊 TRAFFIC STATS\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📭 No OTP data yet.\n\n"
            f"💡 Start using numbers to generate data!\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    stats = f"📊 LIVE TRAFFIC STATS\n"
    stats += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    stats += f"📊 Total OTPs: {total_otp}\n"
    stats += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    stats += f"🏆 COUNTRY RANKINGS\n"
    stats += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, doc in enumerate(results, 1):
        flag = get_country_info(doc["_id"])["flag"] if doc["_id"] != "UNKNOWN" else "🏳️"
        percentage = round((doc["total_otp"] / total_otp) * 100, 1) if total_otp > 0 else 0
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        stats += f"{medal} {flag} {doc['_id']}\n"
        stats += f"   📱 {doc['total_otp']} OTPs  •  {percentage}%\n"
        stats += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    stats += f"\n🔄 Updated: {datetime.now().strftime('%H:%M:%S')}\n"
    stats += f"━━━━━━━━━━━━━━━━━━━━━━━"
    await message.reply(stats)

@app.on_message(filters.text & filters.private & filters.regex("^🆘 Support$"))
async def support(client, message):
    await message.reply(
        f"🆘 SUPPORT CENTER\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Admin: @Amarstarx\n"
        f"📞 Contact: {ADMIN_IDS[0]}\n\n"
        f"⚡ Response: Within 1 hour\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

@app.on_message(filters.text & filters.private & filters.regex("^❓ Help$"))
async def help_cmd(client, message):
    await message.reply(
        f"❓ HOW TO USE\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 Get Number – Get 3 numbers at once\n"
        f"   ⏳ Auto-change in 2s\n\n"
        f"🔍 Search Number – Search by country\n"
        f"   📌 See available numbers\n\n"
        f"📊 Traffic Stats – Real-time OTP stats\n"
        f"   🏆 Country ranking\n"
        f"   📊 Percentage breakdown\n"
        f"   🔄 Live updates\n\n"
        f"🆘 Support – Contact admin\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

@app.on_message(filters.text & filters.private & filters.regex("^ℹ️ About$"))
async def about(client, message):
    await message.reply(
        f"ℹ️ ABOUT {BOT_NAME}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 Developer: @Amarstarx\n"
        f"🗄️ Database: Own🙂\n"
        f"⚡ Status: Online 24/7\n"
        f"💎 Version: Premium 4.0\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

# ---------- ADMIN BUTTONS DISPLAY ----------
@app.on_message(filters.text & filters.private & filters.regex("^📊 Admin Panel$"))
async def admin_panel(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    total_users = db.users.count_documents({})
    total_numbers = db.numbers.count_documents({})
    available = db.numbers.count_documents({"status": "available"})
    in_use = db.numbers.count_documents({"status": "in_use"})
    banned = db.users.count_documents({"is_banned": True})
    total_otp = db.numbers.aggregate([{"$group": {"_id": None, "total": {"$sum": "$otp_count"}}}])
    total_otp = list(total_otp)
    total_otp = total_otp[0]["total"] if total_otp else 0
    
    await message.reply(
        f"👑 ADMIN DASHBOARD\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Users: {total_users}\n"
        f"📱 Numbers: {total_numbers}\n"
        f"✅ Available: {available}\n"
        f"🔴 In Use: {in_use}\n"
        f"🚫 Banned: {banned}\n"
        f"🔑 OTPs: {total_otp}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━",
        reply_markup=admin_panel_keyboard
    )

@app.on_message(filters.text & filters.private & filters.regex("^📈 Stats$"))
async def stats_cmd(client, message):
    if not is_admin(message.from_user.id): return
    await admin_panel(client, message)

@app.on_message(filters.text & filters.private & filters.regex("^🔧 Manage Numbers$"))
async def manage_numbers(client, message):
    if not is_admin(message.from_user.id): return
    await message.reply(
        f"🔧 MANAGE NUMBERS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Use admin panel buttons:\n"
        f"➕ Add Number\n"
        f"➖ Remove Number\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

@app.on_message(filters.text & filters.private & filters.regex("^👥 Users List$"))
async def users_list(client, message):
    if not is_admin(message.from_user.id): return
    users = list(db.users.find({}).limit(20))
    if not users:
        await message.reply("👥 USERS LIST\n━━━━━━━━━━━━━━━━━━━━━━━\n📭 No users.")
        return
    
    text = f"👥 USERS LIST\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for u in users:
        status = "🚫 Banned" if u.get("is_banned") else "✅ Active"
        nums = len(u.get("used_numbers", []))
        otps = u.get("total_otp", 0)
        text += f"• {u['user_id']} – {u.get('first_name', 'Unknown')}\n"
        text += f"  📱 {nums} numbers • 🔑 {otps} OTPs • {status}\n"
        text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    await message.reply(text)

@app.on_message(filters.text & filters.private & filters.regex("^🌍 Country Rank$"))
async def country_rank(client, message):
    if not is_admin(message.from_user.id): return
    pipeline = [
        {"$group": {"_id": "$country", "total_otp": {"$sum": "$otp_count"}}},
        {"$sort": {"total_otp": -1}},
        {"$limit": 10}
    ]
    results = list(db.numbers.aggregate(pipeline))
    if not results:
        await message.reply("🌍 COUNTRY RANK\n━━━━━━━━━━━━━━━━━━━━━━━\n📊 No OTP data yet.")
        return
    
    total_otp = sum([r["total_otp"] for r in results])
    stats = f"🌍 COUNTRY RANKING\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for i, doc in enumerate(results, 1):
        flag = get_country_info(doc["_id"])["flag"] if doc["_id"] != "UNKNOWN" else "🏳️"
        percentage = round((doc["total_otp"] / total_otp) * 100, 1) if total_otp > 0 else 0
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        stats += f"{medal} {flag} {doc['_id']}\n   📱 {doc['total_otp']} OTPs • {percentage}%\n━━━━━━━━━━━━━━━━━━━━━━━\n"
    await message.reply(stats)

@app.on_message(filters.text & filters.private & filters.regex("^📋 Services$"))
async def manage_services(client, message):
    if not is_admin(message.from_user.id): return
    services_list = get_all_services()
            
    if not services_list:
        await message.reply("📋 SERVICES\n━━━━━━━━━━━━━━━━━━━━━━━\n📭 No services available.")
        return
    
    text = "📋 SERVICES\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for s in services_list:
        count = db.numbers.count_documents({"service": s})
        text += f"• {s} – {count} numbers\n"
    await message.reply(text)

@app.on_message(filters.text & filters.private & filters.regex("^📋 OTP Logs$"))
async def otp_logs(client, message):
    if not is_admin(message.from_user.id): return
    logs = list(db.otp_logs.find({}).sort("timestamp", -1).limit(20))
    if not logs:
        await message.reply("📋 OTP LOGS\n━━━━━━━━━━━━━━━━━━━━━━━\n📭 No OTP logs yet.")
        return
    
    text = "📋 OTP LOGS\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for i, log in enumerate(logs, 1):
        flag = log.get("flag", "🏳️")
        masked = log.get("masked_number", log.get("number", "Unknown"))
        otp = log.get("otp", "N/A")
        time = log.get("timestamp", datetime.now()).strftime('%H:%M:%S')
        text += f"{i}. {flag} {masked} → {otp} @ {time}\n   👤 {log.get('user_id', 'Unknown')}\n━━━━━━━━━━━━━━━━━━━━━━━\n"
    text += "\n📤 Export JSON: /export_otp_logs"
    await message.reply(text)

# ---------- ADMIN STATE TRIGGERS ----------
@app.on_message(filters.text & filters.private & filters.regex("^(📢 Broadcast|➕ Add Number|➖ Remove Number|➕ Create Service|➖ Remove Service|🚫 Ban User|✅ Unban User|🔧 Force Join Settings|🗑️ Delete Numbers|🗑️ Delete Services|🗑️ Delete Logs)$"))
async def admin_action_triggers(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    btn = message.text
    if btn == "📢 Broadcast":
        user_states[user_id] = {"action": "broadcast"}
        await message.reply("📢 Send the message you want to broadcast to all users:")
    elif btn == "➕ Add Number":
        user_states[user_id] = {"action": "add_num_step1"}
        await message.reply("➕ Send country code (e.g., 91, 1, 44):")
    elif btn == "➖ Remove Number":
        user_states[user_id] = {"action": "remove_number"}
        await message.reply("➖ Send number to remove (e.g. 911234567890):")
    elif btn == "➕ Create Service":
        user_states[user_id] = {"action": "create_service"}
        await message.reply("➕ Send new service name (e.g. Snapchat):")
    elif btn == "➖ Remove Service":
        user_states[user_id] = {"action": "remove_service"}
        await message.reply("➖ Send service name to remove:")
    elif btn == "🚫 Ban User":
        user_states[user_id] = {"action": "ban_user"}
        await message.reply("🚫 Send user ID to ban:")
    elif btn == "✅ Unban User":
        user_states[user_id] = {"action": "unban_user"}
        await message.reply("✅ Send user ID to unban:")
    elif btn == "🔧 Force Join Settings":
        user_states[user_id] = {"action": "force_join"}
        await message.reply(f"🔧 Current Channel: {CHANNEL_ID}\nSend new channel username (e.g., @newchannel) or /skip:")
    elif btn.startswith("🗑️ Delete"):
        target = btn.replace("🗑️ Delete ", "").lower()
        user_states[user_id] = {"action": f"delete_{target}"}
        await message.reply(f"⚠️ Type 'CONFIRM' to delete ALL {target}:")

# ---------- CENTRAL STATE PROCESSOR ----------
@app.on_message(filters.private & ~filters.command("start"))
async def central_state_handler(client, message):
    user_id = message.from_user.id
    text = message.text.strip() if message.text else ""

    # Catch 4-8 digit OTP input globally
    if text.isdigit() and 4 <= len(text) <= 8 and user_id not in user_states:
        user = get_user_cached(user_id)
        if user and user.get("used_numbers"):
            last_number = user["used_numbers"][-1]
            number_doc = db.numbers.find_one({"number": last_number})
            if number_doc:
                flag = number_doc.get("flag", "🏳️")
                country = number_doc.get("country", "Unknown")
                service = number_doc.get("service", "Unknown")
                db.numbers.update_one({"number": last_number}, {"$push": {"otp_received": text}, "$inc": {"otp_count": 1}})
                db.users.update_one({"user_id": user_id}, {"$inc": {"total_otp": 1}})
                db.otp_logs.insert_one({"number": last_number, "masked_number": mask_number(last_number), "otp": text, "country": country, "flag": flag, "service": service, "user_id": user_id, "timestamp": datetime.now()})
                clear_cache()
                try:
                    await client.send_message(GROUP_ID, f"🔑 OTP RECEIVED\n━━━━━━━━━━━━━━━━━━━━━━━\n📱 Number: {mask_number(last_number)}\n{flag} Country: {country}\n📌 Service: {service}\n🔐 OTP: {text}\n👤 User: {user_id}\n🕐 Time: {datetime.now().strftime('%H:%M:%S')}\n━━━━━━━━━━━━━━━━━━━━━━━")
                except: pass
                return

    if user_id not in user_states:
        return

    state = user_states[user_id]
    action = state.get("action")

    # ----- User State Actions -----
    if action == "select_service":
        user_states.pop(user_id, None)
        if text == "🔙 Back to Main":
            await back_to_main(client, message)
            return
        
        numbers, error = await allocate_three_numbers(user_id, text)
        if error:
            await message.reply(f"❌ {error}\n\n💡 Try again later or contact admin.", reply_markup=user_keyboard)
            return
        
        numbers_text = format_numbers(numbers, text)
        sent_msg = await message.reply(numbers_text, reply_markup=user_keyboard)
        await asyncio.sleep(2)
        
        for num in numbers:
            db.numbers.update_one({"number": num}, {"$set": {"status": "available", "assigned_to": None}})
            
        new_numbers, error2 = await allocate_three_numbers(user_id, text)
        if error2:
            await sent_msg.edit_text(f"⚠️ {error2}")
            return
        
        new_text = format_numbers(new_numbers, text).replace("⏳ Auto-Change in 2s...", "✅ Auto-Changed!")
        await sent_msg.edit_text(new_text)

    elif action == "search_number":
        user_states.pop(user_id, None)
        code = text.replace("+", "")
        available = list(db.numbers.find({"country_code": code, "status": "available"}).limit(10))
        if not available:
            await message.reply(f"❌ No numbers found for country code {code}")
        else:
            res = f"✅ AVAILABLE NUMBERS\n━━━━━━━━━━━━━━━━━━━━━━━\nCountry: {code}\nAvailable: {len(available)}\n━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            for n in available:
                res += f"{n.get('flag', '🏳️')} {n['number']} – {n.get('service', 'WhatsApp')}\n"
            await message.reply(res)

    # ----- Admin State Actions -----
    elif action == "broadcast" and is_admin(user_id):
        user_states.pop(user_id, None)
        users = db.users.find({})
        count = 0
        await message.reply("⏳ Broadcasting...")
        for u in users:
            try:
                await client.send_message(u["user_id"], f"📢 BROADCAST\n━━━━━━━━━━━━━━━━━━━━━━━\n{text}\n━━━━━━━━━━━━━━━━━━━━━━━")
                count += 1
                await asyncio.sleep(0.01)
            except: pass
        await message.reply(f"✅ Broadcast sent to {count} users.")

    elif action == "add_num_step1" and is_admin(user_id):
        code = text.replace("+", "")
        c_info = get_country_info(code)
        user_states[user_id] = {"action": "add_num_step2", "code": code, "name": c_info["name"], "flag": c_info["flag"]}
        await message.reply(f"✅ Country: {c_info['flag']} {c_info['name']} ({code})\n\n📤 Send .txt file OR type numbers (one per line):")

    elif action == "add_num_step2" and is_admin(user_id):
        numbers = []
        if message.document and message.document.file_name.endswith('.txt'):
            file_path = await client.download_media(message.document)
            with open(file_path, 'r', encoding='utf-8') as f:
                numbers = [line.strip() for line in f.read().split('\n') if line.strip()]
        elif message.text:
            numbers = [line.strip() for line in message.text.split('\n') if line.strip()]

        if not numbers:
            await message.reply("❌ No numbers found in input. Try again.")
            user_states.pop(user_id, None)
            return

        user_states[user_id]["numbers"] = numbers
        user_states[user_id]["action"] = "add_num_step3"

        # Dynamically load existing categories + option to create new
        existing_srv = get_all_services()
        srv_buttons = [[s] for s in existing_srv]
        
        reply_markup = ReplyKeyboardMarkup(srv_buttons, resize_keyboard=True) if srv_buttons else None
        
        await message.reply(
            f"✅ {len(numbers)} numbers received!\n━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"🏷️ **Select Category/Service** below OR **type a new category name** directly:\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━",
            reply_markup=reply_markup
        )

    elif action == "add_num_step3" and is_admin(user_id):
        if not text:
            await message.reply("❌ Category name cannot be empty. Type or select a category name:")
            return

        service = text
        code = state["code"]
        c_name = state["name"]
        flag = state["flag"]
        numbers = state["numbers"]
        
        # Save new category to db.services if it doesn't exist
        if not db.services.find_one({"name": service}):
            db.services.insert_one({"name": service, "created_at": datetime.now()})
            
        added = 0
        for num in numbers:
            if num and not db.numbers.find_one({"number": num}):
                db.numbers.insert_one({
                    "number": num,
                    "country": c_name,
                    "country_code": code,
                    "flag": flag,
                    "service": service,
                    "status": "available",
                    "assigned_to": None,
                    "otp_received": [],
                    "otp_count": 0
                })
                added += 1

        user_states.pop(user_id, None)
        await message.reply(
            f"✅ Success!\n━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📁 Category: {service}\n"
            f"📱 Numbers Added: {added}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━",
            reply_markup=admin_panel_keyboard
        )

    elif action == "remove_number" and is_admin(user_id):
        user_states.pop(user_id, None)
        res = db.numbers.delete_one({"number": text})
        await message.reply(f"✅ {text} removed." if res.deleted_count else f"❌ {text} not found.")

    elif action == "create_service" and is_admin(user_id):
        user_states.pop(user_id, None)
        if not db.services.find_one({"name": text}):
            db.services.insert_one({"name": text, "created_at": datetime.now()})
        await message.reply(f"✅ Category '{text}' created!")

    elif action == "remove_service" and is_admin(user_id):
        user_states.pop(user_id, None)
        db.services.delete_one({"name": text})
        cnt = db.numbers.delete_many({"service": text}).deleted_count
        await message.reply(f"✅ Category '{text}' removed ({cnt} numbers deleted).")

    elif action == "ban_user" and is_admin(user_id):
        user_states.pop(user_id, None)
        if text.isdigit():
            db.users.update_one({"user_id": int(text)}, {"$set": {"is_banned": True}})
            await message.reply(f"✅ User {text} banned.")
        else: await message.reply("❌ Invalid user ID.")

    elif action == "unban_user" and is_admin(user_id):
        user_states.pop(user_id, None)
        if text.isdigit():
            db.users.update_one({"user_id": int(text)}, {"$set": {"is_banned": False}})
            await message.reply(f"✅ User {text} unbanned.")
        else: await message.reply("❌ Invalid user ID.")

    elif action == "force_join" and is_admin(user_id):
        user_states.pop(user_id, None)
        if text != "/skip" and text.startswith("@"):
            global CHANNEL_ID
            CHANNEL_ID = text
            db.settings.update_one({"_id": "force_join"}, {"$set": {"channel": text}}, upsert=True)
            await message.reply(f"✅ Channel updated to {text}")
        else:
            await message.reply("❌ Cancelled.")

    elif action.startswith("delete_") and is_admin(user_id):
        target = action.replace("delete_", "")
        user_states.pop(user_id, None)
        if text == "CONFIRM":
            if target == "numbers": db.numbers.delete_many({})
            elif target == "services": db.services.delete_many({})
            elif target == "logs": db.otp_logs.delete_many({})
            await message.reply(f"✅ All {target} deleted successfully.")
        else:
            await message.reply("❌ Cancelled.")

# ---------- EXPORT OTP LOGS ----------
@app.on_message(filters.command("export_otp_logs") & filters.private)
async def export_otp_logs(client, message):
    if not is_admin(message.from_user.id): return
    logs = list(db.otp_logs.find({}, {"_id": 0}).sort("timestamp", -1))
    if not logs:
        await message.reply("📭 No OTP logs to export.")
        return
    for log in logs:
        if "timestamp" in log: log["timestamp"] = log["timestamp"].isoformat()
    
    with open("otp_logs.json", "w") as f:
        f.write(json.dumps(logs, indent=2))
    await message.reply_document(document="otp_logs.json", caption=f"📊 Total: {len(logs)} entries")

# ---------- RUN ----------
print(f"🚀 {BOT_NAME} Starting...")
app.run()
