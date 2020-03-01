import sys
from typing import List

class Vector3(object):
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __str__(self):
        return 'x={0}, y={1}, z={2}'.format(self.x, self.y, self.z)

class Moon(object):
    def __init__(self, position: Vector3, velocity: Vector3):
        self.velocity = velocity
        self.position = position

    def apply_gravity(self, other):
        if self.position.x < other.position.x:
            self.velocity.x += 1
        elif self.position.x > other.position.x:
            self.velocity.x -= 1
        
        if self.position.y < other.position.y:
            self.velocity.y +=1
        elif self.position.y > other.position.y:
            self.velocity.y -=1

        if self.position.z < other.position.z:
            self.velocity.z += 1
        elif self.position.z > other.position.z:
            self.velocity.z -= 1

    def update_position(self):
        self.position = self.position + self.velocity

    def get_total_energy(self):
        potential_energy = abs(self.position.x) + abs(self.position.y) + abs(self.position.z)
        kinetic_energy = abs(self.velocity.x) + abs(self.velocity.y) + abs(self.velocity.z)
        total_energy = potential_energy * kinetic_energy
        return total_energy

    def __str__(self):
        return 'Position=<{0}>, Velocity=<{1}>'.format(self.position, self.velocity)

def read_moons(filename: str) -> List[Moon]:
    moons = []
    with open(filename) as f:
        for line in f:
            tokens = line.split(',')
            tokens = [token.strip(' \n') for token in tokens]
            x = int(tokens[0][3:])
            y = int(tokens[1][2:])
            z = int(tokens[2][2:-1])
            moons.append(Moon(position=Vector3(x, y, z), velocity=Vector3(0, 0, 0)))
        return moons

def apply_gravity(moons: List[Moon]):
    for i in range(len(moons)):
        for j in range(i + 1, len(moons)):
            first = moons[i]
            second = moons[j]
            first.apply_gravity(second)
            second.apply_gravity(first)

def update_positions(moons: List[Moon]):
    for moon in moons:
        moon.update_position()

def get_system_energy(moons: List[Moon]) -> int:
    return sum(moon.get_total_energy() for moon in moons)

def solve(moons: List[Moon], num_time_steps=100):
    system_energy = 0
    for timestep in range(0, num_time_steps):
        for moon in moons:
            print(moon)
        print('========================================')
        apply_gravity(moons)
        update_positions(moons)
        system_energy = get_system_energy(moons)
    print('System energy={0}'.format(system_energy))

if __name__ == "__main__":
    moons = read_moons(sys.argv[1])
    solve(moons, num_time_steps=1000)