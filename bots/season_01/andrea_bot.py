from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId


class AndreaBot(BotAI):
    async def on_step(self, iteration):

        # number of cc
        num_cc = self.townhalls(UnitTypeId.COMMANDCENTER).amount

        # put this lazy SCVs to work
        await self.distribute_workers()

        if self.townhalls(UnitTypeId.COMMANDCENTER):
            command_center = self.townhalls(UnitTypeId.COMMANDCENTER).first
        else:
            # we'll go down fighting
            for worker in self.workers:
                worker.attack(self.enemy_start_locations[0])
            return

        # expansion time
        if self.supply_used == self.supply_cap or self.supply_used > self.supply_cap - (self.supply_cap/5):
            if self.already_pending(UnitTypeId.COMMANDCENTER) == 0 and self.can_afford(UnitTypeId.COMMANDCENTER):
                next_expo = await self.get_next_expansion()
                location = await self.find_placement(UnitTypeId.COMMANDCENTER, next_expo, placement_step=1)
                if location:
                    w = self.select_build_worker(location)
                    if w and self.can_afford(UnitTypeId.COMMANDCENTER):
                        w.build(UnitTypeId.COMMANDCENTER, location)

        # create more workers
        if self.can_afford(UnitTypeId.SCV) and self.workers.amount < 16*num_cc and command_center.is_idle:
            # if self.townhalls(UnitTypeId.COMMANDCENTER).amount>1:
            command_center.train(UnitTypeId.SCV)

        # supply depot construction
        if not self.structures(UnitTypeId.SUPPLYDEPOT) or self.structures(UnitTypeId.SUPPLYDEPOT).amount < 3*num_cc:
            if self.can_afford(UnitTypeId.SUPPLYDEPOT) and not self.already_pending(UnitTypeId.SUPPLYDEPOT):
                await self.build(UnitTypeId.SUPPLYDEPOT, near=command_center.position)

        # barracks construction
        if not self.structures(UnitTypeId.BARRACKS) or self.structures(UnitTypeId.BARRACKS).amount < 4*num_cc and self.structures(UnitTypeId.SUPPLYDEPOT):
            if self.can_afford(UnitTypeId.BARRACKS) and not self.already_pending(UnitTypeId.BARRACKS):
                await self.build(UnitTypeId.BARRACKS, near=command_center.position)

        if self.structures(UnitTypeId.BARRACKS):
            if (self.can_afford(UnitTypeId.MARINE)):
                for index in range(self.structures(UnitTypeId.BARRACKS).amount):
                    barrack = self.structures(UnitTypeId.BARRACKS)[index]
                    barrack.train(UnitTypeId.MARINE)

        if self.units(UnitTypeId.MARINE).idle.amount >= 15:
            for unit in self.units(UnitTypeId.MARINE).idle:
                unit.attack(self.enemy_start_locations[0])
