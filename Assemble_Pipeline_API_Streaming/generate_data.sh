#!/bin/bash

# User 1- default event
docker-compose exec mids \
  ab \
    -n 10 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/

# User1 - Purchase sword event - use default sword type
docker-compose exec mids \
  ab \
    -n 10 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/purchase_a_sword

# User 1 - Earn more gold event
docker-compose exec mids \
  ab \
    -n 25 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/earn_more_gold

# User 1 - join a guild event (default guild name)    
docker-compose exec mids \
  ab \
    -n 2 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/join_a_guild
    
# User 1 - purchase a potion with POST event
docker-compose exec mids \
  ab \
    -n 3 \
    -H "Host:user1.comcast.com" \
    -T "application/json" \
    -p /w205/project-3-latuyetmai/post.txt \
    http://localhost:5000/purchase_a_potion
    
# User 1 - purchase a different sword type with GET event
docker-compose exec mids \
  ab \
    -n 5 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/purchase_a_sword/titanium
    
# User 1 - join another guild event    
docker-compose exec mids \
  ab \
    -n 2 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/join_a_guild/kungfu_chicken
    
# User 1 - Earn more gold event
docker-compose exec mids \
  ab \
    -n 10 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/earn_more_gold
    
# User 1 - purchase a different potion with GET event
docker-compose exec mids \
  ab \
    -n 1 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/purchase_a_potion/fly/5
    
# User 1 - purchase a different potion with GET event
docker-compose exec mids \
  ab \
    -n 2 \
    -H "Host: user1.comcast.com" \
    http://localhost:5000/purchase_a_potion/poison/4 

# User 2 - default event
docker-compose exec mids \
  ab \
    -n 10 \
    -H "Host: user2.att.com" \
    http://localhost:5000/

# User2 - Purchase sword event
docker-compose exec mids \
  ab \
    -n 5 \
    -H "Host: user2.att.com" \
    http://localhost:5000/purchase_a_sword/silver

# User 2 - Earn more gold event
docker-compose exec mids \
  ab \
    -n 30 \
    -H "Host: user2.att.com" \
    http://localhost:5000/earn_more_gold

# User 2 - join a guild event (default guild name)    
docker-compose exec mids \
  ab \
    -H "Host: user2.att.com" \
    http://localhost:5000/join_a_guild
    
# User 2 - join another guild event    
docker-compose exec mids \
  ab \
    -H "Host: user2.att.com" \
    http://localhost:5000/join_a_guild/kungfu_chicken
    
# User 2 - purchase a potion with POST event
docker-compose exec mids \
  ab \
    -n 3 \
    -H "Host: user2.att.com" \
    -T "application/json" \
    -p /w205/project-3-latuyetmai/post.txt \
    http://localhost:5000/purchase_a_potion
    
# User 2 - purchase a potion with GET event
docker-compose exec mids \
  ab \
    -n 2 \
    -H "Host: user2.att.com" \
    http://localhost:5000/purchase_a_potion
    
# User2 - Purchase sword event
docker-compose exec mids \
  ab \
    -H "Host: user2.att.com" \
    http://localhost:5000/purchase_a_sword/magic
    
# User 2 - join another guild event    
docker-compose exec mids \
  ab \
    -H "Host: user2.att.com" \
    http://localhost:5000/join_a_guild/clumsy_witch
    
# User 2 - Earn more gold event
docker-compose exec mids \
  ab \
    -n 5 \
    -H "Host: user2.att.com" \
    http://localhost:5000/earn_more_gold
    
# User 2 - purchase a different potion with GET event
docker-compose exec mids \
  ab \
    -n 1 \
    -H "Host: user2.att.com" \
    http://localhost:5000/purchase_a_potion/love/6
    
# User 2 - purchase a different potion with GET event
docker-compose exec mids \
  ab \
    -n 2 \
    -H "Host: user2.att.com" \
    http://localhost:5000/purchase_a_potion/lucky/7 