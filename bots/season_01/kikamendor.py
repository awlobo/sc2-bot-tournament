from sc2.bot_ai import BotAI
from sc2.position import Point2
from sc2.ids.unit_typeid import UnitTypeId
from sc2.units import Units
from sc2.ids.ability_id import AbilityId


class Kikamendor(BotAI):
    async def on_step(self, iteration):
        # Check if we have a command center
        if not self.townhalls(UnitTypeId.COMMANDCENTER) and not self.already_pending(UnitTypeId.COMMANDCENTER):
            location: Point2 = await self.get_next_expansion()
            workers: Units = self.workers.gathering
            if location and workers:
                workers.first.build(UnitTypeId.COMMANDCENTER, location)
        else:
            command_center = self.townhalls(UnitTypeId.COMMANDCENTER).first
            # If workers were found
            workers: Units = self.workers.gathering
            if not workers and (iteration % 10 == 1):
                workers = [self.workers.first]
            if workers:
                for worker in workers:
                    location: Point2 = await self.find_placement(UnitTypeId.SUPPLYDEPOT, worker.position, placement_step=20)
                    # If a placement location was found
                    if location:
                        # Order worker to build exactly on that location
                        if (
                            (self.structures(UnitTypeId.COMMANDCENTER).ready.amount + self.already_pending(UnitTypeId.COMMANDCENTER) < 5)
                            and (iteration % 5 == 1)
                        ):
                            await self.build(UnitTypeId.COMMANDCENTER, near=command_center.position)
                            continue
                        # Check if we can afford to build Barracks and if there is none in progress
                        if (
                            self.can_afford(UnitTypeId.BARRACKS)
                            and not self.already_pending(UnitTypeId.BARRACKS)
                        ):
                            # Build Barracks near the Comand Center
                            worker.build(UnitTypeId.BARRACKS, location)
                            continue
                        # Check if we can afford to build a Supply Depot and if there is none in progress
                        if (
                            self.can_afford(UnitTypeId.SUPPLYDEPOT)
                            and not self.already_pending(UnitTypeId.SUPPLYDEPOT)
                            and (
                                (self.structures(UnitTypeId.BARRACKS).ready.amount) <= 4
                            )
                            and (iteration % 2 == 1)
                        ):
                            worker.build(UnitTypeId.SUPPLYDEPOT, location)
                            continue
                        if self.can_afford(UnitTypeId.REFINERY) and not self.already_pending(UnitTypeId.REFINERY):
                            vgs: Units = self.vespene_geyser.closer_than(20, location)
                            if vgs:
                                for vg in vgs:
                                    worker.build(UnitTypeId.REFINERY, vg)
                                    continue

            # Lower all depots when finished
            for depot in self.structures(UnitTypeId.SUPPLYDEPOT).ready:
                depot(AbilityId.MORPH_SUPPLYDEPOT_LOWER)

            # TRAIN
            # Check if we already have Barracks
            if self.structures(UnitTypeId.BARRACKS):
                for barrac in self.structures(UnitTypeId.BARRACKS):
                    # Check if we can afford to bui a Marine unit
                    if (self.can_afford(UnitTypeId.MARINE)) and (iteration % 2 == 0):
                        # Train a Marine unit
                        barrac.train(UnitTypeId.MARINE)
                    if (self.can_afford(UnitTypeId.REAPER)) and (iteration % 2 == 1):
                        # Train a Marine unit
                        barrac.train(UnitTypeId.REAPER)
                if self.structures(UnitTypeId.COMMANDCENTER) and (self.supply_workers < 22):
                    for th in self.townhalls.idle:
                        th.train(UnitTypeId.SCV)

            # ATACK
            enemies: Units = self.enemy_units | self.enemy_structures
            if enemies:
                if self.units(UnitTypeId.MARINE).idle.amount >= 5:
                    # Send all of them to attack the enemy base
                    for unit in self.units(UnitTypeId.MARINE).idle:
                        unit.attack(enemies[0])
                if self.units(UnitTypeId.REAPER).idle.amount >= 10:
                    # Send all of them to attack the enemy base
                    for unit in self.units(UnitTypeId.REAPER).idle:
                        unit.attack(enemies[0])
            else:
                if self.units(UnitTypeId.MARINE).idle.amount >= 5:
                    # Send all of them to attack the enemy base
                    for unit in self.units(UnitTypeId.MARINE).idle:
                        unit.attack(self.enemy_start_locations[0])

            await self.distribute_workers()
