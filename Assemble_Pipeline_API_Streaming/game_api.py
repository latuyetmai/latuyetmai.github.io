#!/usr/bin/env python
import json
from kafka import KafkaProducer
from flask import Flask, request

app = Flask(__name__)
producer = KafkaProducer(bootstrap_servers='kafka:29092')


# Sword type library, store all sword types and value of the swords
sword_types = {"steel":1, "silver":2, "gold":3, "titanium":4, "magic":20}
potion_types = {"speed":2}
# User libary, store all users and there golds, all users start with 20 golds
users = {"undefined":20}
# Guild library, store all guild names and the members in the guild
guilds = {"holy_ramen": ["HairyTheCat.meow.com"]}


# Function to send event to kafka
def log_to_kafka(topic, event):
    # Add the headers to the event dictionary
    event.update(request.headers)
    # Send event dictionary to kafka using json
    producer.send(topic, json.dumps(event).encode())

    
@app.route("/")
def default_response():
    global users   
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
        
    default_event = {'event_type': 'default', 
                     'gold_count': users[user],
                     'description': "",
                     'value': ""}
    log_to_kafka('events', default_event)
    
    return "This is the default response!\n"


@app.route("/purchase_a_sword")
def purchase_a_sword():
    global users
    global sword_types
    
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
       
    # Default with buying a steel sword
    sword_type = "steel"
    sword_value = sword_types[sword_type]
    
    # Update the amount of gold of player after buying a sword
    users[user] -= sword_value
    # Do not let player buy a sword if running out of gold
    if users[user] < 0:
        users[user] = 0
        sword_type = "Not_enough_gold_to_buy"
        sword_value = 0
        
    # Send purchase_sword event to kafka
    purchase_sword_event = {'event_type': 'purchase_sword', 
                            'gold_count': users[user], 
                            'description': sword_type,
                            'value': sword_value}    
    log_to_kafka('events', purchase_sword_event)
    
    # Return
    if sword_type == "Not_enough_gold_to_buy":
        return "Not enough gold to buy a sword!\n"
        
    return "Sword Purchased!\n"

@app.route("/purchase_a_sword/<sword_type>")
def get_sword_type(sword_type):
    global users
    global sword_types
    
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
    
    # Update sword type & value for GET method
    sword_type = str(sword_type)
    sword_value = sword_types.get(sword_type, 1)
    
    # Update player's gold count after purchasing a sword
    users[user] -= sword_value 
    # Do not let player buy a sword if running out of gold
    if users[user] < 0:
        users[user] = 0
        sword_type = "Not_enough_gold_to_buy"
        sword_value = 0
    
    # Send purchase_sword event to Kafka
    purchase_sword_event = {'event_type': 'purchase_sword', 
                            'gold_count': users[user], 
                            'description': sword_type,
                            'value': sword_value}     
    log_to_kafka('events', purchase_sword_event)
    
    # return
    if sword_type == "Not_enough_gold_to_buy":
        return "Not enough gold to buy a sword!\n"
    else:
        #Add new sword type in the library if not exist
        if sword_type not in sword_types.keys():
            sword_types.update({sword_type:sword_value})    
    return "Sword Purchased!\n"

@app.route("/join_a_guild")
def join_a_guild():
    global users
    global guilds
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
        
    # Add guild name to the library if not found
    if user not in guilds["holy_ramen"]:
        guilds["holy_ramen"].append(user)
    
    member_count = len(guilds["holy_ramen"])
    
    # Send event to kafka
    join_guild_event = {'event_type': 'join_guild',
                        'gold_count': users[user],
                        'description': 'holy_ramen',
                        'value': member_count}
    log_to_kafka('events', join_guild_event)

    return "Guild Joined!\n"

@app.route("/join_a_guild/<name>")
def join_a_guild_name(name):
    global users
    global guilds
    name = str(name)
    
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
        
    if name not in guilds.keys():
        guilds.update({name:list()})
    
    if user not in guilds[name]:
        guilds[name].append(user)
        
    member_count = len(guilds[name])
    
    join_guild_event = {'event_type': 'join_guild',
                        'gold_count': users[user],
                        'description': name,
                        'value': member_count}
    log_to_kafka('events', join_guild_event)
    return "Guild Joined!\n"

@app.route("/earn_more_gold")
def earn_more_gold():
    global users   
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
    
    users[user] += 1
    earn_gold_event = {'event_type': 'earn_gold',
                       'gold_count': users[user],
                       'description': "", 
                       'value': ""}
    log_to_kafka('events', earn_gold_event)
    return "Earned one Gold!\n" 

@app.route("/purchase_a_potion", methods=['GET','POST'])
def purchase_a_potion():
    global users
    global potion_types
    
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
    
    if request.method == 'POST':
        # POST request:
        data = request.get_json()
        potion_type = str(data.get('potion_type','speed'))
        potion_value = data.get('potion_value',2)
        try:
            potion_value = int(potion_value)
        except:
            potion_value = 2
            
    elif request.method == 'GET':
        # GET request:
        potion_type = "speed"
        potion_value = 2

    # Update the amount of gold of player after buying a potion
    users[user] -= potion_value
    # Do not let player buy a potion if running out of gold
    if users[user] < 0:
        users[user] = 0
        potion_type = "Not_enough_gold_to_buy"
        potion_value = 0
        
    # Send purchase_potion event to kafka
    purchase_potion_event = {'event_type': 'purchase_potion', 
                            'gold_count': users[user], 
                            'description': potion_type,
                            'value': potion_value}
    log_to_kafka('events', purchase_potion_event)
    
    # Return
    if potion_type == "Not_enough_gold_to_buy":
        return "Not enough gold to buy!\n"
    else:
        # Add potion type to the libary
        if potion_type not in potion_types.keys():
            potion_types.update({potion_type:potion_value})
        
    return "Potion Purchased!\n"

@app.route("/purchase_a_potion/<potion_type>/<potion_value>")
def purchase_potion_type(potion_type, potion_value):
    global users
    global potion_types
    
    # Look for user account in the library
    user = str(request.headers.get("Host","undefined"))
    # If user not found, then add to the user library with starting golds = 20
    if user not in users.keys():
        users.update({user:20})
    
    # Update potion type & value for GET method
    potion_type = str(potion_type)
    try:
        potion_value = int(potion_value)
    except:
        potion_value = 2
    
    # Update player's gold count after purchasing
    users[user] -= potion_value 
    # Do not let player buy if running out of gold
    if users[user] < 0:
        users[user] = 0
        potion_type = "Not_enough_gold_to_buy"
        potion_value = 0
    
    # Send event to Kafka
    purchase_potion_event = {'event_type': 'purchase_potion', 
                            'gold_count': users[user], 
                            'description': potion_type,
                            'value': potion_value}
    log_to_kafka('events', purchase_potion_event)
    
    # return
    if potion_type == "Not_enough_gold_to_buy":
        return "Not enough gold to buy!\n"
    else:
        # Add new potion in the library if not exist
        if potion_type not in potion_types.keys():
            potion_types.update({potion_type:potion_value})    
    return "Potion Purchased!\n"