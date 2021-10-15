import person as per
import robot as rbt
import plotting
import time

class SimManager:
    def __init__(self, person_num=1, robot_num=1, sim_time_max=5.0, sim_time_step=1.0, real_time_simulate=False):
        self.person_num = person_num
        self.robot_num = robot_num
        self.person = []
        self.robot = []
        self.person_paths = []
        self.sim_time_max = sim_time_max
        self.sim_time_step = sim_time_step
        self.sim_real_time = real_time_simulate

        self.plot = plotting.Plotting()

        self.person_list = [] #[[名前, 位置, 速度, 観測], [ ], ... ]

    def process(self):
        self.define_person(self.person_num,self.person)
        self.define_robot(self.robot_num,self.robot)
        sim_time = 0.0
        while sim_time < self.sim_time_max:
            self.simulate_process()
            self.plot.animation_robot_and_person(self.person_paths, self.robot, self.person_list)
            sim_time = self.time_update(sim_time)
            print(self.person_list)

        self.plot.graph_show()

    def simulate_process(self):
        self.person_paths.clear()
        person_position = []
        person_observed_list = []
        for p in self.person:
            person_position.append(p.process())
            self.person_paths.append(self.path_length(p.path.copy()))
        for r in self.robot:
            person_observed = r.process(person_position)
            self.observed_list_manager(person_observed_list, person_observed)
        self.person_list_manager(self.person_list, person_observed_list)

    def time_update(self, current_time):
        if self.sim_real_time == True:
            time.sleep(self.sim_time_step)
        else:
            time.sleep(0.01)
        # print("sim_time =", sim_time)
        return current_time + self.sim_time_step

    def define_person(self, person_num, defined_person):
        for i in range(person_num):
            defined_person.append(per.Person(first_check_point_num=min(i*5, 8)))
        print(len(self.person),"person defined")

    def define_robot(self, robot_num, defined_robot):
        for i in range(robot_num):
            defined_robot.append(rbt.Robot(first_check_point_num=min(i^2, 8))) 
        print(len(self.robot), "robot defined")

    def path_length(self, path):
        len_max = 40
        if len(path) > len_max:
            del path[:len(path)-len_max]
        return path

    def observed_list_manager(self, observed_list, new_list):
        for n_list in new_list:
            if len(observed_list) == 0:
                observed_list.append(n_list)
            for o_list in observed_list:
                if n_list[0] == o_list[0]:
                    break
                else:
                    observed_list.append(n_list)

    def calc_person_velocity(self, current_position, past_position):
        velocity = ((current_position[0]-past_position[0])/self.sim_time_step, (current_position[1]-past_position[1])/self.sim_time_step)
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