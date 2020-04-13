# TODO Replace with imports from RLU instead
class vec3:
    def __init__(self, x: float, y: float, z: float):
        self.data = (x, y, z)
    def __getitem__(self, index):
        return self.data[index]
    def __add__(self, other):
        return vec3(self[0] + other[0], self[1] + other[1], self[2] + other[2])
    def __mul__(self, num):
        return vec3(self[0] * num, self[1] * num, self[2] * num)

class Orientation:
    def __init__(self, forward: vec3, left: vec3, up: vec3):
        self.forward = forward
        self.left = left
        self.up = up

def linspace(start, end, n):
    diff = end - start
    step = diff / n
    return [start + step * i for i in range(n)]

# Constants
GRAVITY = vec3(0.0, 0.0, -650.0)
MAX_FIRST_HOLD_DURATION = 0.2
MAX_JUMP_DURATION = 1.25
SINGLE_TICK_ACC = 291.667
FIRST_JUMP_ACC = 1458.333374

class JumpSim:
    def __init__(self, position, velocity, orientation, first_hold_duration, second_jump_time):
        self.position = position
        self.velocity = velocity
        self.orientation = orientation

        assert 0.0 < first_hold_duration <= MAX_FIRST_HOLD_DURATION
        assert first_hold_duration < second_jump_time # <= first_hold_duration + MAX_JUMP_DURATION
        self.first_hold_duration =first_hold_duration
        self.second_jump_time = second_jump_time

        self.jumped_twice = False
        self.timer = 0.0
        self.done = False

    def step(self, dt):
        if self.timer == 0.0:
            self.velocity += self.orientation.up * SINGLE_TICK_ACC
        elif self.timer <= self.first_hold_duration:
            self.velocity += self.orientation.up * FIRST_JUMP_ACC * dt
        elif not self.jumped_twice and self.timer >= self.second_jump_time:
            self.velocity += self.orientation.up * SINGLE_TICK_ACC
            self.jumped_twice = True

        self.velocity += GRAVITY * dt
        self.position += self.velocity * dt

        if self.position[2] <= 0.0 or self.timer > 10.0:
            self.done = True

        self.timer += dt

if __name__ == "__main__":
    import matplotlib.pyplot as plt

    # Setup
    initial_pos = vec3(0.0, 0.0, 0.0)
    initial_vel = vec3(0.0, 0.0, 0.0)
    orientation = Orientation(
        vec3(1.0, 0.0, 0.0),
        vec3(0.0, 1.0, 0.0),
        vec3(0.0, 0.0, 1.0)
    )
    dt = 1.0 / 120.0

    max_heights = []
    max_height_times = []

    for i in linspace(dt, 0.2, 10):
        times = [0.0]
        heights = [initial_pos[2]]

        jump_sim = JumpSim(initial_pos, initial_vel, orientation, i, i + dt)
        max_height = 0.0
        max_height_time = 0.0
        while not jump_sim.done:
            jump_sim.step(dt)
            times.append(jump_sim.timer)
            heights.append(jump_sim.position[2])

            if jump_sim.position[2] > max_height:
                max_height = jump_sim.position[2]
                max_height_time = jump_sim.timer

        max_heights.append(max_height)
        max_height_times.append(max_height_time)

        plt.plot(times, heights)

    plt.scatter(max_height_times, max_heights)

    x = linspace(0.9, 1.4, 10)
    y = [530 * xi - 230 for xi in x]
    plt.plot(x, y)

    plt.show()

    
