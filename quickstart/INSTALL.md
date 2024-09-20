**Install Olvid Bots**
====================

# Prerequesite
In this installation guide we will use Docker and Python3.

You can install docker here: https://docs.docker.com/engine/install/

We will need at least Python3.10 to run use olvid-bot module. If your python install is older you will have to update it.
On macOS, we recommend using homebrew. To install a newer Python version, run `brew install python3`.

# Introduction

To run any Olvid bot, you'll need to deploy a daemon, which serves as the server that your code interacts with. This daemon is a gRPC server embedded in a Docker container and can be thought of as an Olvid application that you can control with code.

As for any Olvid client application, you will need to set up your daemon after starting it for the first time. This implies to create an identity (a profile) and to invite this new identity as a contact in your own Olvid app. To facilitate this process, we will use a Command-Line Interface (CLI).

Once set up, you can start interacting with your daemon. The easiest way to do so is by using our Python module, available via `pip`. Alternatively, you can compile protobuf files in any supported language, but this approach won't be covered in this procedure.

# Basic daemon installation
### The daemon container
The daemon image is available on Docker Hub: https://hub.docker.com/r/olvid/bot-daemon 

You can run the daemon using a `docker run` but it is generally more convenient to use docker compose because the daemon needs data persistence (all the Olvid client databases are stored by the daemon). 

To set up the daemon create a `docker-compose.yaml` file similar to this:
```yaml
services:
  daemon:
    image: olvid/bot-daemon
    environment:
      - OLVID_ADMIN_CLIENT_KEY_CLI=SetARandomValue
    ports:
      - 50051:50051
    volumes:
      - ./data:/daemon/data
      - ./backups:/daemon/backups
```

We configure two volumes:
- one to store all the daemon files and databases,
- one to store backups.

We also need to pick a key that we will use in the CLI to grant it admin privileges and fully manage the daemon. This will allow the CLI to create identities. You can generate this key using the `uuidgen` command.

You can now run `docker compose up -d daemon` to start the daemon in background.

### Preparing the daemon
To set up our daemon instance, we'll use the Olvid Command-Line Interface (CLI), which is embedded in our Python client module, available on `pip`.

First, install the olvid package:
```
pip3 install olvid-bot
```

Then set up the admin client for cli. It's the client key you set previously in daemon environment. You set in as environment variable:
```bash
export OLVID_ADMIN_CLIENT_KEY=generatedKey
```
But we recommend that you write it in a file named `.admin_client_key`:
```bash
echo generatedKey > .admin_client_key
```

Then, run the CLI in interactive mode:
```
olvid-cli
```
(If the `olvid-cli` binary is not available, you can run `python3 -m olvid-bot` to start the CLI.)

This CLI is interactive and provides many commands to perform actions on the daemon. At any time, if you need help, you can pass the `--help` flag after your command to see the command's usage and options.
As an example:
- `--help` will print every command *trees*.
- `message --help` will show you available commands for the message tree.
- `message send --help` will show you arguments and options for the message send command.

For now, we only want to create a new bot identity. This will also generate a client key to let our future program connect to the daemon, and optionally add this bot as a contact. 
These three steps can be achieved with just one command: `identity new`.  Then you can follow the instructions on the screen.

Here is a full example with comments. User inputs start with a *>* and comments with a *#*.
```bash
# We will create a new identity. LastName, Position, and Company are optional. These details can be updated later.
0 > identity new FirstName LastName Position Company
# A client key to connect using this identity is automatically created; you must keep it somewhere.
identity creation > Here is your client key to connect to daemon with this identity:
AAAAAAAA-BBBB-AAAA-AAAA-AAAAAAAAAAAA
# You can directly add this new identity to your contacts. This step is optional but necessary if you want to interact with your bot.
identity creation > Do you want to add this identity to your contacts ? (y/N)
>yes
# This is an invitation link for this new identity. You can open it in your browser and scan the QR code with your mobile application.
# You can also copy it and import it into your desktop application.
identity creation > Send an invitation to this invitation link: https://invitation.olvid.io/#........
# From now, CLI is waiting for a new invitation to arrive ...
# When your invitation arrives, the flow continues.
identity creation > Please enter sas code displayed on the other device
# Enter the four-digit code visible on your device.
> 0000
# Enter the following code in your device
identity creation > Please enter this sas code on the other device: 1111
# Flow had been completed
Now using identity: 1
You can now send messages to YOUR NAME in discussion 1
1 >
```

As you can see, the command prompt changed and is now prefixed with a `1` instead of a `0`. This is because the CLI is now automatically using this new identity, designated by its ID: `1`. Most commands you will run from now will be executed using this identity.
For example if you list contacts using the `contact get` command you will see the contacts of this specific identity.

A daemon can host more than one identity. In that case, you'll need to change the identity in use with the `identity current` command.

To learn more about the CLI and its commands, see: [CLI DOC LINK]()

### Your first bot
To allow your bot to authenticate when connecting to the daemon, it will need the client key that was displayed earlier. If you've lost it, you can list registered client keys using the CLI: `olvid-cli key get`.

This client key can be passed to your bot in three different ways:
* As an environment variable: `export OLVID_CLIENT_KEY=MyClientKey`
* In a file: `echo -n MyClientKey > .client_key`
* Directly in code: pass `client_key="MyClientKey"` when creating your OlvidClient or OlvidBot instance

Now, let's write a minimalist bot in Python in a file named `main.py`. 

```python
# we use coroutines to run code asynchronously
import asyncio
# elements we need in olvid-bot module
from olvid import OlvidBot, datatypes


# we write a class extending the OlvidBot base class
class MyFirstBot(OlvidBot):
	# we override this specific method, called every time our bot receives a message
	async def on_message_received(self, message: datatypes.Message):
		print(f"> {message.body}")
		# when a message arrives we post another message in this discussion with the same content
		await message.reply(body=message.body)


async def main():
	# create the bot
	bot: MyFirstBot = MyFirstBot()
	print("Bot is ready!")
	# In this case this method wait forever
	await bot.wait_for_listeners_end()


# the way to start your program in python asynchronous paradigm
asyncio.run(main())
```

This code requires the `olvid-bot` package, which you previously installed using `pip`. If not, you can install it using `pip3 install olvid-bot`.

To start your bot, run `python3 main.py`. You will need your daemon to be up and running, and your client key to be set in your environment if that's the method you chose.

When your bot has started, you can send it a message from your mobile or your desktop app to check that everything is working properly.

Well done, you just created your first Olvid Bot 🤖!

We can now edit this code. For example, our bot can react to the original message and remove all 'e' characters from the original body:

```python
# python module use coroutine to run code asynchronously
import asyncio
# elements we need in olvid-bot module
from olvid import OlvidBot, datatypes


# we write a class extending the OlvidBot base class
class MyFirstBot(OlvidBot):
	# we override this specific method, called every time our bot receive a message
	async def on_message_received(self, message: datatypes.Message):
		print(f"> {message.body}")
		# !!! Like the original message
		await message.react("👍")
		# edit original body
		new_body: str = message.body.replace("e", "").replace("E", "")
		# when a message arrives we post another message in this discussion with the new content
		await message.reply(body=new_body)


async def main():
	# create the bot
	bot: MyFirstBot = MyFirstBot()
	print("Bot is ready!")
	# In this case this method wait forever
	await bot.wait_for_listeners_end()


# the way to start your program in python asynchronous paradigm
asyncio.run(main())
```

Once you edited your code, just kill your previous bot program using `Ctrl + C` and restart it with: `python3 main.py`.

To go further check our other [examples](../examples) or see our Python module [documentation](https://github.com/olvid-io/Olvid-Bot-Python-Client).

### Deploy in production

When developing and testing your application, it's usually more convenient to use your local Python installation and a daemon container exposed to your host system. However, for a stable environment in production, we recommend using our ready-to-use Docker image.

You can find this image on Docker Hub: <https://hub.docker.com/r/olvid/bot-python-runner>

This image embeds our Python module and is set up to execute your code easily. We will mount our code as a volume, and the image will manage dependencies and run our bot for us. You just need to put your code in a directory named `app`. You can put as may as file as you want, but your program must be started from a file named `main.py`.
If you need extra Python dependencies (other than the `olvid-bot` module) add a `requirements.txt` file next to you `main.py` they will be automatically downloaded when the container starts.

Because we will need to set up our daemon, we will need to run CLI commands. To achieve that we will need to create a new cli service in our docker compose file. We cannot use our local CLI as before if our daemon instance is not exposing port 50051.

Here is the associated `docker-compose.yaml` file:

```yaml
services:
  daemon:
    image: olvid/bot-daemon
    environment:
      # TODO generate a random client key with `uuidgen` command and set it here and in the cli service
      - OLVID_ADMIN_CLIENT_KEY_CLI=SetARandomValue
    volumes:
      - ./data:/daemon/data
      - ./backups:/daemon/backups
    restart: unless-stopped

  bot:
    image: olvid/bot-python-runner
    environment:
      # TODO set OLVID_CLIENT_KEY with the client generated when creating identity on daemon
      - OLVID_CLIENT_KEY=SetMe
      - DAEMON_HOSTNAME=daemon
    volumes:
      - ./app:/app:ro
    restart: unless-stopped
    depends_on:
      - daemon

  cli:
    image: olvid/bot-python-runner
    environment:
      # TODO use the same value as in the daemon OLVID_ADMIN_CLIENT_KEY_CLI
      - OLVID_ADMIN_CLIENT_KEY=
      - DAEMON_HOSTNAME=daemon
    command: ["cmd", "olvid-cli"]
    stdin_open: true
    tty: true
    # share a volume where you can put photos to set up identity profile photos
    volumes:
      - ./photos:/photos
    depends_on:
      - daemon
    # You may use a profile as the CLI only needs to be started manually
    profiles:
      - "cli"
```

When your `docker-compose.yaml` file is ready, generate a client key for the CLI. You can generate it using the `uuidgen` bash command. Then set the generated UUID as the `OLVID_ADMIN_CLIENT_KEY_CLI` value in the daemon environment and as the `OLVID_ADMIN_CLIENT_KEY` value in the cli environment.

If it's a new installation, leave the `OLVID_CLIENT_KEY` empty in the bot environment; otherwise, set your bot client key and jump to the next step.

If it's a new installation we will need to create a new identity and set up the daemon. To start CLI use this command: `docker compose run --rm -it cli`. Then you can follow the procedure described here [Prepare Daemon Link] to create a new identity, retrieve your client key and add your new bot in your contacts.
Once you have your client key, set it in `OLVID_CLIENT_KEY` for the bot environment.

Before you start your bot, check that you created a directory named `app` and you added your `main.py` and all the code you need inside.
Then you can start your bot with this command:
```
docker compose up -d bot
```

If you need to check any service log use this:
```
docker compose logs -f [daemon|bot]
```

# Create your bot docker image
**To write**

# Set up your bots in Keycloak
**To write**

# Use cli to debug
**To write**

