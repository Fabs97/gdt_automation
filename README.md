# Script for automations in Munich's real Italian Board games Group

Code available for any inspections from anyone interested.

## Requirements

- Python3.12
- Install the `requirements.txt` using pip3
- Export the following variables

```sh
export BOT_TOKEN=<bot_token>
export CHANNEL_ID=<channel_id>
```

## Run

```sh
git clone (git@github.com:Fabs97/gdt_automation.git)[git@github.com:Fabs97/gdt_automation.git]
cd gdt_automation
python3 -m venv .env
source .env/bin/activate
pip3 install -r requirements.txt
python3 __main__.py
```

## Clean up

```sh
cd ..
sudo rm -r gdt_automation
```

Brought to you with ❤️ by Fabrizio Siciliano
