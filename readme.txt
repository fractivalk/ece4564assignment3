ECE 4564
Team 13
Assignment 3

Nicholas Phan
Eric Walters
Wes Hirshiemer
Colin Grundey

Project Contributions:
Eric - Canvas Interaction/Services.py
Nicholas - Custom API/Services.py
Wes - ZeroConf/LED.py
Colin - LED and GPIO Configuration/LED.py

Current Authentication Credentials
1. username = apple, password = pie
2. username = banana, password = cake
3. username = orange, password = popsicle

Example curl commands for custom API (4 Total - 2 GET, 2 POST)

/PartyInfo (GET)
    curl -u username:password "ipaddress:5000/PartyInfo"
    
/PartyInfo/<char_name> (GET)
    curl -u username:password "ipaddress:5000/PartyInfo/charactername(nospaces)"
    
/PartyInfo/AddCharacter (POST)
    curl -u username:password -H "Content-Type: application/json" -X POST -d "{\"name\":\"<char_name>\", "\"level\:\"<char_lvl>\", "\class":\"<char_class>\"}" "ipaddress:5000/PartyInfo/AddCharacter"
    \(only for windows)
    
/PartyInfo/<char_name>/AddSkill (POST)
    curl -u username:password -F "skill=nameofskill" -X POST "ipaddress:5000/char_name/AddSkill"
    
Canvas Upload and Download operates as specified in the documentation (handles both GET and POST requests)
Example download:
    curl -u username:password "ipaddress:5000/Canvas?file=<file_name>&operation=download"
Example upload (upload file must be in same directory as services.py)
    curl -u username:password "ipaddress:5000/Canvas?file=<file_name>&operation=download"