# Starcraft 2 bot tournament

## What is this?

Starcraft II is a very popular real-time strategy game in which you gather resources to create an army and fight other armies.

For quite some time now, nerds from all over the world are writing bots that interact with the game to automatically command their armies and fight against other bots.

This is a simple guide to get you started by showing you how to write a bot and send it to war.

In order for you to interact with the game, a very cool Python library has been created: https://github.com/BurnySc2/python-sc2

## Tournament

The goal is to create a tournament with friends so you can put your bot to fight with others and prove that yours is the best one!

### Description

- It’s a [Round Robin tournament](https://en.wikipedia.org/wiki/Round-robin_tournament); all bots vs all bots.
- Only one bot can win.
- The map for all matches will be **Acropolis LE**.
- The replay file for every match will be saved for further review.
- Every match has a time limit of 6 minutes (equivalent to 1 hour in the game). After that, it’s considered a tie.
- The winner will be the bot that wins the most matches.

### Rules

- It’s forbidden to use an existing bot (copy/paste). Write your own!
- Only one bot per author will be eligible.
- All bots must use the [Terran](https://starcraft.fandom.com/wiki/Terran) race.
- If a bot gives an error, loses the match.
- Players will not be able to see the code of the rest of the bots until the tournament has finished.
- Players must give a name to their bot.
- Bots cannot require special Python libraries other than the ones included by default and `python-sc2` (the game interface).

## Setup

Enough talking. Let's make this thing work.

### 1. Install the game

You can download and install Starcraft 2 from the [official site](https://starcraft2.com/) and clicking the "Play free now" button.

The game works natively in Windows and Mac. Linux users get the best experience by installing the Windows version of StarCraft II with [Wine](https://www.winehq.org/). Linux user can also use the [Linux binary](https://github.com/Blizzard/s2client-proto#downloads), but it's headless so you cannot actually see the game.

### 2. Install the map

In this repo you will find the map we will use for the tournament. It's called **Acropolis LE** and you can find it at `maps/AcropolisLE.SC2Map`.

To install it, download the `AcropolisLE.SC2Map` file and place it into the root of the Starcraft `Maps` directory: `install-dir/Maps/AcropolisLE.SC2Map`.
If the `Maps` directory does not exist, create it.
**e.g.** For Mac users, the `Maps` directory must be at `/Applications/StarCraft II/Maps`

### 3. Install Python

This project uses Python 3. There is a very high chance that you already have it installed in your computer.
To confirm this, run:

`python3 -V`

If you see a version, all is good. If not, please [install Python 3](https://www.python.org/downloads/) to continue with this guide.

### 4. Create virtual environment

It is always a good practice to create a [virtual environment](https://docs.python.org/3/tutorial/venv.html) for every Python project, so you don't pollute the global space with different versions of libraries.

To do this, got to the directory where you want to keep your bot and run:

`python3 -m venv env`

This will create a folder called `env` that contains the python binaries and libraries.

Once you have created your virtual environment, it's time to **activate** it. Run:

`source env/bin/activate`

By doing this you are telling your computer to use the Python version and the libraries that are inside the `env` folder instead of the global ones.

### 5. Install the `python-sc2` library

Now that you are in your project's directory and you have activated your virtual environment, it's time to install the library that will give us the tools to interact with the game:

`pip install burnysc2`

This command will download and install the `python-sc2` library in your virtual environment. That's all you need! We can start using it now.

### 6. Run the basic bot

Whit this guide I've included a very basic bot that demonstrates some simple actions that you can perform. You will quickly realise that it's not a good bot because it can't win even against the computer in an Easy setting, but it's purpose is only to show you some of the stuff you can do.

You should now be able to run it by executing:

`python bots/basic.py`

If all goes well, you should see that the Starcraft game is started and you can see the bot doing its job. This can take a while depending on your computer, please be patient.

You will realise that the speed is way faster than real-time. This is configured like that so the matches are not that long to watch.

### 7. Write your own bot

Ok, you now have everything you need to start coding your killer bot.

I have included a "template bot" with this guide, so you have a starting point. You can find it in `templates/start_here.py`.

As per the rules, you have to give your bot a name, so copy or rename the `start_here.py` file to `<your_bot>.py` and inside the file replace the class name `MyBot` with the name you want.

You can execute this bot as it is, but since there are no instructions on what it should do, it will just stay there waiting for its unavoidable death. It's time for you to give it life!

You can see that at the end of the file there is an instruction to run the match:

``` python
sc2.run_game(
    sc2.maps.get("AcropolisLE"),
    [Bot(sc2.Race.Terran, MyBot()), Computer(sc2.Race.Terran, sc2.Difficulty.Easy)],
    realtime=False
)
```

In there you are specifying that the match will take place in the map `AcropolisLE`, with your bot against the computer with a difficulty set to `Easy`, and that the match will play fast.

Change the difficulty to `Medium` or to `Hard` when your bot can nadle it. You can also set `realtime` to `True` if you want to see what's going on in real time.

## Resources

There are a few sources where you can see examples for your bot and documentation on how to use the `python-sc2` library and what are the rules for Starcraft:

- [`python-sc2` library documentation](https://burnysc2.github.io/python-sc2/docs/index.html)
- [`python-sc2` library code](https://github.com/BurnySc2/python-sc2)
- [`python-sc2` library examples](https://github.com/BurnySc2/python-sc2/tree/develop/examples)
- [Starcraft 2 wiki](https://starcraft.fandom.com/wiki/StarCraft_Wiki)
  - [Terran race](https://starcraft.fandom.com/wiki/Terran)
  - [Terran units](https://starcraft.fandom.com/wiki/List_of_StarCraft_II_units#Units)
  - [Terran Structures](https://starcraft.fandom.com/wiki/List_of_StarCraft_II_units#Structures)

## Now what?

Once you have your bot ready, contact the tournament organizers so they can tell you how to proceed.
