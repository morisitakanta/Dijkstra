from math import hypot
import random
import time

from matplotlib.pyplot import pink

class Robot:
    def __init__(self, x_start=(4,4), first_check_point_num=0):
        self.x_start = x_start
        self.check_point_num = first_check_point_num
        self.check_point_num_passed = first_check_point_num

        self.sensor_range = 5.0
        self.robot_velocity = 0.5 # 1 or 0.5
        self.enable_random_walk = True
        self.check_points, self.connection = self.define_check_points(self.enable_random_walk)

        self.current_position = self.x_start
        self.motion_control = True
        self.person_list = []

    def define_check_points(self, enable_random_walk=False):
        if enable_random_walk:
            check_points = [(4,4), (25,4), (47, 4), (4,16), (25,16), (47,16), (4,28), (25,28), (47,28)]
            connection = [(1,3), (0,2,4), (1,5), (0,4,6), (1,3,5,7), (2,4,8), (3,7), (4,6,8), (5,7)]
        else:
            check_points = [(4, 16), (28, 16), (28, 3), (47, 5), (44, 27), (4, 27)]
            connection = []
            self.x_start = check_points[0]
            self.check_point_num = 0
            self.check_point_num_passed = 0
        return check_points, connection

    def process(self, person_position):
        self.update_robot_position()
        person_inside = self.person_is_inside_sensor_range(person_position, self.current_position)
        self.person_list_manager(self.person_list, person_inside)
        # print(self.person_list)
            

    def update_robot_position(self):
        if self.motion_control:
            check_point = self.select_check_point(self.check_points, self.check_point_num)
            motion = self.motion_decision(check_point, self.current_position)
            next_position = self.update_current_position(self.current_position, motion)
            self.current_position = next_position
            self.check_point_num, self.check_point_num_passed = self.update_check_point(self.check_points, self.check_point_num, self.current_position, self.connection, self.check_point_num_passed)
            # self.create_path(self.current_position)

    def select_check_point(self, check_points, check_point_num):
        check_point = check_points[check_point_num]
        return check_point

    def motion_decision(self, check_point, current_position):
        diff = (check_point[0]-current_position[0], check_point[1]-current_position[1])
        motion_x = 0
        motion_y = 0
        if(diff[0] != 0):
            motion_x = diff[0]/hypot(diff[0],diff[1])
        if(diff[1] != 0):
            motion_y = diff[1]/hypot(diff[0],diff[1])
        return (motion_x*self.robot_velocity, motion_y*self.robot_velocity)
        
    def update_current_position(self, current_position, motion):
        next_position = (current_position[0]+motion[0], current_position[1]+motion[1])
        return next_position

    def update_check_point(self, check_points, check_point_num, current_position, connection, check_point_num_passed):
        if self.enable_random_walk == True:
            if check_points[check_point_num][0]-current_position[0]==0 and check_points[check_point_num][1]-current_position[1]==0:
            # if check_points[check_point_num][0]-current_position[0]<=(1-self.robot_velocity) and check_points[check_point_num][1]-current_position[1]<=(1-self.robot_velocity):
                check_point_num_rand = check_point_num_passed
                while check_point_num_rand == check_point_num_passed:
                    check_point_num_rand = random.choice(connection[check_point_num])
                return check_point_num_rand, check_point_num 
            return check_point_num, check_point_num_passed

        if self.enable_random_walk == False:
            if check_points[check_point_num][0]==current_position[0] and check_points[check_point_num][1]==current_position[1]:
                if check_point_num == len(check_points)-1:
                    self.motion_control = False
                    return check_point_num, 0
                else:
                    return check_point_num + 1, 0
            return check_point_num, 0

    def create_path(self, current_position):
        self.path.append(current_position)

    def person_is_inside_sensor_range(self, person_position, robot_position):
        person_num = 0
        person_inside_num_position = []
        for pp in person_position:
            dist = hypot(pp[0]-robot_position[0], pp[1]-robot_position[1])
            if dist <= self.sensor_range:
                person_inside_num_position.append([person_num, pp, None, None])
            person_num += 1
        return person_inside_num_position

    def calc_person_velocity(self, current_position, past_position):
        velocity = (current_position[0]-past_position[0], current_position[1]-past_position[1])
        return velocity
        
    def person_list_manager(self, person_list, person_inside):
        for p_inside in person_inside:
            is_already_listed = False
            for p_listed in person_list:
                if p_inside[0] == p_listed[0]:
                    is_already_listed = True
                    if p_listed[3] ==True:
                        velocity = self.calc_person_velocity(p_inside[1], p_listed[1])
                        p_listed[2] = velocity
                    else:
                        p_listed[2] = None
                    p_listed[1] = p_inside[1]
                    break
            if is_already_listed == False:
                person_list.append(p_inside)
                
        for p_listed in person_list:
            is_observed = False
            for p_inside in person_inside:
                if p_listed[0] == p_inside[0]:
                    is_observed = True
                    p_listed[3] = True
            if is_observed == False:
                p_listed[3] = False

                time.sleep(0)