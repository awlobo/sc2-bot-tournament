import sc2
from sc2 import Race
from sc2.player import Bot

# from bots.season_01.andrea_bot import AndreaBot
# from bots.season_01.angusin_bot import AngusinBot
# from bots.season_01.basic_v2 import BasicV2
from bots.season_01.kikamendor import Kikamendor
from bots.season_01.retromonguer_bot import RetromonguerBot
# from bots.season_01.roberto import RobertoElRobot


def main():
    # Change only this part for the fight
    bot1 = Kikamendor()
    bot2 = RetromonguerBot()

    # Do not modify this part
    bot1_name = bot1.__class__.__name__
    bot2_name = bot2.__class__.__name__

    sc2.run_game(
        sc2.maps.get('AcropolisLE'),
        [Bot(Race.Terran, bot1, name=bot1_name), Bot(Race.Terran, bot2, name=bot2_name)],
        realtime=False,
        save_replay_as=f'replays/{bot1_name}_vs_{bot2_name}.SC2Replay',
        game_time_limit=3600
    )


if __name__ == "__main__":
    main()
