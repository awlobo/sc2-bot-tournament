"""

===========================================================
====                     BASIC BOT                     ====
===========================================================

This is a simple bot that does the following:
- Harvest minerals
- Create a Supply Depot (required to build Barracks)
- Create Barracks (required to train Marines)
- Start training Marines
- When there are 5 Marine units available, they are
  commanded to attack the enemy base
- Keep creating Marine units

As you will quickly see if you run this bot, this strategy
is far from effective (you will lose), but this bot is
only for demonstration purposes.

Also, this is NOT by any means a good example on how to
code a bot.

"""

import sc2
from sc2.bot_ai import BotAI
from sc2.player import Bot, Computer
from sc2.ids.unit_typeid import UnitTypeId


# Rename this class to your bot's name
class MyBot(BotAI):

    # This function is executed in an infinite loop during the game
    async def on_step(self, iteration):
        # Check if we have a command center to use as a reference position for other buildings
        if self.townhalls(UnitTypeId.COMMANDCENTER):
            command_center = self.townhalls(UnitTypeId.COMMANDCENTER).first
        else:
            # If our command center got destroyed, do nothing and die with pride
            return

        # Check if we still have no Supply Depot (this is required to build Barracks)
        # https://starcraft.fandom.com/wiki/Barracks#StarCraft_II
        if not self.structures(UnitTypeId.SUPPLYDEPOT):
            # Check if we can afford to build a Supply Depot and if there is none in progress
            if self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                # Build a Supply Depot near the Comand Center
                await self.build(UnitTypeId.SUPPLYDEPOT, near=command_center.position)
        else:
            # Check if we have a Supply Depot, but still no Barracks
            if not self.structures(UnitTypeId.BARRACKS):
                # Check if we can afford to build Barracks and if there is none in progress
                if self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
                    # Build Barracks near the Comand Center
                    await self.build(UnitTypeId.BARRACKS, near=command_center.position)

        # Check if we already have Barracks
        if self.structures(UnitTypeId.BARRACKS):
            # Check if we can afford to bui a Marine unit
            if (self.can_afford(UnitTypeId.MARINE)):
                # Get the first Barracks structure
                barracks = self.structures(UnitTypeId.BARRACKS).first

                # Train a Marine unit
                barracks.train(UnitTypeId.MARINE)

        # Check if we have at least 5 Marine units that are doing nothing
        if self.units(UnitTypeId.MARINE).idle.amount >= 5:
            # Send all of them to attack the enemy base
            for unit in self.units(UnitTypeId.MARINE).idle:
                unit.attack(self.enemy_start_locations[0])


# Here is where the war starts: your bot vs te computer in an Easy setting
sc2.run_game(
    sc2.maps.get("AcropolisLE"),  # The map is defined here
    [Bot(sc2.Race.Terran, MyBot()), Computer(sc2.Race.Terran, sc2.Difficulty.Easy)],
    realtime=False,  # This makes the game run faster
    game_time_limit=3600    # This sets the time limit in seconds before declaring a tie
                            # In fast mode 1 real minute equals to 10 game minutes, so
                            # we set the limit to 1 game hour (6 real minutes)
)
