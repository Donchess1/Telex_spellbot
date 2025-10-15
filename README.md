##DESCRIPTION
This is a hang game build with DRF, for telex integration, with the sole aim to unwind

## Key Features
1. Acceptance of input from users to start, guess or end the game
2. back end modification
3. return of result to user
---

## Installation
1. Clone the Repository
git clone https://github.com/telexintegrations/Telex_spellbot.git
cd Telex_spellbot
2. Create a Virtual Environment
python3 -m venv venv
source venv/bin/activate  
3. Install Dependencies
pip install -r requirements.txt

## Installation on Telex
log into the telex app
Create a channel and copy the channel_Id.
Create a .env file in the project file, create and paste the "Channel_ID = copied variable".
In the telex app, add new app and enter the json url ="https://telex-spellbot.onrender.com/api/markdown/"
Switch the app on to activate the integration

## Playing the game
start the game with "!start"
make guesses by entering an alphabet and pressing enter
exit the game at anytime before exhausted attempt chances with "!exit"
