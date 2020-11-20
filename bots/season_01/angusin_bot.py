
from sc2.ids.unit_typeid import UnitTypeId
from sc2.position import Point2
from sc2.unit import Unit
from sc2.bot_ai import BotAI


class AngusinBot(BotAI):
    async def on_step(self, iteration):

        commandCenter: Unit = self.townhalls(UnitTypeId.COMMANDCENTER).first
        closeToEnemyBase: Point2 = self.game_info.map_center.towards_with_random_angle(
            self.enemy_start_locations[0], 30)

        # All workers to gather mineral
        for scv in self.workers.idle:
            scv.gather(self.mineral_field.closest_to(commandCenter))

        # Train workers until 20
        if self.can_afford(UnitTypeId.SCV) and self.supply_workers < 20 and commandCenter.is_idle:
            commandCenter.train(UnitTypeId.SCV)

        # Build 7 depots
        elif self.structures(UnitTypeId.SUPPLYDEPOT).amount < 7:
            if self.can_afford(UnitTypeId.SUPPLYDEPOT):
                await self.build(UnitTypeId.SUPPLYDEPOT, near=commandCenter.position.towards(self.game_info.map_center, 5))

        # Build 5 barracks
        elif self.structures(UnitTypeId.BARRACKS).amount < 6:
            if self.can_afford(UnitTypeId.BARRACKS):
                await self.build(UnitTypeId.BARRACKS, near=closeToEnemyBase)

        # Train marines permanently
        for marine in self.structures(UnitTypeId.BARRACKS).ready.idle:
            if self.can_afford(UnitTypeId.MARINE):
                marine.train(UnitTypeId.MARINE)

        # Attack with 20 marines
        if self.units(UnitTypeId.MARINE).idle.amount >= 20:
            for marine in self.units(UnitTypeId.MARINE).idle:
                marine.attack(self.enemy_start_locations[0])
