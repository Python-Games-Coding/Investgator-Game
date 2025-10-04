from random import randint

class BossAI:
    def __init__(self, boss, parent):
        self.boss = boss
        self.parent = parent

    def start_random_move(self):
        self._move_boss()

    def _move_boss(self):
        new_x = randint(100, 1200)
        direction = "R" if new_x > self.boss.x else "L"
        step = 8  # 步长加大，原来是3
        def update_boss_position():
            if abs(self.boss.x - new_x) > step:
                if direction == "R":
                    self.boss.x += step
                else:
                    self.boss.x -= step
                self.boss.move_to(self.boss.x, self.boss.y, direction)
                self.parent.after(70, update_boss_position)  # 70ms刷新一次
            else:
                self.parent.after(randint(100, 1500), self._move_boss)  # 停顿时间可调
        update_boss_position()