import sc2
from sc2 import Race
from sc2.player import Bot

# from bots.season_01.andrea_bot import AndreaBot
# from bots.season_01.angusin_bot import AngusinBot
from bots.season_01.basic_v2 import BasicV2
# from bots.season_01.kikamendor import Kikamendor
# from bots.season_01.retromonguer_bot import RetromonguerBot
from bots.season_01.roberto import RobertoElRobot


def main():
    # Change only this part for the fight
    bot1 = BasicV2()
    bot2 = RobertoElRobot()

    # Do not modify this part
    sc2.run_game(
        sc2.maps.get('AcropolisLE'),
        [Bot(Race.Terran, bot1), Bot(Race.Terran, bot2)],
        realtime=False,
        save_replay_as=f'replays/{bot1.__class__.__name__}_vs_{bot2.__class__.__name__}.SC2Replay',
        game_time_limit=3600
    )


if __name__ == "__main__":
    main()
