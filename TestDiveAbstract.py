from DiveEllipsoid import DiveEllipsoid
import unittest
import numpy as np
# from dive_abstract import DiveAbstract  # only needed if required

class TestDiveAbstract(unittest.TestCase):

    def setUp(self):
        self.obj = DiveEllipsoid()

    def test_set_mass(self):
        self.obj.set_mass(10.0)
        self.assertEqual(self.obj.get_mass(), 10.0)

    def test_set_dist(self):
        dist = np.array([5.0, 6.0])
        self.obj.set_dist(dist)
        np.testing.assert_array_equal(self.obj.get_dist(), dist)

    def test_set_dist_x_y(self):
        self.obj.set_dist(np.array([0.0, 0.0]))
        self.obj.set_dist_x(3.0)
        self.obj.set_dist_y(4.0)
        np.testing.assert_array_equal(self.obj.get_dist(), np.array([3.0, 4.0]))

    def test_set_volumes(self):
        self.obj.set_vol_total(20.0)
        self.obj.set_vol_dived(5.0)
        self.assertEqual(self.obj.get_vol_total(), 20.0)
        self.assertEqual(self.obj.get_vol_dived(), 5.0)

    def test_set_velocity(self):
        vel = np.array([1.0, 2.0])
        self.obj.set_velocity(vel)
        np.testing.assert_array_equal(self.obj.get_velocity(), vel)

    def test_set_velocity_x_y(self):
        self.obj.set_velocity(np.array([0.0, 0.0]))
        self.obj.set_velocity_x(7.0)
        self.obj.set_velocity_y(8.0)
        np.testing.assert_array_equal(self.obj.get_velocity(), np.array([7.0, 8.0]))

    def test_set_density(self):
        self.obj.set_density(2.5)
        self.assertEqual(self.obj.get_density(), 2.5)

    def test_set_all(self):
        self.obj.set_all(
            50.0,
            np.array([1.0, 2.0]),
            100.0,
            40.0,
            np.array([3.0, 4.0])
        )

        self.assertEqual(self.obj.get_mass(), 50.0)
        np.testing.assert_array_equal(self.obj.get_dist(), np.array([1.0, 2.0]))
        self.assertEqual(self.obj.get_vol_total(), 100.0)
        self.assertEqual(self.obj.get_vol_dived(), 40.0)
        np.testing.assert_array_equal(self.obj.get_velocity(), np.array([3.0, 4.0]))

    def test_set_abstract(self):
        other = DiveEllipsoid()
        other.set_mass(99.0)

        self.obj.set_abstract(other)
        self.assertEqual(self.obj.get_mass(), 99.0)

    def test_fix_density(self):
        self.obj.set_mass(10.0)
        self.obj.set_vol_total(2.0)
        self.obj.fix_density()

        self.assertEqual(self.obj.get_density(), 5.0)  # density = mass / volume


if __name__ == "__main__":
    unittest.main()
