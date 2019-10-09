from rlutilities.mechanics import AerialTurn, Dodge
from maneuvers.kit import *
from maneuvers.jumps.air_dodge import AirDodge

# class AirDodge(Maneuver):

#     def __init__(self, car: Car, duration: float, target: vec3):
#         super().__init__(car)

#         self.dodge = AirDodge(car, duration, target)
#         self.turn = AerialTurn(car)
#         self.turn.target = look_at(direction(car, target), vec3(0,0,1))
#         self.jump = self.dodge.jump
#         self.target = target

#     def step(self, dt):
#         self.dodge.step(dt)
#         self.controls = self.dodge.controls
#         self.finished = self.dodge.finished
#         if not self.dodge.jump.finished and not self.car.on_ground:
#             target_direction = direction(self.car, self.target + vec3(0, 0, 100))
#             up = target_direction * (-1)
#             up[2] = 1
#             up = normalize(up)
#             self.turn.target = look_at(target_direction, up)
#             self.turn.step(dt)
#             self.controls.pitch = self.turn.controls.pitch
#             self.controls.yaw = self.turn.controls.yaw
#             self.controls.roll = self.turn.controls.roll

class AimDodge(Dodge):

    def step(self, dt):
        target_dir = vec3(self.direction)
        target_dir[2] = 1
        target_dir = normalize(target_dir)
        self.preorientation = look_at(target_dir, vec3(0,0,1))
        super().step(dt)