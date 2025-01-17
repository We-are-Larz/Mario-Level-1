import unittest
from ..states import level1
from ..components import powerups
from ..components import collider
from .. import constants as c
from ..components import enemies
from pprint import pprint


class TestLevel1(unittest.TestCase):

    def setUp(self):
        self.persist = {c.COIN_TOTAL: 0,
                        c.SCORE: 0,
                        c.LIVES: 3,
                        c.TOP_SCORE: 0,
                        c.CURRENT_TIME: 0.0,
                        c.LEVEL_STATE: None,
                        c.CAMERA_START_X: 0,
                        c.MARIO_DEAD: False}

    def test_adjust_mario_position(self):
        l1 = level1.Level1()
        l1.startup(0.0, self.persist)
        l1.viewport.x = 200

        # mario in transition state, mario.x < viewport.x
        l1.mario.in_transition_state = True
        l1.adjust_mario_position()
        self.assertEquals(l1.mario.rect.y, 498)
        self.assertEquals(l1.mario.rect.x, 205)

        # mario not in transition state, mario.x < viewport.x
        l1.mario.in_transition_state = False
        l1.mario.y_vel = 10
        l1.adjust_mario_position()
        self.assertEquals(l1.mario.rect.y, 498)
        self.assertEquals(l1.mario.rect.x, 205)

        # mario not in transition state, mario.x > viewport.x
        l1.mario.rect.x = 500
        l1.adjust_mario_position()
        self.assertEquals(l1.mario.rect.y, 498)
        self.assertEquals(l1.mario.rect.x, 500)


    def test_adjust_mario_for_x_collisions(self):
        # Setup
        collider1 = collider.Collider(100, 0, 10, 10)
        l1 = level1.Level1()
        l1.startup(0.0, self.persist)

        # Assertions
        l1.mario.rect.x = 99
        l1.adjust_mario_for_x_collisions(collider1)
        self.assertEqual(l1.mario.rect.x, 70)
        self.assertEqual(l1.mario.rect.right, 100)
        self.assertEqual(l1.mario.x_vel, 0)
        l1.mario.rect.x = 101
        l1.adjust_mario_for_x_collisions(collider1)
        self.assertEqual(l1.mario.rect.x, 110)
        self.assertEqual(l1.mario.rect.right, 140)
        self.assertEqual(l1.mario.x_vel, 0)

    def test_adjust_enemy_position(self):
        # Setup
        goombaA = enemies.Goomba()
        goombaA.rect.x = 200
        goombaA.x_vel = 10
        goombaB = enemies.Goomba()
        goombaB.rect.x = 250
        goombaB.x_vel = -10
        goombaC = enemies.Goomba()
        goombaC.rect.x = 150
        goombaC.x_vel = 10
        l1 = level1.Level1()
        l1.startup(0.0, self.persist)
        l1.enemy_group.add(goombaA, goombaB, goombaC)
        # A and B collide, C collides with nothing
        l1.adjust_enemy_position()

        # Assertions
        self.assertEquals(goombaA.rect.x, 210)
        self.assertEquals(goombaA.x_vel, -2)
        self.assertEquals(goombaB.rect.x, 250)
        self.assertEquals(goombaB.x_vel, 2)
        self.assertEquals(goombaC.rect.x, 160)
        self.assertEquals(goombaC.x_vel, 10)

    def test_adjust_fireball_position(self):
        # Setup
        l1 = level1.Level1()
        l1.startup(0.0, self.persist)

        # Bouncing FireBall
        fb1 = powerups.FireBall(1, 1, True)
        fb1.state = c.BOUNCING
        l1.adjust_fireball_position(fb1)

        # Flying FireBall
        fb2 = powerups.FireBall(1, 1, False)
        l1.adjust_fireball_position(fb2)

        # Off Screen FireBall
        fb3 = powerups.FireBall(1, 1, True)
        fb3.rect.x = -99999
        l1.enemy_group.add(fb3)
        l1.ground_group.add(fb3)
        l1.adjust_fireball_position(fb3)

        # Assertions
        self.assertEquals(fb1.rect.x, -7)
        self.assertEquals(fb1.rect.y, 11)
        self.assertEquals(fb1.y_vel,  10.9)
        self.assertEquals(fb2.rect.x, -31)
        self.assertEquals(fb2.rect.y, 11)
        self.assertEquals(fb2.y_vel,  10)
        self.assertNotIn(fb3, l1.enemy_group)
        self.assertNotIn(fb3, l1.ground_group)

    def test_bounce_fireball(self):
        # Setup
        l1 = level1.Level1()
        l1.startup(0.0, self.persist)

        # Right facing fireball flying
        fb1 = powerups.FireBall(1, 1, True)
        l1.bounce_fireball(fb1)

        # Left facing fireball bouncing
        fb2 = powerups.FireBall(1, 1, False)
        l1.powerup_group.add(fb2)
        l1.bounce_fireball(fb2)

        # Assertions
        self.assertEquals(fb1.y_vel, -8)
        self.assertEquals(fb1.x_vel, 15)
        self.assertEqual(fb1.state, 'flying')
        self.assertEquals(fb2.y_vel, -8)
        self.assertEquals(fb2.x_vel, -15)
        self.assertEqual(fb2.state, 'bouncing')



if __name__ == '__main__':
    unittest.main()
