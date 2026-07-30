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

# ---------- CACHE ----------
user_cache = {}

def get_user_cached(user_id):
    if user_id in user_cache:
        return user_cache[user_id]
    user = db.users.find_one({"user_id": user_id})
    user_cache[user_id] = user
    return user

def clear_cache():
    user_cache.clear()

# ---------- FULL COUNTRIES (WITHOUT + DETECTION) ----------
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
    # Remove '+' if present
    if code.startswith('+'):
        code = code[1:]
    
    # Try exact match
    if code in COUNTRIES:
        return COUNTRIES[code]
    
    # Try partial match (for numbers like 22373838399 -> 223)
    for country_code, info in COUNTRIES.items():
        if code.startswith(country_code):
            return info
    
    return {"flag": "🏳️", "name": "Unknown"}

def mask_number(number):
    if len(number) <= 4:
        return number
    country_code = ""
    # Extract country code without +
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
    
    number_docs = list(db.numbers.find({"status": "available"}).limit(3))
    
    if len(number_docs) < 3:
        return None, f"❌ Only {len(number_docs)} numbers available."
    
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
    username = message.from_user.username or "NoUsername"
    first_name = message.from_user.first_name or "User"
    
    add_user(user_id, username, first_name)
    
    if is_banned(user_id):
        await message.reply("🚫 You are banned. Contact admin.")
        return
    
    if is_admin(user_id):
        keyboard = admin_keyboard
        welcome_text = f"👑 Welcome Admin {first_name}!"
    else:
        keyboard = user_keyboard
        welcome_text = f"👋 Hello {first_name}!"
    
    await message.reply(
        f"{BOT_NAME}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"{welcome_text}\n"
        f"📌 Choose an option below.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━",
        reply_markup=keyboard
    )

# ---------- BACK TO MAIN ----------
@app.on_message(filters.text & filters.private & filters.regex("🔙 Back to Main"))
async def back_to_main(client, message):
    user_id = message.from_user.id
    keyboard = user_keyboard if is_admin(user_id) else user_keyboard
    await message.reply(
        f"✅ Main Menu\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 Choose an option below.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━",
        reply_markup=keyboard
    )

# ---------- ADMIN PANEL ----------
@app.on_message(filters.text & filters.private & filters.regex("📊 Admin Panel"))
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

# ---------- SERVICES LIST ----------
@app.on_message(filters.text & filters.private & filters.regex("📋 Services"))
async def manage_services(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    services_from_numbers = db.numbers.distinct("service")
    services_from_db = db.services.find({})
    services_list = []
    
    for s in services_from_db:
        if s.get("name") and s.get("name") != "SYSTEM":
            services_list.append(s.get("name"))
    
    for s in services_from_numbers:
        if s and s != "SYSTEM" and s not in services_list:
            services_list.append(s)
    
    if not services_list:
        await message.reply(
            f"📋 SERVICES\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📭 No services available.\n\n"
            f"💡 Use 'Create Service' to add new.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    text = f"📋 SERVICES\n"
    text += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for s in services_list:
        if s and s != "SYSTEM":
            count = db.numbers.count_documents({"service": s})
            text += f"• {s} – {count} numbers\n"
    text += f"\n━━━━━━━━━━━━━━━━━━━━━━━\n"
    text += f"💡 Use 'Create Service' to add new.\n"
    text += f"💡 Use 'Remove Service' to delete.\n"
    text += f"━━━━━━━━━━━━━━━━━━━━━━━"
    await message.reply(text)

# ---------- CREATE SERVICE (FIXED) ----------
@app.on_message(filters.text & filters.private & filters.regex("➕ Create Service"))
async def create_service(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"➕ CREATE SERVICE\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send new service name:\n"
        f"Example: Snapchat, Twitter, etc.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def create_handler(client, msg):
        service = msg.text.strip()
        
        if not service:
            await msg.reply("❌ Service name cannot be empty.")
            app.remove_handler(create_handler)
            return
        
        # Check if service exists
        existing = db.numbers.find_one({"service": service})
        existing_service = db.services.find_one({"name": service})
        
        if existing or existing_service:
            await msg.reply(f"❌ Service '{service}' already exists.")
            app.remove_handler(create_handler)
            return
        
        # ✅ CREATE SERVICE IN BOTH COLLECTIONS
        db.services.insert_one({"name": service, "created_at": datetime.now()})
        
        # Also add a dummy entry to numbers collection so service shows up immediately
        db.numbers.insert_one({
            "number": "DUMMY_" + service,
            "country": "SYSTEM",
            "country_code": "0",
            "flag": "🏳️",
            "service": service,
            "status": "available",
            "assigned_to": None,
            "otp_received": [],
            "otp_count": 0
        })
        # Remove dummy after 1 second
        asyncio.create_task(remove_dummy(service))
        
        await msg.reply(
            f"✅ SERVICE CREATED\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Service: {service}\n"
            f"📊 Status: Active\n"
            f"📱 Numbers: 0\n\n"
            f"💡 Now use 'Add Number' to add numbers.\n"
            f"💡 Use '📋 Services' to see all services.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        app.remove_handler(create_handler)

async def remove_dummy(service):
    await asyncio.sleep(1)
    db.numbers.delete_one({"number": "DUMMY_" + service})

# ---------- REMOVE SERVICE ----------
@app.on_message(filters.text & filters.private & filters.regex("➖ Remove Service"))
async def remove_service(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    services_from_numbers = db.numbers.distinct("service")
    services_from_db = db.services.find({})
    services_list = []
    
    for s in services_from_db:
        if s.get("name") and s.get("name") != "SYSTEM":
            services_list.append(s.get("name"))
    
    for s in services_from_numbers:
        if s and s != "SYSTEM" and s not in services_list:
            services_list.append(s)
    
    if not services_list:
        await message.reply(
            f"❌ NO SERVICES\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"No services available to remove.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    service_list_text = "\n".join([f"• {s}" for s in services_list])
    await message.reply(
        f"➖ REMOVE SERVICE\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 Available Services:\n{service_list_text}\n\n"
        f"Send service name to remove:\n"
        f"⚠️ This will delete ALL numbers in this service!\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def remove_handler(client, msg):
        service = msg.text.strip()
        
        if not service:
            await msg.reply("❌ Service name cannot be empty.")
            app.remove_handler(remove_handler)
            return
        
        count = db.numbers.count_documents({"service": service})
        service_exists = db.services.find_one({"name": service})
        
        if count == 0 and not service_exists:
            await msg.reply(f"❌ Service '{service}' not found.")
            app.remove_handler(remove_handler)
            return
        
        if count > 0:
            db.numbers.delete_many({"service": service})
        
        if service_exists:
            db.services.delete_one({"name": service})
        
        await msg.reply(
            f"✅ SERVICE REMOVED\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📌 Service: {service}\n"
            f"📱 Numbers Deleted: {count}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        app.remove_handler(remove_handler)

# ---------- DELETE NUMBERS (INDIVIDUAL) ----------
@app.on_message(filters.text & filters.private & filters.regex("🗑️ Delete Numbers"))
async def delete_numbers(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    total = db.numbers.count_documents({})
    await message.reply(
        f"🗑️ DELETE NUMBERS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📱 Total Numbers: {total}\n\n"
        f"Send 'CONFIRM' to delete ALL numbers.\n"
        f"Send /cancel to cancel.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def confirm_handler(client, msg):
        text = msg.text.strip()
        
        if text == "/cancel":
            await msg.reply("❌ Cancelled.")
            app.remove_handler(confirm_handler)
            return
        
        if text != "CONFIRM":
            await msg.reply("❌ Send 'CONFIRM' to proceed or /cancel to cancel.")
            return
        
        count = db.numbers.count_documents({})
        db.numbers.delete_many({})
        
        await msg.reply(
            f"✅ NUMBERS DELETED\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 Numbers Deleted: {count}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        app.remove_handler(confirm_handler)

# ---------- DELETE SERVICES (INDIVIDUAL) ----------
@app.on_message(filters.text & filters.private & filters.regex("🗑️ Delete Services"))
async def delete_services(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    total = db.services.count_documents({})
    await message.reply(
        f"🗑️ DELETE SERVICES\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📋 Total Services: {total}\n\n"
        f"Send 'CONFIRM' to delete ALL services.\n"
        f"Send /cancel to cancel.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def confirm_handler(client, msg):
        text = msg.text.strip()
        
        if text == "/cancel":
            await msg.reply("❌ Cancelled.")
            app.remove_handler(confirm_handler)
            return
        
        if text != "CONFIRM":
            await msg.reply("❌ Send 'CONFIRM' to proceed or /cancel to cancel.")
            return
        
        count = db.services.count_documents({})
        db.services.delete_many({})
        
        await msg.reply(
            f"✅ SERVICES DELETED\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 Services Deleted: {count}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        app.remove_handler(confirm_handler)

# ---------- DELETE LOGS (INDIVIDUAL) ----------
@app.on_message(filters.text & filters.private & filters.regex("🗑️ Delete Logs"))
async def delete_logs(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    total = db.otp_logs.count_documents({})
    await message.reply(
        f"🗑️ DELETE LOGS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 Total OTP Logs: {total}\n\n"
        f"Send 'CONFIRM' to delete ALL logs.\n"
        f"Send /cancel to cancel.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def confirm_handler(client, msg):
        text = msg.text.strip()
        
        if text == "/cancel":
            await msg.reply("❌ Cancelled.")
            app.remove_handler(confirm_handler)
            return
        
        if text != "CONFIRM":
            await msg.reply("❌ Send 'CONFIRM' to proceed or /cancel to cancel.")
            return
        
        count = db.otp_logs.count_documents({})
        db.otp_logs.delete_many({})
        
        await msg.reply(
            f"✅ LOGS DELETED\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 Logs Deleted: {count}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        app.remove_handler(confirm_handler)

# ---------- ADD NUMBER (FIXED) ----------
add_number_step = {}

@app.on_message(filters.text & filters.private & filters.regex("➕ Add Number"))
async def add_number_start(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    add_number_step[user_id] = {"step": "country"}
    
    await message.reply(
        f"➕ ADD NUMBER\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send country code (e.g., 91, 1, 44):\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

@app.on_message(filters.private & ~filters.command("start"))
async def add_number_handler(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    if user_id not in add_number_step:
        return
    
    step = add_number_step[user_id].get("step")
    
    # Step 1: Country code
    if step == "country":
        # Check if it's a document
        if message.document:
            await message.reply("❌ First send country code, then file.")
            return
        
        country_code = message.text.strip() if message.text else None
        if not country_code:
            await message.reply("❌ Send country code.")
            return
        
        # Remove '+' if present
        if country_code.startswith('+'):
            country_code = country_code[1:]
        
        country_info = get_country_info(country_code)
        flag = country_info["flag"]
        country_name = country_info["name"]
        
        add_number_step[user_id]["country_code"] = country_code
        add_number_step[user_id]["country_name"] = country_name
        add_number_step[user_id]["flag"] = flag
        add_number_step[user_id]["step"] = "numbers"
        
        await message.reply(
            f"✅ Country: {flag} {country_name} ({country_code})\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📤 Send .txt file OR\n"
            f"📝 Type numbers (one per line):\n"
            f"Example:\n"
            f"911234567890\n"
            f"44234567890\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    # Step 2: Numbers (TXT or Text)
    if step == "numbers":
        numbers = []
        
        # Check if it's a document (TXT file)
        if message.document:
            file = message.document
            if file.file_name.endswith('.txt'):
                await message.reply("⏳ Downloading file...")
                file_path = await client.download_media(file)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        numbers = [line.strip() for line in content.split('\n') if line.strip()]
                    await message.reply(f"✅ Extracted {len(numbers)} numbers from {file.file_name}.")
                except Exception as e:
                    await message.reply(f"❌ Error reading file: {e}")
                    add_number_step.pop(user_id, None)
                    return
            else:
                await message.reply("❌ Please send a .txt file.")
                return
        
        # Check if it's text
        elif message.text:
            numbers = [line.strip() for line in message.text.split('\n') if line.strip()]
        
        else:
            await message.reply("❌ Send text or .txt file.")
            add_number_step.pop(user_id, None)
            return
        
        if not numbers:
            await message.reply("❌ No numbers found.")
            add_number_step.pop(user_id, None)
            return
        
        # Get all services
        services = db.numbers.distinct("service")
        service_list = db.services.find({})
        for s in service_list:
            if s.get("name") not in services and s.get("name") != "SYSTEM":
                services.append(s.get("name"))
        services = [s for s in services if s and s != "SYSTEM"]
        
        if not services:
            await message.reply(
                f"❌ No services available.\n"
                f"💡 Use 'Create Service' first.\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━"
            )
            add_number_step.pop(user_id, None)
            return
        
        add_number_step[user_id]["numbers"] = numbers
        add_number_step[user_id]["step"] = "service"
        
        service_buttons = []
        for s in services[:4]:
            service_buttons.append([s])
        service_buttons.append(["Custom Service", "🔙 Back to Main"])
        
        await message.reply(
            f"✅ {len(numbers)} numbers detected.\n\n"
            f"📌 Available services: {', '.join(services)}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Select service:",
            reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True)
        )
        return
    
    # Step 3: Service selection
    if step == "service":
        service = message.text.strip()
        
        if service == "🔙 Back to Main":
            add_number_step.pop(user_id, None)
            await back_to_main(client, message)
            return
        
        if service == "Custom Service":
            await message.reply("Send custom service name:")
            add_number_step[user_id]["step"] = "custom_service"
            return
        
        # Save numbers to DB
        country_code = add_number_step[user_id]["country_code"]
        country_name = add_number_step[user_id]["country_name"]
        flag = add_number_step[user_id]["flag"]
        numbers = add_number_step[user_id]["numbers"]
        
        added = 0
        for num in numbers:
            if num and not db.numbers.find_one({"number": num}):
                db.numbers.insert_one({
                    "number": num,
                    "country": country_name,
                    "country_code": country_code,
                    "flag": flag,
                    "service": service,
                    "status": "available",
                    "assigned_to": None,
                    "otp_received": [],
                    "otp_count": 0
                })
                added += 1
        
        add_number_step.pop(user_id, None)
        
        await message.reply(
            f"✅ Added {added} numbers to '{service}'.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Country: {flag} {country_name}\n"
            f"Service: {service}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    # Step 4: Custom service name
    if step == "custom_service":
        service = message.text.strip()
        if not service:
            await message.reply("❌ Service name cannot be empty.")
            return
        
        # Check if service exists
        existing = db.numbers.find_one({"service": service})
        existing_service = db.services.find_one({"name": service})
        if existing or existing_service:
            await message.reply(f"❌ Service '{service}' already exists.")
            add_number_step.pop(user_id, None)
            return
        
        # Create service
        db.services.insert_one({"name": service, "created_at": datetime.now()})
        
        # Save numbers
        country_code = add_number_step[user_id]["country_code"]
        country_name = add_number_step[user_id]["country_name"]
        flag = add_number_step[user_id]["flag"]
        numbers = add_number_step[user_id]["numbers"]
        
        added = 0
        for num in numbers:
            if num and not db.numbers.find_one({"number": num}):
                db.numbers.insert_one({
                    "number": num,
                    "country": country_name,
                    "country_code": country_code,
                    "flag": flag,
                    "service": service,
                    "status": "available",
                    "assigned_to": None,
                    "otp_received": [],
                    "otp_count": 0
                })
                added += 1
        
        add_number_step.pop(user_id, None)
        
        await message.reply(
            f"✅ Service '{service}' created!\n"
            f"✅ Added {added} numbers.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"Country: {flag} {country_name}\n"
            f"Service: {service}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )

# ---------- GET NUMBER ----------
@app.on_message(filters.text & filters.private & filters.regex("📱 Get Number"))
async def get_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        await message.reply("🚫 You are banned.")
        return
    
    services = db.numbers.distinct("service")
    service_list = db.services.find({})
    for s in service_list:
        if s.get("name") not in services and s.get("name") != "SYSTEM":
            services.append(s.get("name"))
    services = [s for s in services if s and s != "SYSTEM"]
    
    if not services:
        await message.reply(
            f"📱 GET NUMBER\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"❌ No services available.\n\n"
            f"💡 Contact admin to create a service.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    service_buttons = []
    for s in services[:4]:
        service_buttons.append([s])
    service_buttons.append(["🔙 Back to Main"])
    
    await message.reply(
        f"📱 SELECT SERVICE\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 Available: {', '.join(services)}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Choose a service:",
        reply_markup=ReplyKeyboardMarkup(service_buttons, resize_keyboard=True)
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def service_handler(client, msg):
        service = msg.text.strip()
        
        if service == "🔙 Back to Main":
            await back_to_main(client, msg)
            app.remove_handler(service_handler)
            return
        
        numbers, error = await allocate_three_numbers(user_id, service)
        
        if error:
            await msg.reply(f"❌ {error}\n\n💡 Try again later or contact admin.")
            app.remove_handler(service_handler)
            return
        
        numbers_text = format_numbers(numbers, service)
        sent_msg = await msg.reply(numbers_text)
        
        await asyncio.sleep(2)
        
        for num in numbers:
            db.numbers.update_one(
                {"number": num},
                {"$set": {"status": "available", "assigned_to": None}}
            )
        
        new_numbers, error2 = await allocate_three_numbers(user_id, service)
        
        if error2:
            await sent_msg.edit_text(f"⚠️ {error2}")
            app.remove_handler(service_handler)
            return
        
        new_text = format_numbers(new_numbers, service)
        new_text = new_text.replace("⏳ Auto-Change in 2s...", "✅ Auto-Changed!")
        await sent_msg.edit_text(new_text)
        
        app.remove_handler(service_handler)

# ---------- OTP CATCH ----------
@app.on_message(filters.private & filters.text & filters.regex(r'^\d{4,8}$') & ~filters.command("start"))
async def catch_otp(client, message):
    user_id = message.from_user.id
    text = message.text
    
    user = get_user_cached(user_id)
    if not user or not user.get("used_numbers"):
        return
    
    last_number = user["used_numbers"][-1] if user["used_numbers"] else None
    if not last_number:
        return
    
    number_doc = db.numbers.find_one({"number": last_number})
    if not number_doc:
        return
    
    flag = number_doc.get("flag", "🏳️")
    country = number_doc.get("country", "Unknown")
    service = number_doc.get("service", "Unknown")
    
    db.numbers.update_one(
        {"number": last_number},
        {"$push": {"otp_received": text}, "$inc": {"otp_count": 1}}
    )
    db.users.update_one(
        {"user_id": user_id},
        {"$inc": {"total_otp": 1}}
    )
    
    db.otp_logs.insert_one({
        "number": last_number,
        "masked_number": mask_number(last_number),
        "otp": text,
        "country": country,
        "flag": flag,
        "service": service,
        "user_id": user_id,
        "timestamp": datetime.now()
    })
    
    clear_cache()
    
    masked = mask_number(last_number)
    
    try:
        await client.send_message(
            GROUP_ID,
            f"🔑 OTP RECEIVED\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📱 Number: {masked}\n"
            f"{flag} Country: {country}\n"
            f"📌 Service: {service}\n"
            f"🔐 OTP: {text}\n"
            f"👤 User: {user_id}\n"
            f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
    except:
        pass

# ---------- TRAFFIC STATS ----------
@app.on_message(filters.text & filters.private & filters.regex("📊 Traffic Stats"))
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

# ---------- SEARCH ----------
@app.on_message(filters.text & filters.private & filters.regex("🔍 Search Number"))
async def search_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        await message.reply("🚫 You are banned.")
        return
    
    await message.reply(
        f"🔍 SEARCH NUMBERS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send country code (e.g., 91, 1, 44):\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def search_handler(client, msg):
        code = msg.text.strip()
        if code.startswith('+'):
            code = code[1:]
        
        available = list(db.numbers.find({"country_code": code, "status": "available"}).limit(10))
        
        if not available:
            await msg.reply(f"❌ No numbers found for {code}\n\n💡 Try another country code.")
        else:
            text = f"✅ AVAILABLE NUMBERS\n"
            text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            text += f"Country: {code}\n"
            text += f"Available: {len(available)}\n"
            text += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            for n in available:
                flag = n.get("flag", "🏳️")
                service = n.get("service", "WhatsApp")
                text += f"{flag} {n['number']} – {service}\n"
            text += f"\n💡 Click Get Number to claim!\n"
            text += f"━━━━━━━━━━━━━━━━━━━━━━━"
            await msg.reply(text)
        app.remove_handler(search_handler)

# ---------- SUPPORT ----------
@app.on_message(filters.text & filters.private & filters.regex("🆘 Support"))
async def support(client, message):
    await message.reply(
        f"🆘 SUPPORT CENTER\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 Admin: @Amarstarx\n"
        f"📞 Contact: {ADMIN_IDS[0]}\n\n"
        f"⚡ Response: Within 1 hour\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

# ---------- HELP ----------
@app.on_message(filters.text & filters.private & filters.regex("❓ Help"))
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
        f"🆘 Support – Contact admin\n\n"
        f"💎 Premium Features:\n"
        f"✅ 3 Numbers at once\n"
        f"✅ Auto-change in 2s\n"
        f"✅ Direct OTP Group\n"
        f"✅ Real-time Traffic Stats\n"
        f"✅ User Isolation\n"
        f"✅ Service Management\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

# ---------- ABOUT ----------
@app.on_message(filters.text & filters.private & filters.regex("ℹ️ About"))
async def about(client, message):
    await message.reply(
        f"ℹ️ ABOUT {BOT_NAME}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👨‍💻 Developer: @Amarstarx\n"
        f"🗄️ Database: Own😛\n"
        f"⚡ Status: Online 24/7\n"
        f"💎 Version: Premium 4.0\n\n"
        f"✅ 3 Numbers at once\n"
        f"✅ Auto-change in 2s\n"
        f"✅ Direct OTP Group\n"
        f"✅ Real-time Traffic Stats\n"
        f"✅ User Isolation\n"
        f"✅ Service Management\n"
        f"✅ Admin Panel\n"
        f"✅ Broadcast System\n"
        f"✅ OTP Logs (Admin)\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

# ---------- OTP GROUP ----------
@app.on_message(filters.text & filters.private & filters.regex("📢 OTP Group"))
async def otp_group(client, message):
    await message.reply(
        f"📢 OTP GROUP\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"🔥 Join now to receive OTPs!\n\n"
        f"🚀 Click Here: {OTP_GROUP_LINK}\n\n"
        f"💡 All OTPs forwarded here\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━",
        disable_web_page_preview=True
    )

# ---------- REMOVE NUMBER ----------
@app.on_message(filters.text & filters.private & filters.regex("➖ Remove Number"))
async def remove_number(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"➖ REMOVE NUMBER\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send number to remove:\n"
        f"Example: 911234567890\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def remove_handler(client, msg):
        num = msg.text.strip()
        result = db.numbers.delete_one({"number": num})
        if result.deleted_count:
            await msg.reply(f"✅ {num} removed successfully.")
        else:
            await msg.reply(f"❌ {num} not found.")
        app.remove_handler(remove_handler)

# ---------- BAN USER ----------
@app.on_message(filters.text & filters.private & filters.regex("🚫 Ban User"))
async def ban_user(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"🚫 BAN USER\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send user ID to ban:\n"
        f"Example: 123456789\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def ban_handler(client, msg):
        try:
            uid = int(msg.text.strip())
            db.users.update_one({"user_id": uid}, {"$set": {"is_banned": True}})
            await msg.reply(f"✅ User {uid} banned successfully.")
        except:
            await msg.reply("❌ Invalid user ID. Must be a number.")
        app.remove_handler(ban_handler)

# ---------- UNBAN USER ----------
@app.on_message(filters.text & filters.private & filters.regex("✅ Unban User"))
async def unban_user(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"✅ UNBAN USER\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send user ID to unban:\n"
        f"Example: 123456789\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def unban_handler(client, msg):
        try:
            uid = int(msg.text.strip())
            db.users.update_one({"user_id": uid}, {"$set": {"is_banned": False}})
            await msg.reply(f"✅ User {uid} unbanned successfully.")
        except:
            await msg.reply("❌ Invalid user ID. Must be a number.")
        app.remove_handler(unban_handler)

# ---------- BROADCAST ----------
@app.on_message(filters.text & filters.private & filters.regex("📢 Broadcast"))
async def broadcast(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"📢 BROADCAST\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Send the message you want to broadcast to all users.\n\n"
        f"⚠️ This will be sent to ALL users.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def broadcast_handler(client, msg):
        text = msg.text
        users = db.users.find({})
        count = 0
        
        await msg.reply("⏳ Broadcasting... Please wait.")
        
        for user in users:
            try:
                await client.send_message(
                    user["user_id"],
                    f"📢 BROADCAST\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                    f"{text}\n"
                    f"━━━━━━━━━━━━━━━━━━━━━━━"
                )
                count += 1
                await asyncio.sleep(0.01)
            except:
                pass
        
        await msg.reply(f"✅ Broadcast sent to {count} users.")
        app.remove_handler(broadcast_handler)

# ---------- STATS ----------
@app.on_message(filters.text & filters.private & filters.regex("📈 Stats"))
async def stats_cmd(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
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
        f"📊 BOT STATISTICS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"👥 Users: {total_users}\n"
        f"📱 Numbers: {total_numbers}\n"
        f"✅ Available: {available}\n"
        f"🔴 In Use: {in_use}\n"
        f"🚫 Banned: {banned}\n"
        f"🔑 OTPs: {total_otp}\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )

# ---------- USERS LIST ----------
@app.on_message(filters.text & filters.private & filters.regex("👥 Users List"))
async def users_list(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    users = list(db.users.find({}).limit(20))
    if not users:
        await message.reply(
            f"👥 USERS LIST\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📭 No users.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    text = f"👥 USERS LIST\n"
    text += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for u in users:
        status = "🚫 Banned" if u.get("is_banned") else "✅ Active"
        nums = len(u.get("used_numbers", []))
        otps = u.get("total_otp", 0)
        text += f"• {u['user_id']} – {u.get('first_name', 'Unknown')}\n"
        text += f"  📱 {nums} numbers • 🔑 {otps} OTPs • {status}\n"
        text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    await message.reply(text)

# ---------- COUNTRY RANK ----------
@app.on_message(filters.text & filters.private & filters.regex("🌍 Country Rank"))
async def country_rank(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    pipeline = [
        {"$group": {"_id": "$country", "total_otp": {"$sum": "$otp_count"}}},
        {"$sort": {"total_otp": -1}},
        {"$limit": 10}
    ]
    results = list(db.numbers.aggregate(pipeline))
    
    if not results:
        await message.reply(
            f"🌍 COUNTRY RANK\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 No OTP data yet.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    total_otp = sum([r["total_otp"] for r in results])
    stats = f"🌍 COUNTRY RANKING\n"
    stats += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    for i, doc in enumerate(results, 1):
        flag = get_country_info(doc["_id"])["flag"] if doc["_id"] != "UNKNOWN" else "🏳️"
        percentage = round((doc["total_otp"] / total_otp) * 100, 1) if total_otp > 0 else 0
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        stats += f"{medal} {flag} {doc['_id']}\n"
        stats += f"   📱 {doc['total_otp']} OTPs • {percentage}%\n"
        stats += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    stats += f"\n📊 Total OTPs: {total_otp}\n"
    stats += f"🔄 Updated: {datetime.now().strftime('%H:%M:%S')}\n"
    stats += f"━━━━━━━━━━━━━━━━━━━━━━━"
    await message.reply(stats)

# ---------- OTP LOGS ----------
@app.on_message(filters.text & filters.private & filters.regex("📋 OTP Logs"))
async def otp_logs(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    logs = list(db.otp_logs.find({}).sort("timestamp", -1).limit(20))
    
    if not logs:
        await message.reply(
            f"📋 OTP LOGS\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━\n"
            f"📭 No OTP logs yet.\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        return
    
    text = f"📋 OTP LOGS\n"
    text += f"━━━━━━━━━━━━━━━━━━━━━━━\n\n"
    
    for i, log in enumerate(logs, 1):
        flag = log.get("flag", "🏳️")
        masked = log.get("masked_number", log.get("number", "Unknown"))
        otp = log.get("otp", "N/A")
        time = log.get("timestamp", datetime.now()).strftime('%H:%M:%S')
        text += f"{i}. {flag} {masked} → {otp} @ {time}\n"
        text += f"   👤 {log.get('user_id', 'Unknown')}\n"
        text += f"━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    text += f"\n📤 To export JSON: /export_otp_logs"
    await message.reply(text)

# ---------- EXPORT OTP LOGS ----------
@app.on_message(filters.command("export_otp_logs") & filters.private)
async def export_otp_logs(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    logs = list(db.otp_logs.find({}, {"_id": 0}).sort("timestamp", -1))
    
    if not logs:
        await message.reply("📭 No OTP logs to export.")
        return
    
    for log in logs:
        if "timestamp" in log:
            log["timestamp"] = log["timestamp"].isoformat()
    
    json_data = json.dumps(logs, indent=2)
    
    with open("otp_logs.json", "w") as f:
        f.write(json_data)
    
    await message.reply_document(
        document="otp_logs.json",
        caption=f"📊 OTP Logs Export\nTotal: {len(logs)} entries"
    )

# ---------- FORCE JOIN SETTINGS ----------
@app.on_message(filters.text & filters.private & filters.regex("🔧 Force Join Settings"))
async def force_join_settings(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        await message.reply("⛔ Admin only.")
        return
    
    await message.reply(
        f"🔧 FORCE JOIN SETTINGS\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━\n"
        f"Current Channel: {CHANNEL_ID}\n"
        f"Status: Disabled (User side)\n\n"
        f"Send new channel username to update.\n"
        f"Example: @newchannel\n"
        f"Or send /skip to cancel.\n\n"
        f"⚠️ This will only update the channel name.\n"
        f"━━━━━━━━━━━━━━━━━━━━━━━"
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def update_channel_handler(client, msg):
        text = msg.text.strip()
        
        if text == "/skip":
            await msg.reply("❌ Cancelled.")
            app.remove_handler(update_channel_handler)
            return
        
        if not text.startswith("@"):
            await msg.reply("❌ Invalid channel format. Use @username")
            return
        
        global CHANNEL_ID
        CHANNEL_ID = text
        db.settings.update_one({"_id": "force_join"}, {"$set": {"channel": text}}, upsert=True)
        
        await msg.reply(
            f"✅ Force Join channel updated!\n\n"
            f"New Channel: {text}\n"
            f"━━━━━━━━━━━━━━━━━━━━━━━"
        )
        app.remove_handler(update_channel_handler)

# ---------- ONLINE NOTIFICATION ----------
async def send_online_notification():
    await asyncio.sleep(3)
    try:
        for admin_id in ADMIN_IDS:
            await app.send_message(
                admin_id,
                f"✅ {BOT_NAME} IS ONLINE!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━\n"
                f"🚀 Bot is now active and ready!\n"
                f"📌 All features are working.\n"
                f"🕐 Time: {datetime.now().strftime('%H:%M:%S')}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━━"
            )
    except:
        pass

# ---------- RUN ----------
print(f"🚀 {BOT_NAME} Starting...")
print("========================================")
print(f"✅ Bot Name: {BOT_NAME}")
print(f"✅ Admin ID: {ADMIN_IDS[0]}")
print(f"✅ Channel: {CHANNEL_ID}")
print(f"✅ Group: {GROUP_ID}")
print(f"✅ Database: Connected")
print(f"✅ Countries: {len(COUNTRIES)}")
print(f"✅ Workers: 100")
print(f"✅ Force Join: Disabled")
print(f"✅ OTP Masking: Enabled")
print(f"✅ OTP Logs: Enabled")
print("========================================")

app.run()