# discord-game-chat-forwarding

- Game: Diablo Immortal
- For simultaneously forwarding chat between in-game clan chat and discord. 

## preparation

- An alt at a minimum of level 43, joined the clan.
- A spare PC.
- A discord bot, check how to [create a discord bot](https://discordpy.readthedocs.io/en/stable/discord.html).
- The token for the bot needs to be saved in `./resources/token.txt`
- Tested in python 3.8.
- Game setting: lowest possible graphics, othewise by default.

## Usage

- On the spare PC, log in the alt account. On the left side, make sure the first quest teleports you somewhere.
- Open the chat window (the pop up one on the right), and switch to clan channel.
- Run in shell `python3 discord_.py`.
- In discord, invite the bot using the bot's link (see above link). 
- Create a new channel (suggested), assign the bot to the channel.
- When the bot is running, type `--config receiving channel`
