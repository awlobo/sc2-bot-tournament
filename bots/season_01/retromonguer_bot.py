from sc2.constants import *
from numpy.core import numeric
from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.units import Units


class RetromonguerBot(BotAI):

    # Loop
    async def on_step(self, iteration):

        ### CONFIG

        maxSupplyDepots: numeric = 5

        maxMarineUnits: numeric = 21
        marineNumberPack: numeric = 7
        maxReaperUnits: numeric = 30
        reaperNumberPack: numeric = 5
        maxMarauderUnits: numeric = 2000
        marauderNumberPack: numeric = 1

        ### CHECK PHASE

        # If we do not have a command center build one
        if self.townhalls(UnitTypeId.COMMANDCENTER).amount <= 0:
            await self.build(UnitTypeId.COMMANDCENTER, near=self.all_own_units.center)

        # Lower supply depots to not be in the middle
        if (self.structures(UnitTypeId.SUPPLYDEPOT).ready):
            for sd in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
                self.do(sd(MORPH_SUPPLYDEPOT_LOWER))

        ### BUILD PHASE

        # Loop over all townhalls that are 100% complete
        for th in self.townhalls.ready:
            if (
                self.can_afford(UnitTypeId.SUPPLYDEPOT)
                and (self.structures(UnitTypeId.SUPPLYDEPOT).amount < maxSupplyDepots)
                and not self.already_pending(UnitTypeId.SUPPLYDEPOT)
                ):
                # Build a Supply Depot near the Comand Center
                await self.build(UnitTypeId.SUPPLYDEPOT, near=th.position)

            # Check if we can afford to build Barracks and if there is none in progress
            if self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
                # Build Barracks near the Comand Center
                await self.build(UnitTypeId.BARRACKS, near=th.position)

            # get all geysers close to townhall
            geysers: Units = self.vespene_geyser.closer_than(10, th)
            for geyser in geysers:
                # If there are no refinerys build at least 2
                if self.structures(UnitTypeId.REFINERY).amount < 2 and self.can_afford(UnitTypeId.REFINERY):
                    # Find all vespene geysers that are closer than range 10 to this townhall
                    await self.build(UnitTypeId.REFINERY, near=geyser)

            # Make SCV's
            if (
                self.can_afford(UnitTypeId.SCV)
                and self.supply_left > 0
                and self.supply_workers < 22
                and (
                    self.structures(UnitTypeId.BARRACKS).ready.amount < 1
                    and self.townhalls(UnitTypeId.COMMANDCENTER).idle
                    or self.townhalls(UnitTypeId.ORBITALCOMMAND).idle
                )
            ):
                th.train(UnitTypeId.SCV)

        if self.supply_left > 0:
            # Loop through all idle barracks
            for rax in self.structures(UnitTypeId.BARRACKS).idle:
                if(not rax.has_techlab):
                    self.do(rax.build(BARRACKSTECHLAB))

            for rax in self.structures(UnitTypeId.BARRACKS).idle:
                if (self.units(UnitTypeId.MARAUDER).amount < maxMarauderUnits and self.can_afford(UnitTypeId.MARAUDER)):
                    rax.train(UnitTypeId.MARAUDER)
                if (self.units(UnitTypeId.REAPER).amount < maxReaperUnits and self.can_afford(UnitTypeId.REAPER)):
                    rax.train(UnitTypeId.REAPER)
                if (self.units(UnitTypeId.MARINE).amount < maxMarineUnits and self.can_afford(UnitTypeId.MARINE)):
                    rax.train(UnitTypeId.MARINE)


        ### IDLE ASSIGN PHASE

        # if idle SCV
        if self.units(UnitTypeId.SCV).idle:
            for scv in self.units(UnitTypeId.SCV).idle:
                # Assign to Refinery
                if (self.structures(UnitTypeId.REFINERY) and self.structures(UnitTypeId.REFINERY).ready):
                    scv.gather(self.structures(UnitTypeId.REFINERY).ready.first)
                # Assign to diamond
                else:
                    if (self.mineral_field.closer_than(10, scv)):
                        scv.gather(self.mineral_field.closer_than(10, scv).first)

        target: Point2 = None
        if(self.enemy_structures):
            target = self.enemy_structures.random_or(self.enemy_start_locations[0]).position
        elif(self.enemy_units):
            target = self.enemy_units.first.position
        else:
            target = self.enemy_start_locations[0]

        if(target):
            # Check if we have at least N Marine units that are doing nothing
            if self.units(UnitTypeId.MARINE).idle.amount >= marineNumberPack:
                # Send all of them to attack the enemy base
                for unit in self.units(UnitTypeId.MARINE).idle:
                    unit.attack(target)

            # Check if we have at least N Reaper units that are doing nothing
            if self.units(UnitTypeId.REAPER).idle.amount >= reaperNumberPack:
                # Send all of them to attack the enemy base
                for unit in self.units(UnitTypeId.REAPER).idle:
                    unit.attack(target)

            # Check if we have at least N Marauder units that are doing nothing
            if self.units(UnitTypeId.MARAUDER).idle.amount >= marauderNumberPack:
                # Send all of them to attack the enemy base
                for unit in self.units(UnitTypeId.MARAUDER).idle:
                    unit.attack(target)
