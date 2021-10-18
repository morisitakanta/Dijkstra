from math import hypot
import random
import env


class Robot:
    def __init__(self, x_start=(4,4), first_check_point_num=0, time_step = 1.0):
        # self.x_start = x_start
        self.env = env.Env()
        self.enable_random_walk = True
        self.check_points, self.connection = self.define_check_points(self.enable_random_walk)
        self.check_point_num = first_check_point_num
        self.check_point_num_passed = first_check_point_num
        self.x_start = self.check_points[first_check_point_num]
        self.time_step = time_step

        self.sensor_range = 7.0
        self.robot_velocity = 0.3 * self.time_step # 0.0 ~ 1.0

        self.current_position = self.x_start
        self.motion_control = True
        self.person_list = []

    def define_check_points(self, enable_random_walk=False):
        if enable_random_walk:
            check_points = self.env.check_points
            connection = self.env.connection
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
        # self.person_list_manager(self.person_list, person_inside)
        return person_inside
            

    def update_robot_position(self):
        if self.motion_control:
            check_point = self.select_check_point(self.check_points, self.check_point_num)
            motion = self.motion_decision(check_point, self.current_position)
            next_position = self.update_current_position(self.current_position, motion)
            self.current_position = next_position
            self.check_point_num, self.check_point_num_passed = self.update_check_point(self.check_points, self.check_point_num, self.current_position, self.connection, self.check_point_num_passed)

    def select_check_point(self, check_points, check_point_num):
        check_point = check_points[check_point_num]
        return check_point

    def motion_decision(self, check_point, current_position):
        diff = (check_point[0]-current_position[0], check_point[1]-current_position[1])
        motion_x = 0
        motion_y = 0
        dist = hypot(diff[0], diff[1])
        if(diff[0] != 0):
            motion_x = diff[0]/dist
        if(diff[1] != 0):
            motion_y = diff[1]/dist
        return (motion_x*self.robot_velocity, motion_y*self.robot_velocity)
        
    def update_current_position(self, current_position, motion):
        next_position = (current_position[0]+motion[0], current_position[1]+motion[1])
        return next_position

    def update_check_point(self, check_points, check_point_num, current_position, connection, check_point_num_passed):
        if self.enable_random_walk == True:
            if hypot(check_points[check_point_num][0]-current_position[0], check_points[check_point_num][1]-current_position[1])<self.robot_velocity:
                self.current_position = self.update_current_position(current_position, (check_points[check_point_num][0]-current_position[0], check_points[check_point_num][1]-current_position[1]))
                check_point_num_rand = check_point_num_passed
                while check_point_num_rand == check_point_num_passed:
                    check_point_num_rand = random.choice(connection[check_point_num])
                return check_point_num_rand, check_point_num 
            return check_point_num, check_point_num_passed

        if self.enable_random_walk == False:
            if hypot(check_points[check_point_num][0]-current_position[0], check_points[check_point_num][1]-current_position[1])<self.robot_velocity:
                self.current_position = self.update_current_position(current_position, (check_points[check_point_num][0]-current_position[0], check_points[check_point_num][1]-current_position[1]))
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