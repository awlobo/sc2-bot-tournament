import sc2
from sc2.bot_ai import BotAI


class RobertoElRobot(BotAI):
    main_cc = None
    raise_hell = False

    async def on_step(self, iteration):
        # Get command center
        ccs = self.townhalls(sc2.UnitTypeId.COMMANDCENTER)
        if not ccs:
            return
        else:
            self.main_cc = ccs.first

        # Train workers
        if self.can_afford(sc2.UnitTypeId.SCV) and self.workers.amount < 20 and self.main_cc.is_idle:
            self.main_cc.train(sc2.UnitTypeId.SCV)

        # Build depots
        await self.build_depots()

        # Raise depots when enemies are near
        self.automate_depots()

        # Build refineries
        self.build_refineries()

        # Build barracks
        await self.build_barracks()

        # Build factories
        await self.build_factories()

        # Train forces
        self.train_forces()

        # Put idle workers to work
        self.put_scvs_to_work()

        # Attack!!
        self.attack()

    async def build_depots(self):
        # Get positions from to block the ramp
        depot_placement_positions = self.main_base_ramp.corner_depots | {self.main_base_ramp.depot_in_middle}

        # Filter locations close to finished supply depots
        depots = self.structures.of_type({sc2.UnitTypeId.SUPPLYDEPOT, sc2.UnitTypeId.SUPPLYDEPOTLOWERED})
        if depots:
            depot_placement_positions = {
                d for d in depot_placement_positions if depots.closest_distance_to(d) > 1
            }

        # Build depots
        if self.can_afford(sc2.UnitTypeId.SUPPLYDEPOT) and self.already_pending(sc2.UnitTypeId.SUPPLYDEPOT) == 0:
            # Get a random worker
            workers = self.workers.gathering
            if workers:  # if workers were found
                worker = workers.random
            else:
                # No workers available. Don't build anything
                return

            if len(depot_placement_positions) == 0:
                if depots.amount < 18:
                    target_depot_location = await self.find_placement(sc2.UnitTypeId.SUPPLYDEPOT, near=self.main_base_ramp.depot_in_middle.position, placement_step=1)
                else:
                    # We have all the depots we need. Don't build more
                    return
            else:
                target_depot_location = depot_placement_positions.pop()

            worker.build(sc2.UnitTypeId.SUPPLYDEPOT, target_depot_location)

    def automate_depots(self):
        # Raise depots when enemies are nearby
        for depo in self.structures(sc2.UnitTypeId.SUPPLYDEPOT).ready:
            for unit in self.enemy_units:
                if unit.distance_to(depo) < 15:
                    break
            else:
                depo(sc2.AbilityId.MORPH_SUPPLYDEPOT_LOWER)

        # Lower depots when no enemies are nearby
        for depo in self.structures(sc2.UnitTypeId.SUPPLYDEPOTLOWERED).ready:
            for unit in self.enemy_units:
                if unit.distance_to(depo) < 10:
                    depo(sc2.AbilityId.MORPH_SUPPLYDEPOT_RAISE)
                    break

    def build_refineries(self):
        if self.gas_buildings.amount < 2:
            if self.can_afford(sc2.UnitTypeId.REFINERY):
                # All the vespene geysirs nearby, including ones with a refinery on top of it
                vgs = self.vespene_geyser.closer_than(10, self.main_cc)

                for vg in vgs:
                    if self.gas_buildings.filter(lambda unit: unit.distance_to(vg) < 1):
                        continue

                    # Select a worker closest to the vespene geysir
                    worker = self.select_build_worker(vg)

                    if worker is None:
                        continue
                    # Issue the build command to the worker, important: vg has to be a Unit, not a position
                    worker.build_gas(vg)

    def put_scvs_to_work(self):
        # Keep refineries at maximum capacity
        for refinery in self.gas_buildings:
            if refinery.assigned_harvesters < refinery.ideal_harvesters:
                worker = self.workers.closer_than(10, refinery)
                if worker:
                    worker.random.gather(refinery)

        # Send idle workers to father minerals
        for scv in self.workers.idle:
            scv.gather(self.mineral_field.closest_to(self.main_cc))

    async def build_barracks(self):
        # Build barracks when needed
        if self.structures(sc2.UnitTypeId.SUPPLYDEPOT).ready:
            if self.structures(sc2.UnitTypeId.BARRACKS).amount < 3 and not self.already_pending(sc2.UnitTypeId.BARRACKS):
                if self.can_afford(sc2.UnitTypeId.BARRACKS):
                    position = self.main_cc.position.towards_with_random_angle(self.game_info.map_center, 5)
                    await self.build(sc2.UnitTypeId.BARRACKS, near=position)

    async def build_factories(self):
        if self.structures(sc2.UnitTypeId.BARRACKS).ready:
            if self.structures(sc2.UnitTypeId.FACTORY).amount < 3 and not self.already_pending(sc2.UnitTypeId.FACTORY):
                if self.can_afford(sc2.UnitTypeId.FACTORY):
                    position = self.main_cc.position.towards_with_random_angle(self.game_info.map_center, 5)
                    await self.build(sc2.UnitTypeId.FACTORY, near=position)

    def train_forces(self):
        if self.structures(sc2.UnitTypeId.BARRACKS):
            if (self.can_afford(sc2.UnitTypeId.REAPER)):
                for barrack in self.structures(sc2.UnitTypeId.BARRACKS):
                    # barrack.train(sc2.UnitTypeId.MARINE)
                    barrack.train(sc2.UnitTypeId.REAPER)

        if self.structures(sc2.UnitTypeId.FACTORY):
            if (self.can_afford(sc2.UnitTypeId.HELLION)):
                for factory in self.structures(sc2.UnitTypeId.FACTORY):
                    factory.train(sc2.UnitTypeId.HELLION)

    def attack(self):
        if self.raise_hell:
            for marine in self.units(sc2.UnitTypeId.MARINE).idle:
                if self.enemy_units:
                    closest_enemy = self.enemy_units.closest_to(marine)
                    marine.attack(closest_enemy)
                elif self.enemy_structures:
                    closest_building = self.enemy_structures.closest_to(marine)
                    marine.attack(closest_building)
                else:
                    marine.attack(self.enemy_start_locations[0])

            for reaper in self.units(sc2.UnitTypeId.REAPER).idle:
                if self.enemy_units:
                    closest_enemy = self.enemy_units.closest_to(reaper)
                    reaper.attack(closest_enemy)
                elif self.enemy_structures:
                    closest_building = self.enemy_structures.closest_to(reaper)
                    reaper.attack(closest_building)
                else:
                    reaper.attack(self.enemy_start_locations[0])

            for hellion in self.units(sc2.UnitTypeId.HELLION).idle:
                if self.enemy_units:
                    closest_enemy = self.enemy_units.closest_to(hellion)
                    hellion.attack(closest_enemy)
                elif self.enemy_structures:
                    closest_building = self.enemy_structures.closest_to(hellion)
                    hellion.attack(closest_building)
                else:
                    hellion.attack(self.enemy_start_locations[0])
        else:
            army_count = self.units(sc2.UnitTypeId.MARINE).amount + self.units(sc2.UnitTypeId.REAPER).amount + self.units(sc2.UnitTypeId.HELLION).amount
            if army_count >= 60:
                self.raise_hell = True
