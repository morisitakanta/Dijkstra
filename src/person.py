import random

class Person:
    def __init__(self, x_start, theta_start, v_start, g_map):
        self.x_start = x_start
        self.theta_start = theta_start
        self.v_start = v_start
        self.g_map = g_map
        self.rand_flag = True
        self.check_points, self.connection = self.define_check_points(self.rand_flag)
        self.check_point_num = 0
        self.check_point_num_passed = 0

        self.current_position = self.x_start
        self.motion_control = True
        self.path = [self.x_start]


    def define_check_points(self, rand_flag=False):
        if rand_flag:
            check_points = [(4,4), (27,4), (47, 4), (4,16), (27,16), (47,16), (4,28), (27,28), (47,28)]
            connection = [(1,3), (0,2,4), (1,5), (0,4,6), (1,3,5,7), (2,4,8), (3,7), (4,6,8), (5,7)]
        else:
            check_points = [(4, 16), (28, 16), (28, 3), (47, 5), (44, 27), (4, 27), self.x_start]
            connection = []
        return check_points, connection

    def process(self):
        if self.motion_control:
            check_point = self.select_check_point(self.check_points, self.check_point_num)
            motion = self.motion_decision(check_point, self.current_position)
            next_position = self.update_current_position(self.current_position, motion)
            self.current_position = next_position
            self.check_point_num, self.check_point_num_passed = self.update_check_point(self.check_points, self.check_point_num, self.current_position, self.connection, self.check_point_num_passed)
            self.create_path(self.current_position)
        return

    def select_check_point(self, check_points, check_point_num):
        check_point = check_points[check_point_num]
        return check_point

    def motion_decision(self, check_point, current_position):
        diff = (check_point[0]-current_position[0], check_point[1]-current_position[1])
        motion_x = 0
        motion_y = 0
        if(diff[0] != 0):
            motion_x = int(diff[0]/abs(diff[0]))
        if(diff[1] != 0):
            motion_y = int(diff[1]/abs(diff[1]))
        return (motion_x, motion_y)
        
    def update_current_position(self, current_position, motion):
        next_position = (current_position[0]+motion[0], current_position[1]+motion[1])
        return next_position

    def update_check_point(self, check_points, check_point_num, current_position, connection, check_point_num_passed):
        if self.rand_flag == True:
            if check_points[check_point_num][0]==current_position[0] and check_points[check_point_num][1]==current_position[1]:
                check_point_num_rand = check_point_num_passed
                while check_point_num_rand == check_point_num_passed:
                    check_point_num_rand = random.choice(connection[check_point_num])
                print(check_point_num, "->", check_point_num_rand)
                return check_point_num_rand, check_point_num 
            return check_point_num, check_point_num_passed
        if self.rand_flag == False:
            if check_points[check_point_num][0]==current_position[0] and check_points[check_point_num][1]==current_position[1]:
                if check_point_num == len(check_points)-1:
                    self.motion_control = False
                    return check_point_num, 0
                else:
                    return check_point_num + 1, 0
            return check_point_num, 0

    def create_path(self, current_position):
        self.path.append(current_position)
        return