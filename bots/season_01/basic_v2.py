from sc2.bot_ai import BotAI
from sc2.ids.unit_typeid import UnitTypeId


# Rename this class to your bot's name
class BasicV2(BotAI):

    def is_building_needed(self, type):
        if not self.can_afford(type) or not self.already_pending(type) == 0:
            return False

        if type == UnitTypeId.SUPPLYDEPOT:
            return self.structures(type).ready.amount + self.already_pending(type) < 2
        elif type == UnitTypeId.BARRACKS:
            if self.structures(UnitTypeId.SUPPLYDEPOT).ready.amount < 2:
                return False
            return self.structures(type).ready.amount + self.already_pending(type) < 1
        elif type == UnitTypeId.REFINERY:
            if self.structures(UnitTypeId.BARRACKS).ready.amount < 1:
                return False
            return self.structures(type).ready.amount + self.already_pending(type) < 1
        elif type == UnitTypeId.FACTORY:
            if self.structures(UnitTypeId.REFINERY).ready.amount < 1:
                return False
            return self.structures(type).ready.amount + self.already_pending(type) < 1
        elif type == UnitTypeId.TECHLAB:
            if self.structures(UnitTypeId.FACTORY).ready.amount < 1:
                return False
            return self.structures(type).ready.amount + self.already_pending(type) < 1
        # self.structures(UnitTypeId.BARRACKS).ready.amount + self.already_pending(UnitTypeId.BARRACKS) > 0
        return False

    # This function is executed in an infinite loop during the game
    async def on_step(self, iteration):
        # Check if we have a command center to use as a reference position for other buildings
        if self.townhalls(UnitTypeId.COMMANDCENTER):
            command_center = self.townhalls(UnitTypeId.COMMANDCENTER).first
        else:
            # If our command center got destroyed, do nothing and die with pride
            return

        if self.units(UnitTypeId.SCV).idle.amount > 0:
            await self.distribute_workers()

        # Build SCVs
        if self.can_afford(UnitTypeId.SCV) and self.workers.amount < 16 and command_center.is_idle:
            command_center.train(UnitTypeId.SCV)

        # Check if we still have no Supply Depot (this is required to build Barracks)
        # https://starcraft.fandom.com/wiki/Barracks#StarCraft_II
        if self.is_building_needed(UnitTypeId.SUPPLYDEPOT):
            # Build a Supply Depot near the Comand Center
            await self.build(UnitTypeId.SUPPLYDEPOT, near=command_center.position)

        if self.is_building_needed(UnitTypeId.BARRACKS):
            # Build Barracks near the Comand Center
            await self.build(UnitTypeId.BARRACKS, near=command_center.position)

        # Check if we already have Barracks
        if self.structures(UnitTypeId.BARRACKS):
            # Get the first Barracks structure
            barracs = self.structures(UnitTypeId.BARRACKS).first
            # Check if we can afford to bui a Marine unit
            if (self.can_afford(UnitTypeId.MARINE)):
                # Train a Marine unit
                barracs.train(UnitTypeId.MARINE)

        if self.units(UnitTypeId.MARINE).idle.amount >= 15:
            # Send all of them to attack the enemy base
            for unit in self.units(UnitTypeId.MARINE).idle[:15]:
                unit.attack(self.enemy_start_locations[0])
