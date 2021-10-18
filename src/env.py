"""
Environment for rrt_2D
@author: huiming zhou
"""

class Env:
    def __init__(self):
        self.x_range = (0, 50)
        self.y_range = (0, 30)
        self.obs_boundary = self.obs_boundary()
        self.obs_circle = self.obs_circle()
        self.obs_rectangle = self.obs_rectangle()
        self.check_points, self.connection = self.test_check_points()

    @staticmethod
    def obs_boundary():
        obs_boundary = [
            [0, 0, 1, 30],
            [0, 30, 50, 1],
            [1, 0, 50, 1],
            [50, 1, 1, 30]
        ]
        return obs_boundary

    @staticmethod
    def obs_rectangle():
        obs_rectangle = [
            [14, 12, 8, 2],
            [18, 22, 8, 3],
            [26, 7, 2, 12],
            [32, 14, 10, 2]
        ]

        test = [
            [30, 6, 12, 8],
            [30, 18, 12, 8],
            [8, 6, 12, 8],
            [8, 18, 12, 8],
        ]

        return test
        # return obs_rectangle

    @staticmethod
    def obs_circle():
        obs_cir = [
            [7, 12, 3],
            [46, 20, 2],
            [15, 5, 2],
            [37, 7, 3],
            [37, 23, 3]
        ]

        test = []

        return test
        # return obs_cir

    @staticmethod
    def test_check_points():
        check_points = [(4,4), (25,4), (47, 4), (4,16), (25,16), (47,16), (4,28), (25,28), (47,28)]
        connection = [(1,3), (0,2,4), (1,5), (0,4,6), (1,3,5,7), (2,4,8), (3,7), (4,6,8), (5,7)]
        return check_points, connection