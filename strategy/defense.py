from maneuvers.strikes.clears import DodgeClear, AerialClear, DoubleJumpClear
from maneuvers.strikes.strike import Strike
from rlutilities.simulation import Car
from utils.game_info import GameInfo


class Defense:

    def __init__(self, info: GameInfo):
        self.info = info

    def any_clear(self, car: Car) -> Strike:
        clears = [
            DodgeClear(car, self.info),
            # DoubleJumpClear(car, self.info)
        ]
        if car.boost > 40:  # TODO
            clears.append(AerialClear(car, self.info))
        return min(clears, key=lambda clear: clear.intercept.time)