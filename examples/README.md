# Examples
This directory contains code examples and small projects you might want to re-use.

[basic_bot_main.py](./basic_bot_main.py) and [basic_script_main.py](./basic_script_main.py): contain code samples to let you start a new bot / script when you know how to use the olvid-bot module.

# Setup
To start using any of our example projects you will need a properly set up Olvid daemon and a client key to connect to it.
If this is not already the case, please follow our [INSTALL procedure](../quickstart/INSTALL.md)

You should already have downloaded this repository and can start by going to the example directory you want to run
```
cd bot_basic_example
```

You can write your client key in a `.client_key` file in your working directory,
```bash
echo -n yourClientKey > .client_key
```
or if you prefer, define an environment variable.
```bash
export OLVID_CLIENT_KEY=yourClientKey
```

Then you will also need to install project dependencies. We recommend that you set up a virtual environment for this project.
```bash
(Optional)
python3 -m venv .venv
source .venv/bin/activate
```
Then install dependencies
```bash
pip3 install -r requirements.txt
```

You can finally start your program.
```bash
python3 main.py
```
If the program is a bot it will run forever, you will need to use `Ctrl + C` to stop it and restart it every time you edit the code.

⚠️ Remember to re-export your client key in environment every time you start a new terminal session.
You will also need to re-use venv:
```bash
source .venv/bin/activate
```

# Projects description
#### [Bot Basic Example](./bot_basic_example)
The first project to have a look at when you start using the olvid-bot module. It implements a few mechanisms needed to write your first chatbot. 

#### [Bot Broadcast](./bot_broadcast)
A simple but fully packaged project. This program starts an HTTP server (on port 8080 by default) and send the content of any request it receives in every discussion it participates in (direct discussions or group discussions).

#### [Bot Webhook](./bot_webhook)
A more complex and packaged project. This bot creates a discussion-specific webhook url for each of its discussions. You can then use such an url to post messages and/or attachments to a specific discussion.

It can be interesting to check what was necessary to develop and add to get a nicer and smoother user experience.
