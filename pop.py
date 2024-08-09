import os
import re
from telethon.sync import TelegramClient, events
from datetime import datetime

# Get the current date and time
current_datetime = datetime.now()

# Format the current date and time as required
formatted_date = current_datetime.strftime("%d-%m-%Y")  # Change the date format as needed
formatted_time = datetime.now().strftime("%H:%M:%S")  # Change the time format as needed

name = 'test'
api_id = 29114143
api_hash = 'd7f17f0b6657fe37142abcf7ba3e7d03'

capture_or_msg = []                   #scenario 2&3 tagged messages
capture_dirc_msg = []
capture_sing_txt = []


logss_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fetcheddata.txt")

# Initialize the Telegram client
client = TelegramClient(name, api_id, api_hash)

# Chat identifier of the group you want to listen to
group_chat_id = -1002081980221  # Replace with the actual chat ID fintrades

# 1001842161161 #heuid channel id#
#1002081980221
# 1001871775753 #testing api channel id#
# 1001904707643 fintrade
# 1002081980221 #swathi channel

destination_chat_id = -1001871775753

# Dictionary to store pending messages
pending_messages = {}


@client.on(events.NewMessage(chats=group_chat_id))  # Filter by group chat ID
async def newMessageListene(event):
    message_id = event.id
    reply_id = None
    message_text = event.message.text
    flag = 0

    message_text = message_text.replace('\n', ' ')
    
    bold_pattern = r'\*\*([^*]+)\*\*'
    italic_pattern = r'__([^_]+)__'


    message_text = re.sub(bold_pattern, r'\1', message_text)
    message_text = re.sub(italic_pattern, r'\1', message_text)


    if event.reply_to:
        reply_id = event.reply_to.reply_to_msg_id

    print(f"Received message: {message_id}, Reply To: {reply_id}, Reftext :{message_text}")
        
    # patternasfiv = r'(?i)(buy\s*)?\d{4,5}\s*(ce|pe)\s*(above|entry|abv|@)\s*\d{1,3}(\.\d{1,2})?'
    patternassi = r'(?i)(buy\s*)?((nifty|banknifty|finnifty|midcpnifty)\s*)?\d{4,5}\s*(ce|pe)\s*(above|entry|abv|@|around)\s*\d{1,3}(\.\d{1,2})?'

    match_assix = re.search(patternassi, message_text)

    if match_assix:
        matching_text = match_assix.group(0)
        message_text = matching_text
   

    if is_valid_condition(message_text):
        capture_or_msg.append(str(message_id) + "_+_" + message_text)
        capture_dirc_msg.append(str(message_id) + "_+_" + message_text) 
    elif re.search(patternassi, message_text):
        capture_sing_txt.append(str(message_id) + "_+_" + message_text)    
    elif contains_stpls_key(message_text):
        stpls =extract_numeric_stpl(message_text)
        stoploss = (f"STOPLOSS : {stpls}")
        if await client.send_message(destination_chat_id, stoploss):
            print("-- Stoploss sent --" + "\n" + stoploss)
        else:
            print("cannot send to personal channel through tag")
    
    for x in capture_or_msg:
        parts = x.split('_+_')
        if len(parts) == 2:
            org_msgd = int(parts[0])
            after = parts[1]
            prefix, numeric_part, option = extract_banknifty_info(after)
            sf1 = (f"I AM BUYING {prefix} {numeric_part} {option}")
            if reply_id == org_msgd:
                if is_valid_reply_condition(message_text):
                    numc_value = extractmy_value(message_text,numeric_part)
                    place = sf1 + "\n" + "\n" + "ABOVE " + numc_value
                    if await client.send_message(destination_chat_id, place):
                        flag = 1
                        print("-- order sent tag--" + "\n" + place)
                        with open(logss_path, 'a') as fileo:
                            fileo.write(f"-- order sent --\n\norder_date: {formatted_date}\norder_time: {datetime.now()}\n\n{place}\n\n\n")
                    else:
                        print("cannot send to personal channel through tag")

    for l in capture_dirc_msg:
        segs = l.split('_+_')
        if len(segs) == 2:
            msgido = int(segs[0])  # Fixed the variable name here
            msgfido = segs[1]
            prefix, numeric_part, option = extract_banknifty_info(msgfido)  # Fixed the variable here
            sfk = (f"I AM BUYING {prefix} {numeric_part} {option}")
            if msgido == int(message_id) - 1 and (reply_id == None):  # Fixed the variable name here ("reply_id == None")
                if is_valid_reply_condition(message_text) and not re.search(r'\b\d{4,5}\b', message_text) and not any(word.lower() in ["pe", "ce"] for word in message_text.split()):
                    numc_value = extractmy_value(message_text)
                    placetr = sfk + "\n" + "\n" + "ABOVE " + numc_value
                    if await client.send_message(destination_chat_id, placetr):
                        print("-- order sent dir --" + "\n" + placetr)
                        with open(logss_path, 'a') as fil:
                            fil.write(f"-- order sent --\n\norder_date: {formatted_date}\norder_time: {datetime.now()}\n\n{placetr}\n\n\n")
                    else:
                        print("cannot send to personal channel through dir")
                if len(capture_dirc_msg) == 2:
                    capture_dirc_msg.pop(0)
    
    for z in capture_sing_txt:
        sm = z.split('_+_')
        if len(sm) == 2:
            mido = int(sm[0])
            msgs = sm[1]
            # Default values
            insname = "BANKNIFTY"
            insvalue = None
            instype = None
            abvval = None

            # Define regex patterns to extract the required values
            prefix_pattern = r'(MIDCPNIFTY|BANKNIFTY|NIFTY|FINNIFTY)'
            strikeprice_pattern = r'(\d{4,5})'  # Matches 5 to 6 digits
            optiontype_pattern = r'(PE|CE)'
            entryprice_pattern = r'(?:(?:above|abv|entry|@|entry@|buy@|around)\s*(\d{1,3}(?:\.\d{1,2})?))'   # Matches 1 to 3 digits with optional decimal

            # Try to find prefix
            prefix_match = re.search(prefix_pattern, msgs ,re.IGNORECASE)
            
            if prefix_match:
                insname = prefix_match.group(1)


            # Try to find strikeprice
            strikeprice_match = re.search(strikeprice_pattern, msgs)
            if strikeprice_match:
                insvalue = strikeprice_match.group(1)

            instop = int(insvalue)
            if 15000 <= instop <= 28000 and insname!="FINNIFTY":
                insname = "NIFTY" 
            # Try to find optiontype
            optiontype_match = re.search(optiontype_pattern, msgs ,re.IGNORECASE)
            if optiontype_match:
                instype = optiontype_match.group(1)

            # Try to find entryprice
            entryprice_match = re.search(entryprice_pattern, msgs ,re.IGNORECASE)
            if entryprice_match:
                abvval = entryprice_match.group(1)

            sfo = (f'I AM BUYING {insname.upper()} {insvalue} {instype.upper()}\n\nABOVE {abvval}')
            if flag != 1:
                if await client.send_message(destination_chat_id, sfo):
                    print("-- order sent singletxt--" + "\n" + sfo)
                    with open(logss_path, 'a') as fila:
                        fila.write(f"-- order sent --\n\norder_date: {formatted_date}\norder_time: {datetime.now()}\n\n{sfo}\n\n\n")
                else:
                    print("cannot send to personal channel through tag")
        if len(capture_sing_txt) == 1:
                    capture_sing_txt.pop(0)


def is_valid_condition(message_text):
    # Check if the message contains "pe" or "ce"
    if any(keyword in message_text.lower() for keyword in ["pe", "ce"]):
        numeric_value = extract_numeric_value(message_text)
        
        # Check if numeric_value is not None and greater than 9999
        if numeric_value is not None and numeric_value > 3000:
            
            # Check if the message contains 1-3 digit numbers using regular expression
            if not re.search(r'\b\d{1,3}(?:\.\d{1,2})?\b', message_text):
                
                # Check if the message contains "ABOVE" (case-insensitive)
                if "above" not in message_text.lower() and "abv" not in message_text.lower():
                    return True
                
    return False


def is_valid_reply_condition(reply_text):
    return any(keyword in reply_text.lower() for keyword in ["above", "buy", "abv", "@", "entry", "entry@", "buy@" ,"enter@" , "around"])

def extract_numeric_value(message_text):
    words = message_text.split()
    for word in words:
        if word.isdigit() and len(word) >= 4:
            return int(word)
    return None

def extractmy_value(text,numrx):
    patterno = r'(?:around|above|abv|@|entry)[^\d]*(\d{1,3}(?:\.\d{1,2})?)?'
    matcho = re.search(patterno, text, re.IGNORECASE)
    if matcho:
        return matcho.group(1)
    else:
        return None

def extract_banknifty_info(message_text):
    numeric_part = None
    option = None
    words = message_text.split()
    for word in words:
        if word.isdigit() and len(word) >= 4:
            numeric_part = word
        if word.lower() == "pe" or word.lower() == "ce":
            option = word.upper()

    instanceop = int(numeric_part)
    # Normalize the prefix based on variations (case-insensitive)
    prefix = "BANKNIFTY"
    for candidate_prefix in ["MIDCPNIFTY", "FINNIFTY", "NIFTY"]:
        if any(candidate_prefix.lower() in message_text.lower() for candidate_prefix in ["midcpnif", "midc", "midcp", "mid"]):
            prefix = "MIDCPNIFTY"
        elif any(candidate_prefix.lower() in message_text.lower() for candidate_prefix in ["finnif", "finif", "fin", "finn", "finifty"]):
            prefix = "FINNIFTY"
        elif any(candidate_prefix.lower() in message_text.lower() for candidate_prefix in ["nif", "niff"]) and prefix != "FINNIFTY" and (15000 <= instanceop <= 28000) :
            prefix = "NIFTY"
    
    return prefix, numeric_part, option

def match_pattern_singtxt5(input_str):
    # Split the input string into words
    parts = input_str.split()

    # Check each part of the input against the expected format
    if parts[0].lower() != 'buy' or not parts[1].isdigit() or parts[2].lower() not in ['ce', 'pe'] or len(parts[3]) != 3 or not parts[4].isdigit():
        return False

    return True


def contains_stpls_key(input_string):
    # Define the keywords as a case-insensitive pattern
    keywords_pattern = re.compile(r'(STPLSS|STPLS|STOPLOSS|STPL|SL)', re.IGNORECASE)

    # Check if any of the keywords are present in the input string
    if re.search(keywords_pattern, input_string):
        return True
    else:
        return False

def extract_numeric_stpl(input_string):
    patterneo = r'(?:STPLSS|STPLS|STOPLOSS|STPL|SL)[^\d]*(\d{1,3})'
    matchoe = re.search(patterneo, input_string, re.IGNORECASE)
    if matchoe:
        return matchoe.group(1)
    else:
        return None

# Start the client
with client:
    print("Listening for new messages...")
    client.run_until_disconnected()
