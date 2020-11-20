import os

from sc2.observer_ai import ObserverAI
from sc2 import run_replay

replay_file = 'AndreaBot_vs_AngusinBot.SC2Replay'


class ObserverBot(ObserverAI):
    async def on_start(self):
        print('Replay started')

    async def on_step(self, iteration: int):
        print(f'Replay iteration: {iteration}')


if __name__ == '__main__':
    file_name = replay_file
    file_path = os.path.dirname(os.path.realpath(__file__))
    full_path = os.path.join(file_path, 'replays/season_01', file_name)

    run_replay(ObserverBot(), replay_path=full_path)
