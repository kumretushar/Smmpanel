import asyncio
import re
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from pymongo import MongoClient
import aiohttp

# ---------- YOUR CONFIG ----------
API_ID = 30954859
API_HASH = "240537c89299fc2c94e8c78607229a21"
BOT_TOKEN = "8841502557:AAH7m1ezXQbK8DKHsGuY6T7H2IMPtRAeVq8"
GROUP_ID = -1002949251809
CHANNEL_ID = "@gmtusharxfiles"
OTP_GROUP_LINK = "https://t.me/trxxotp"

BOT_NAME = "𝗚𝗠𝘅𝗢𝗧𝗣 ✉️"

# ---------- MONGODB ----------
MONGO_URI = "mongodb://tusharkumarin74_db_user:star%40123@ac-zborjum-shard-00-00.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-01.7jv0uuq.mongodb.net:27017,ac-zborjum-shard-00-02.7jv0uuq.mongodb.net:27017/?ssl=true&replicaSet=atlas-qnvkfj-shard-0&authSource=admin&appName=Cluster"

db_client = MongoClient(
    MONGO_URI,
    maxPoolSize=100,
    minPoolSize=20,
    maxIdleTimeMS=30000,
    connectTimeoutMS=2000,
    socketTimeoutMS=2000,
    retryWrites=False,
    w=0
)
db = db_client.numberx

ADMIN_IDS = [8430946490]

# ---------- CLIENT (FIXED — "default" parse mode) ----------
app = Client(
    "numberx_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN,
    sleep_threshold=0,
    workers=100,
    parse_mode="default",  # ✅ FIXED: "default" works everywhere
    max_concurrent_transmissions=100
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

# ---------- ALL COUNTRIES (COMPLETE) ----------
COUNTRIES = {
    "+93": {"flag": "🇦🇫", "name": "Afghanistan"},
    "+355": {"flag": "🇦🇱", "name": "Albania"},
    "+213": {"flag": "🇩🇿", "name": "Algeria"},
    "+376": {"flag": "🇦🇩", "name": "Andorra"},
    "+244": {"flag": "🇦🇴", "name": "Angola"},
    "+54": {"flag": "🇦🇷", "name": "Argentina"},
    "+374": {"flag": "🇦🇲", "name": "Armenia"},
    "+61": {"flag": "🇦🇺", "name": "Australia"},
    "+43": {"flag": "🇦🇹", "name": "Austria"},
    "+994": {"flag": "🇦🇿", "name": "Azerbaijan"},
    "+1242": {"flag": "🇧🇸", "name": "Bahamas"},
    "+973": {"flag": "🇧🇭", "name": "Bahrain"},
    "+880": {"flag": "🇧🇩", "name": "Bangladesh"},
    "+375": {"flag": "🇧🇾", "name": "Belarus"},
    "+32": {"flag": "🇧🇪", "name": "Belgium"},
    "+501": {"flag": "🇧🇿", "name": "Belize"},
    "+229": {"flag": "🇧🇯", "name": "Benin"},
    "+975": {"flag": "🇧🇹", "name": "Bhutan"},
    "+591": {"flag": "🇧🇴", "name": "Bolivia"},
    "+387": {"flag": "🇧🇦", "name": "Bosnia and Herzegovina"},
    "+267": {"flag": "🇧🇼", "name": "Botswana"},
    "+55": {"flag": "🇧🇷", "name": "Brazil"},
    "+673": {"flag": "🇧🇳", "name": "Brunei"},
    "+359": {"flag": "🇧🇬", "name": "Bulgaria"},
    "+226": {"flag": "🇧🇫", "name": "Burkina Faso"},
    "+257": {"flag": "🇧🇮", "name": "Burundi"},
    "+855": {"flag": "🇰🇭", "name": "Cambodia"},
    "+237": {"flag": "🇨🇲", "name": "Cameroon"},
    "+1": {"flag": "🇨🇦", "name": "Canada"},
    "+238": {"flag": "🇨🇻", "name": "Cape Verde"},
    "+236": {"flag": "🇨🇫", "name": "Central African Republic"},
    "+235": {"flag": "🇹🇩", "name": "Chad"},
    "+56": {"flag": "🇨🇱", "name": "Chile"},
    "+86": {"flag": "🇨🇳", "name": "China"},
    "+57": {"flag": "🇨🇴", "name": "Colombia"},
    "+269": {"flag": "🇰🇲", "name": "Comoros"},
    "+242": {"flag": "🇨🇬", "name": "Congo"},
    "+506": {"flag": "🇨🇷", "name": "Costa Rica"},
    "+385": {"flag": "🇭🇷", "name": "Croatia"},
    "+53": {"flag": "🇨🇺", "name": "Cuba"},
    "+357": {"flag": "🇨🇾", "name": "Cyprus"},
    "+420": {"flag": "🇨🇿", "name": "Czech Republic"},
    "+45": {"flag": "🇩🇰", "name": "Denmark"},
    "+253": {"flag": "🇩🇯", "name": "Djibouti"},
    "+1767": {"flag": "🇩🇲", "name": "Dominica"},
    "+1809": {"flag": "🇩🇴", "name": "Dominican Republic"},
    "+593": {"flag": "🇪🇨", "name": "Ecuador"},
    "+20": {"flag": "🇪🇬", "name": "Egypt"},
    "+503": {"flag": "🇸🇻", "name": "El Salvador"},
    "+240": {"flag": "🇬🇶", "name": "Equatorial Guinea"},
    "+291": {"flag": "🇪🇷", "name": "Eritrea"},
    "+372": {"flag": "🇪🇪", "name": "Estonia"},
    "+251": {"flag": "🇪🇹", "name": "Ethiopia"},
    "+679": {"flag": "🇫🇯", "name": "Fiji"},
    "+358": {"flag": "🇫🇮", "name": "Finland"},
    "+33": {"flag": "🇫🇷", "name": "France"},
    "+241": {"flag": "🇬🇦", "name": "Gabon"},
    "+220": {"flag": "🇬🇲", "name": "Gambia"},
    "+995": {"flag": "🇬🇪", "name": "Georgia"},
    "+49": {"flag": "🇩🇪", "name": "Germany"},
    "+233": {"flag": "🇬🇭", "name": "Ghana"},
    "+30": {"flag": "🇬🇷", "name": "Greece"},
    "+502": {"flag": "🇬🇹", "name": "Guatemala"},
    "+224": {"flag": "🇬🇳", "name": "Guinea"},
    "+245": {"flag": "🇬🇼", "name": "Guinea-Bissau"},
    "+592": {"flag": "🇬🇾", "name": "Guyana"},
    "+509": {"flag": "🇭🇹", "name": "Haiti"},
    "+504": {"flag": "🇭🇳", "name": "Honduras"},
    "+36": {"flag": "🇭🇺", "name": "Hungary"},
    "+354": {"flag": "🇮🇸", "name": "Iceland"},
    "+91": {"flag": "🇮🇳", "name": "India"},
    "+62": {"flag": "🇮🇩", "name": "Indonesia"},
    "+98": {"flag": "🇮🇷", "name": "Iran"},
    "+964": {"flag": "🇮🇶", "name": "Iraq"},
    "+353": {"flag": "🇮🇪", "name": "Ireland"},
    "+972": {"flag": "🇮🇱", "name": "Israel"},
    "+39": {"flag": "🇮🇹", "name": "Italy"},
    "+225": {"flag": "🇨🇮", "name": "Ivory Coast"},
    "+81": {"flag": "🇯🇵", "name": "Japan"},
    "+962": {"flag": "🇯🇴", "name": "Jordan"},
    "+7": {"flag": "🇰🇿", "name": "Kazakhstan"},
    "+254": {"flag": "🇰🇪", "name": "Kenya"},
    "+686": {"flag": "🇰🇮", "name": "Kiribati"},
    "+965": {"flag": "🇰🇼", "name": "Kuwait"},
    "+996": {"flag": "🇰🇬", "name": "Kyrgyzstan"},
    "+856": {"flag": "🇱🇦", "name": "Laos"},
    "+371": {"flag": "🇱🇻", "name": "Latvia"},
    "+961": {"flag": "🇱🇧", "name": "Lebanon"},
    "+266": {"flag": "🇱🇸", "name": "Lesotho"},
    "+231": {"flag": "🇱🇷", "name": "Liberia"},
    "+218": {"flag": "🇱🇾", "name": "Libya"},
    "+423": {"flag": "🇱🇮", "name": "Liechtenstein"},
    "+370": {"flag": "🇱🇹", "name": "Lithuania"},
    "+352": {"flag": "🇱🇺", "name": "Luxembourg"},
    "+261": {"flag": "🇲🇬", "name": "Madagascar"},
    "+265": {"flag": "🇲🇼", "name": "Malawi"},
    "+60": {"flag": "🇲🇾", "name": "Malaysia"},
    "+960": {"flag": "🇲🇻", "name": "Maldives"},
    "+223": {"flag": "🇲🇱", "name": "Mali"},
    "+356": {"flag": "🇲🇹", "name": "Malta"},
    "+692": {"flag": "🇲🇭", "name": "Marshall Islands"},
    "+222": {"flag": "🇲🇷", "name": "Mauritania"},
    "+230": {"flag": "🇲🇺", "name": "Mauritius"},
    "+52": {"flag": "🇲🇽", "name": "Mexico"},
    "+691": {"flag": "🇫🇲", "name": "Micronesia"},
    "+373": {"flag": "🇲🇩", "name": "Moldova"},
    "+377": {"flag": "🇲🇨", "name": "Monaco"},
    "+976": {"flag": "🇲🇳", "name": "Mongolia"},
    "+382": {"flag": "🇲🇪", "name": "Montenegro"},
    "+212": {"flag": "🇲🇦", "name": "Morocco"},
    "+258": {"flag": "🇲🇿", "name": "Mozambique"},
    "+95": {"flag": "🇲🇲", "name": "Myanmar"},
    "+264": {"flag": "🇳🇦", "name": "Namibia"},
    "+674": {"flag": "🇳🇷", "name": "Nauru"},
    "+977": {"flag": "🇳🇵", "name": "Nepal"},
    "+31": {"flag": "🇳🇱", "name": "Netherlands"},
    "+64": {"flag": "🇳🇿", "name": "New Zealand"},
    "+505": {"flag": "🇳🇮", "name": "Nicaragua"},
    "+227": {"flag": "🇳🇪", "name": "Niger"},
    "+234": {"flag": "🇳🇬", "name": "Nigeria"},
    "+850": {"flag": "🇰🇵", "name": "North Korea"},
    "+47": {"flag": "🇳🇴", "name": "Norway"},
    "+968": {"flag": "🇴🇲", "name": "Oman"},
    "+92": {"flag": "🇵🇰", "name": "Pakistan"},
    "+680": {"flag": "🇵🇼", "name": "Palau"},
    "+970": {"flag": "🇵🇸", "name": "Palestine"},
    "+507": {"flag": "🇵🇦", "name": "Panama"},
    "+675": {"flag": "🇵🇬", "name": "Papua New Guinea"},
    "+595": {"flag": "🇵🇾", "name": "Paraguay"},
    "+51": {"flag": "🇵🇪", "name": "Peru"},
    "+63": {"flag": "🇵🇭", "name": "Philippines"},
    "+48": {"flag": "🇵🇱", "name": "Poland"},
    "+351": {"flag": "🇵🇹", "name": "Portugal"},
    "+974": {"flag": "🇶🇦", "name": "Qatar"},
    "+40": {"flag": "🇷🇴", "name": "Romania"},
    "+7": {"flag": "🇷🇺", "name": "Russia"},
    "+250": {"flag": "🇷🇼", "name": "Rwanda"},
    "+685": {"flag": "🇼🇸", "name": "Samoa"},
    "+378": {"flag": "🇸🇲", "name": "San Marino"},
    "+966": {"flag": "🇸🇦", "name": "Saudi Arabia"},
    "+221": {"flag": "🇸🇳", "name": "Senegal"},
    "+381": {"flag": "🇷🇸", "name": "Serbia"},
    "+248": {"flag": "🇸🇨", "name": "Seychelles"},
    "+232": {"flag": "🇸🇱", "name": "Sierra Leone"},
    "+65": {"flag": "🇸🇬", "name": "Singapore"},
    "+421": {"flag": "🇸🇰", "name": "Slovakia"},
    "+386": {"flag": "🇸🇮", "name": "Slovenia"},
    "+677": {"flag": "🇸🇧", "name": "Solomon Islands"},
    "+252": {"flag": "🇸🇴", "name": "Somalia"},
    "+27": {"flag": "🇿🇦", "name": "South Africa"},
    "+82": {"flag": "🇰🇷", "name": "South Korea"},
    "+34": {"flag": "🇪🇸", "name": "Spain"},
    "+94": {"flag": "🇱🇰", "name": "Sri Lanka"},
    "+249": {"flag": "🇸🇩", "name": "Sudan"},
    "+597": {"flag": "🇸🇷", "name": "Suriname"},
    "+268": {"flag": "🇸🇿", "name": "Swaziland"},
    "+46": {"flag": "🇸🇪", "name": "Sweden"},
    "+41": {"flag": "🇨🇭", "name": "Switzerland"},
    "+963": {"flag": "🇸🇾", "name": "Syria"},
    "+886": {"flag": "🇹🇼", "name": "Taiwan"},
    "+992": {"flag": "🇹🇯", "name": "Tajikistan"},
    "+255": {"flag": "🇹🇿", "name": "Tanzania"},
    "+66": {"flag": "🇹🇭", "name": "Thailand"},
    "+228": {"flag": "🇹🇬", "name": "Togo"},
    "+676": {"flag": "🇹🇴", "name": "Tonga"},
    "+1868": {"flag": "🇹🇹", "name": "Trinidad and Tobago"},
    "+216": {"flag": "🇹🇳", "name": "Tunisia"},
    "+90": {"flag": "🇹🇷", "name": "Turkey"},
    "+993": {"flag": "🇹🇲", "name": "Turkmenistan"},
    "+688": {"flag": "🇹🇻", "name": "Tuvalu"},
    "+256": {"flag": "🇺🇬", "name": "Uganda"},
    "+380": {"flag": "🇺🇦", "name": "Ukraine"},
    "+971": {"flag": "🇦🇪", "name": "United Arab Emirates"},
    "+44": {"flag": "🇬🇧", "name": "United Kingdom"},
    "+1": {"flag": "🇺🇸", "name": "United States"},
    "+598": {"flag": "🇺🇾", "name": "Uruguay"},
    "+998": {"flag": "🇺🇿", "name": "Uzbekistan"},
    "+678": {"flag": "🇻🇺", "name": "Vanuatu"},
    "+379": {"flag": "🇻🇦", "name": "Vatican City"},
    "+58": {"flag": "🇻🇪", "name": "Venezuela"},
    "+84": {"flag": "🇻🇳", "name": "Vietnam"},
    "+967": {"flag": "🇾🇪", "name": "Yemen"},
    "+260": {"flag": "🇿🇲", "name": "Zambia"},
    "+263": {"flag": "🇿🇼", "name": "Zimbabwe"}
}

def get_country_info(code):
    for country_code, info in COUNTRIES.items():
        if code.startswith(country_code):
            return info
    return {"flag": "🏳️", "name": "Unknown"}

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
def bold(text):
    return f"**{text}**"

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

# ---------- FORCE JOIN ----------
async def force_join_check(user_id):
    try:
        member = await app.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member", "administrator", "creator"]
    except:
        return False

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
    ["🔙 Back"]
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
                            "country_code": num[:3] if num.startswith("+") else "UNKNOWN",
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

def format_numbers_with_flags(numbers, service):
    text = f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**{BOT_NAME}**  💎 Premium
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

📱 **YOUR NUMBERS** 
━━━━━━━━━━━━━━━━━━━━━━━
"""
    for num in numbers:
        info = get_country_info(num)
        text += f"""
{info['flag']} **Number:** `{num}`
📌 **Service:** {service}
━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    text += f"""
⏳ **Auto-Change in 2s...**
🔄 New numbers incoming!

━━━━━━━━━━━━━━━━━━━━━━━
🔹 **OTP Group:** {OTP_GROUP_LINK}
━━━━━━━━━━━━━━━━━━━━━━━
"""
    return text

# ---------- START ----------
@app.on_message(filters.command("start") & filters.private)
async def start(client, message):
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    first_name = message.from_user.first_name or "User"
    
    add_user(user_id, username, first_name)
    
    if is_banned(user_id):
        await message.reply(f"{bold('🚫 You are banned.')}")
        return
    
    if not await force_join_check(user_id):
        await message.reply(
            f"""
{bold("⚠️ Join Channel First")}

━━━━━━━━━━━━━━━━━━━━━━━
Please join: {CHANNEL_ID}
━━━━━━━━━━━━━━━━━━━━━━━
""",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")],
                [InlineKeyboardButton("✅ Joined", callback_data="check_join")]
            ])
        )
        return
    
    keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**{BOT_NAME}** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

👋 Hello {first_name}!
📌 Choose an option below.
━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=keyboard
    )

# ---------- CHECK JOIN ----------
@app.on_callback_query(filters.regex("check_join"))
async def check_join_callback(client, callback):
    user_id = callback.from_user.id
    is_member = await force_join_check(user_id)
    
    if is_member:
        keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
        await callback.message.edit_text(
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**✅ Welcome to {BOT_NAME}** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

🎉 Thanks for joining!
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
        await callback.message.reply(
            "🎉 Use buttons below.",
            reply_markup=keyboard
        )
        await callback.answer("✅ Joined!", show_alert=True)
    else:
        await callback.answer(
            "❌ Join first, then click again.",
            show_alert=True
        )

# ---------- GET NUMBER ----------
@app.on_message(filters.text & filters.private & filters.regex("📱 Get Number"))
async def get_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return await message.reply(f"{bold('🚫 You are banned.')}")
    
    if not await force_join_check(user_id):
        return await message.reply(
            f"{bold('⚠️ Join channel first:')} {CHANNEL_ID}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")]
            ])
        )
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📱 SELECT SERVICE** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Choose service:
━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=ReplyKeyboardMarkup([
            ["📱 WhatsApp", "📘 Facebook"],
            ["✈️ Telegram", "📸 Instagram"],
            ["🔙 Back"]
        ], resize_keyboard=True)
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def service_handler(client, msg):
        service = msg.text.strip()
        
        if service == "🔙 Back":
            keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
            await msg.reply("🔙 Main menu.", reply_markup=keyboard)
            app.remove_handler(service_handler)
            return
        
        numbers, error = await allocate_three_numbers(user_id, service)
        
        if error:
            await msg.reply(f"❌ {error}")
            app.remove_handler(service_handler)
            return
        
        numbers_text = format_numbers_with_flags(numbers, service)
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
        
        new_text = format_numbers_with_flags(new_numbers, service)
        new_text = new_text.replace("Auto-Change in 2s...", "✅ **Auto-Changed!**")
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
    
    db.numbers.update_one(
        {"number": last_number},
        {
            "$push": {"otp_received": text},
            "$inc": {"otp_count": 1}
        }
    )
    db.users.update_one(
        {"user_id": user_id},
        {"$inc": {"total_otp": 1}}
    )
    clear_cache()
    
    try:
        await client.send_message(
            GROUP_ID,
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**🔑 OTP RECEIVED** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

📱 Number: `{last_number}`
{flag} Country: {country}
🔐 OTP: `{text}`
👤 User: {user_id}
🕐 Time: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
    except:
        pass

# ---------- TRAFFIC STATS ----------
@app.on_message(filters.text & filters.private & filters.regex("📊 Traffic Stats"))
async def traffic_stats(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return await message.reply(f"{bold('🚫 You are banned.')}")
    
    if not await force_join_check(user_id):
        return await message.reply(
            f"{bold('⚠️ Join channel first:')} {CHANNEL_ID}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")]
            ])
        )
    
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
        return await message.reply(
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📊 TRAFFIC STATS** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

📭 No OTP data yet.

💡 Start using numbers to generate data!
━━━━━━━━━━━━━━━━━━━━━━━
🔄 Updated: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
    
    stats = f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📊 LIVE TRAFFIC STATS** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

📊 **Total OTPs Received:** {total_otp}
━━━━━━━━━━━━━━━━━━━━━━━
🏆 **COUNTRY RANKINGS**
━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    for i, doc in enumerate(results, 1):
        flag = get_country_info(doc["_id"])["flag"] if doc["_id"] != "UNKNOWN" else "🏳️"
        percentage = round((doc["total_otp"] / total_otp) * 100, 1) if total_otp > 0 else 0
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        stats += f"""
{medal} {flag} **{doc['_id']}**
   📱 {doc['total_otp']} OTPs  •  {percentage}% of total
━━━━━━━━━━━━━━━━━━━━━━━
"""
    
    stats += f"""
🔄 **Updated:** {datetime.now().strftime('%H:%M:%S')}
📌 **Showing:** Top {len(results)} countries
━━━━━━━━━━━━━━━━━━━━━━━
💡 Use top countries for best results!
━━━━━━━━━━━━━━━━━━━━━━━
"""
    await message.reply(stats)

# ---------- SEARCH ----------
@app.on_message(filters.text & filters.private & filters.regex("🔍 Search Number"))
async def search_number(client, message):
    user_id = message.from_user.id
    if is_banned(user_id):
        return await message.reply(f"{bold('🚫 You are banned.')}")
    
    if not await force_join_check(user_id):
        return await message.reply(
            f"{bold('⚠️ Join channel first:')} {CHANNEL_ID}",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📢 Join", url=f"https://t.me/{CHANNEL_ID.replace('@', '')}")]
            ])
        )
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**🔍 SEARCH NUMBERS** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Send country code (e.g., +91, +1, +44):
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def search_handler(client, msg):
        code = msg.text.strip()
        available = list(db.numbers.find({"country_code": code, "status": "available"}).limit(10))
        
        if not available:
            await msg.reply(
                f"""
❌ **No numbers found for {code}**

━━━━━━━━━━━━━━━━━━━━━━━
💡 Try another country code.
━━━━━━━━━━━━━━━━━━━━━━━
"""
            )
        else:
            text = f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**✅ AVAILABLE NUMBERS** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

**Country:** {code}
**Available:** {len(available)}
━━━━━━━━━━━━━━━━━━━━━━━
"""
            for n in available:
                flag = n.get("flag", "🏳️")
                service = n.get("service", "WhatsApp")
                text += f"{flag} `{n['number']}` – {service}\n"
            
            text += """
━━━━━━━━━━━━━━━━━━━━━━━
💡 Click **Get Number** to claim!
"""
            await msg.reply(text)
        app.remove_handler(search_handler)

# ---------- SUPPORT ----------
@app.on_message(filters.text & filters.private & filters.regex("🆘 Support"))
async def support(client, message):
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**🆘 SUPPORT CENTER** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

👤 Admin: @Amarstarx
📞 Contact: {ADMIN_IDS[0]}

⚡ Response: Within 1 hour
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )

# ---------- HELP ----------
@app.on_message(filters.text & filters.private & filters.regex("❓ Help"))
async def help_cmd(client, message):
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**❓ HOW TO USE** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

📱 **Get Number** – Get 3 numbers at once
   ⏳ Auto-change in 2s

🔍 **Search Number** – Search by country
   📌 See available numbers

📊 **Traffic Stats** – Real-time OTP stats
   🏆 Country ranking
   📊 Percentage breakdown
   🔄 Live updates

🆘 **Support** – Contact admin

━━━━━━━━━━━━━━━━━━━━━━━
💎 **Premium Features:**
✅ 3 Numbers at once
✅ Auto-change in 2s
✅ Direct OTP Group
✅ Real-time Traffic Stats with %
✅ User Isolation
✅ Service Management
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )

# ---------- ABOUT ----------
@app.on_message(filters.text & filters.private & filters.regex("ℹ️ About"))
async def about(client, message):
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**ℹ️ ABOUT {BOT_NAME}** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

👨‍💻 Developer: @Amarstarx
🗄️ Database: MongoDB
⚡ Status: Online 24/7
💎 Version: Premium 4.0

✨ **Features:**
✅ 3 Numbers at once
✅ Auto-change in 2s
✅ Direct OTP Group
✅ Real-time Traffic Stats
✅ User Isolation
✅ Service Management
✅ Admin Panel
✅ Broadcast System
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )

# ---------- OTP GROUP ----------
@app.on_message(filters.text & filters.private & filters.regex("📢 OTP Group"))
async def otp_group(client, message):
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📢 OTP GROUP** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

🔥 Join now to receive OTPs!

[🚀 Click Here to Join]({OTP_GROUP_LINK})

━━━━━━━━━━━━━━━━━━━━━━━
💡 All OTPs forwarded here
━━━━━━━━━━━━━━━━━━━━━━━
""",
        disable_web_page_preview=True
    )

# ---------- CLOSE ----------
@app.on_message(filters.text & filters.private & filters.regex("❌ Close"))
async def close_message(client, message):
    user_id = message.from_user.id
    keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
    await message.reply(
        f"""
✅ **Closed.**  
📌 Use buttons below.
""",
        reply_markup=keyboard
    )

# ---------- BACK ----------
@app.on_message(filters.text & filters.private & filters.regex("🔙 Back"))
@app.on_message(filters.text & filters.private & filters.regex("🔙 Back to Main"))
async def back_to_main(client, message):
    user_id = message.from_user.id
    keyboard = admin_keyboard if is_admin(user_id) else user_keyboard
    await message.reply(
        f"""
✅ **Main Menu**  
📌 Use buttons below.
""",
        reply_markup=keyboard
    )

# ---------- ADMIN PANEL ----------
@app.on_message(filters.text & filters.private & filters.regex("📊 Admin Panel"))
async def admin_panel(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return await message.reply(f"{bold('⛔ Admin only.')}")
    
    total_users = db.users.count_documents({})
    total_numbers = db.numbers.count_documents({})
    available = db.numbers.count_documents({"status": "available"})
    in_use = db.numbers.count_documents({"status": "in_use"})
    banned = db.users.count_documents({"is_banned": True})
    total_otp = db.numbers.aggregate([{"$group": {"_id": None, "total": {"$sum": "$otp_count"}}}])
    total_otp = list(total_otp)
    total_otp = total_otp[0]["total"] if total_otp else 0
    
    total_allocated = db.users.aggregate([{"$group": {"_id": None, "total": {"$sum": "$numbers_allocated"}}}])
    total_allocated = list(total_allocated)
    total_allocated = total_allocated[0]["total"] if total_allocated else 0
    
    services = db.numbers.distinct("service")
    service_text = ""
    for s in services:
        count = db.numbers.count_documents({"service": s})
        service_text += f"   • {s}: {count} numbers\n"
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**👑 ADMIN DASHBOARD** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

📊 **Overall Stats:**
━━━━━━━━━━━━━━━━━━━━━━━
👥 Total Users: {total_users}
📱 Total Numbers: {total_numbers}
✅ Available: {available}
🔴 In Use: {in_use}
🚫 Banned: {banned}
🔑 Total OTPs: {total_otp}
📦 Total Allocated: {total_allocated}

━━━━━━━━━━━━━━━━━━━━━━━
📋 **Services:**
{service_text if service_text else '   No services yet'}
━━━━━━━━━━━━━━━━━━━━━━━
🔄 Updated: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━
""",
        reply_markup=admin_panel_keyboard
    )

# ---------- ADD NUMBER ----------
@app.on_message(filters.text & filters.private & filters.regex("➕ Add Number"))
async def add_number(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**➕ ADD NUMBER** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Send country code (e.g., +91, +1, +44):
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def step1_country(client, msg):
        country_code = msg.text.strip()
        country_info = get_country_info(country_code)
        flag = country_info["flag"]
        country_name = country_info["name"]
        
        await msg.reply(
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**➕ ADD NUMBER - STEP 2** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Country: {flag} {country_name} ({country_code})

Send numbers (one per line):
Example:
+911234567890
+44234567890
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
        
        @app.on_message(filters.text & filters.private & ~filters.command("start"))
        async def step2_numbers(client, msg):
            numbers = msg.text.strip().split("\n")
            
            await msg.reply(
                f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**➕ ADD NUMBER - STEP 3** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Select service:
━━━━━━━━━━━━━━━━━━━━━━━
""",
                reply_markup=ReplyKeyboardMarkup([
                    ["WhatsApp", "Facebook", "Telegram"],
                    ["Instagram", "Custom Service", "🔙 Back"]
                ], resize_keyboard=True)
            )
            
            @app.on_message(filters.text & filters.private & ~filters.command("start"))
            async def step3_service(client, msg):
                service = msg.text.strip()
                
                if service == "Custom Service":
                    await msg.reply("Send custom service name:")
                    
                    @app.on_message(filters.text & filters.private & ~filters.command("start"))
                    async def custom_service(client, msg):
                        service = msg.text.strip()
                        await add_numbers_to_db(msg, numbers, country_code, country_name, flag, service)
                        app.remove_handler(custom_service)
                    return
                
                if service == "🔙 Back":
                    await admin_panel(client, msg)
                    return
                
                await add_numbers_to_db(msg, numbers, country_code, country_name, flag, service)
                app.remove_handler(step3_service)
            
            app.remove_handler(step2_numbers)
        
        app.remove_handler(step1_country)

async def add_numbers_to_db(msg, numbers, country_code, country_name, flag, service):
    added = 0
    for num in numbers:
        num = num.strip()
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
    
    await msg.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**✅ NUMBERS ADDED** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Country: {flag} {country_name}
Service: {service}
Added: {added} numbers
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )

# ---------- REMOVE NUMBER ----------
@app.on_message(filters.text & filters.private & filters.regex("➖ Remove Number"))
async def remove_number(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**➖ REMOVE NUMBER** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Send number to remove:
Example: +911234567890
━━━━━━━━━━━━━━━━━━━━━━━
"""
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

# ---------- CREATE SERVICE ----------
@app.on_message(filters.text & filters.private & filters.regex("➕ Create Service"))
async def create_service(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**➕ CREATE SERVICE** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Send new service name:
Example: Snapchat, Twitter, etc.
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def create_handler(client, msg):
        service = msg.text.strip()
        
        existing = db.numbers.find_one({"service": service})
        if existing:
            await msg.reply(f"❌ Service '{service}' already exists.")
            app.remove_handler(create_handler)
            return
        
        db.numbers.insert_one({
            "number": "DUMMY",
            "country": "SYSTEM",
            "country_code": "+0",
            "flag": "🏳️",
            "service": service,
            "status": "available",
            "assigned_to": None,
            "otp_received": [],
            "otp_count": 0
        })
        db.numbers.delete_one({"number": "DUMMY"})
        
        await msg.reply(
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**✅ SERVICE CREATED** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Service: {service}
Status: Active

Now you can add numbers to this service.
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
        app.remove_handler(create_handler)

# ---------- REMOVE SERVICE ----------
@app.on_message(filters.text & filters.private & filters.regex("➖ Remove Service"))
async def remove_service(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    services = db.numbers.distinct("service")
    if not services:
        await message.reply("❌ No services available.")
        return
    
    service_list = "\n".join([f"• {s}" for s in services])
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**➖ REMOVE SERVICE** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Available Services:
{service_list}

━━━━━━━━━━━━━━━━━━━━━━━
Send service name to remove:
⚠️ This will delete ALL numbers in this service!
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )
    
    @app.on_message(filters.text & filters.private & ~filters.command("start"))
    async def remove_handler(client, msg):
        service = msg.text.strip()
        count = db.numbers.count_documents({"service": service})
        if count == 0:
            await msg.reply(f"❌ Service '{service}' not found.")
            app.remove_handler(remove_handler)
            return
        
        db.numbers.delete_many({"service": service})
        
        await msg.reply(
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**✅ SERVICE REMOVED** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Service: {service}
Numbers Deleted: {count}
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
        app.remove_handler(remove_handler)

# ---------- SERVICES LIST ----------
@app.on_message(filters.text & filters.private & filters.regex("📋 Services"))
async def manage_services(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    services = db.numbers.distinct("service")
    
    text = f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📋 SERVICES** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

"""
    if not services:
        text += "📭 No services available.\n"
    else:
        for s in services:
            count = db.numbers.count_documents({"service": s})
            text += f"• {s} – {count} numbers\n"
    
    text += """
━━━━━━━━━━━━━━━━━━━━━━━
💡 Use 'Create Service' to add new.
💡 Use 'Remove Service' to delete.
"""
    await message.reply(text)

# ---------- BAN USER ----------
@app.on_message(filters.text & filters.private & filters.regex("🚫 Ban User"))
async def ban_user(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    await message.reply(
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**🚫 BAN USER** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Send user ID to ban:
Example: 123456789
━━━━━━━━━━━━━━━━━━━━━━━
"""
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
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**✅ UNBAN USER** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Send user ID to unban:
Example: 123456789
━━━━━━━━━━━━━━━━━━━━━━━
"""
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
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📢 BROADCAST** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Send the message you want to broadcast to all users.

⚠️ This will be sent to ALL users.
━━━━━━━━━━━━━━━━━━━━━━━
"""
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
                    f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📢 BROADCAST** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

{text}
━━━━━━━━━━━━━━━━━━━━━━━
"""
                )
                count += 1
                await asyncio.sleep(0.01)
            except:
                pass
        
        await msg.reply(
            f"""
✅ **Broadcast Complete!**
━━━━━━━━━━━━━━━━━━━━━━━
Message sent to: {count} users
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
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
        f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📊 BOT STATISTICS** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

👥 Total Users: {total_users}
📱 Total Numbers: {total_numbers}
✅ Available: {available}
🔴 In Use: {in_use}
🚫 Banned: {banned}
🔑 Total OTPs: {total_otp}
━━━━━━━━━━━━━━━━━━━━━━━
"""
    )

# ---------- USERS LIST ----------
@app.on_message(filters.text & filters.private & filters.regex("👥 Users List"))
async def users_list(client, message):
    user_id = message.from_user.id
    if not is_admin(user_id):
        return
    
    users = list(db.users.find({}).limit(20))
    if not users:
        return await message.reply(
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📭 NO USERS** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Database is empty.
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
    
    text = f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**👥 USERS LIST** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

"""
    for u in users:
        status = "🚫 Banned" if u.get("is_banned") else "✅ Active"
        nums = len(u.get("used_numbers", []))
        otps = u.get("total_otp", 0)
        text += f"• {u['user_id']} – {u.get('first_name', 'Unknown')}\n"
        text += f"  📱 {nums} numbers • 🔑 {otps} OTPs • {status}\n"
        text += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    
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
        return await message.reply(
            f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**📊 NO OTP DATA** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

Start using numbers to generate data.
━━━━━━━━━━━━━━━━━━━━━━━
"""
        )
    
    total_otp = sum([r["total_otp"] for r in results])
    stats = f"""
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨
**🌍 COUNTRY RANKING** 💎
✨ **━━━━━━━━━━━━━━━━━━━━━━━** ✨

"""
    for i, doc in enumerate(results, 1):
        flag = get_country_info(doc["_id"])["flag"] if doc["_id"] != "UNKNOWN" else "🏳️"
        percentage = round((doc["total_otp"] / total_otp) * 100, 1) if total_otp > 0 else 0
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "🔹"
        stats += f"{medal} {flag} {doc['_id']}\n"
        stats += f"   📱 {doc['total_otp']} OTPs • {percentage}%\n"
        stats += "━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    stats += f"""
📊 Total OTPs: {total_otp}
🔄 Updated: {datetime.now().strftime('%H:%M:%S')}
━━━━━━━━━━━━━━━━━━━━━━━
"""
    await message.reply(stats)

# ---------- RUN ----------
print(f"🚀 {BOT_NAME} Starting...")
print("━━━━━━━━━━━━━━━━━━━━━━━")
print(f"✅ Bot Name: {BOT_NAME}")
print(f"✅ Admin ID: {ADMIN_IDS[0]}")
print(f"✅ Channel: {CHANNEL_ID}")
print(f"✅ Group: {GROUP_ID}")
print(f"✅ OTP Group: {OTP_GROUP_LINK}")
print(f"✅ Database: Connected")
print(f"✅ Countries Loaded: {len(COUNTRIES)}")
print(f"✅ Workers: 100")
print(f"✅ Cache: Enabled")
print(f"✅ Parse Mode: default (Fixed)")
print("━━━━━━━━━━━━━━━━━━━━━━━")

app.run()