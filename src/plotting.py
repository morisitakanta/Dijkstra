"""
Plotting tools for Sampling-based algorithms
@author: huiming zhou
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import env
import math


class Plotting:
    def __init__(self, x_start=(0,0), x_goal=(0,0)):
        self.xI, self.xG = x_start, x_goal
        self.env = env.Env()
        self.obs_bound = self.env.obs_boundary
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.init_flag = True
        self.delay_time = 0.001
        self.color = ['r', 'g', 'b', 'c', 'm', 'y', 'k']

    def animation(self, nodelist, path, name, animation=False):
        self.plot_grid(name, self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, 0)
        self.plot_nodes(nodelist, animation)
        self.plot_path(path)

    def animation_realtime(self, nodelist, name, count):
        self.plot_grid("Dijkstra realtime.ver", self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG)
        self.plot_nodes(nodelist, False)
        self.graph_draw()

    def animation_person(self, paths):
        self.plot_grid("person random walk", self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, True)
        self.plot_paths(paths)
        self.graph_draw()

    def animation_robot(self, robots):
        self.plot_grid("robot random walk", self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, True)
        self.plot_robot(robots)
        self.graph_draw()

    def animation_robot_and_person(self, paths, robots, person_list):
        self.plot_grid("robot & person random walk", self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, True)
        self.plot_paths(paths)
        self.plot_robot(robots)
        self.plot_observed_person(person_list)
        self.graph_draw()

    def plot_grid(self, name, obs_bound, obs_rectangle, obs_circle, xI, xG, person=False):
        if self.init_flag == True:
            fig = plt.figure()
            self.init_flag = False
        else:
            self.graph_reset()

        ax = plt.subplot(111)

        for (ox, oy, w, h) in obs_bound:
            ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='black',
                    fill=True
                )
            )

        for (ox, oy, w, h) in obs_rectangle:
            ax.add_patch(
                patches.Rectangle(
                    (ox, oy), w, h,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        for (ox, oy, r) in obs_circle:
            ax.add_patch(
                patches.Circle(
                    (ox, oy), r,
                    edgecolor='black',
                    facecolor='gray',
                    fill=True
                )
            )

        if person == False:
            plt.plot(xI[0], xI[1], "bs", linewidth=3)
            plt.plot(xG[0], xG[1], "gs", linewidth=3)

        plt.title(name)
        plt.axis("equal")

    def plot_path(self, path, animation=True):
        if len(path) != 0:
            plt.plot([x[0] for x in path], [x[1] for x in path], 'r', linewidth=2)
            plt.pause(0.01)
        if animation:
            plt.show()

    def plot_paths(self, paths):

        path_max_len = math.inf
        person_num = 0
        for path in paths:
            if len(path) != 0:
                if len(path) > path_max_len:
                    del path[:len(path)-path_max_len]
                    plt.plot([x[0] for x in path], [x[1] for x in path], ':'+self.color[min(person_num, 6)], linewidth=2, alpha=0.5)
                    plt.plot(path[len(path)-1][0], path[len(path)-1][1], marker = "o", color = self.color[min(person_num, 6)],  markersize = 4)
                    plt.annotate('person'+str(person_num), (path[len(path)-1][0], path[len(path)-1][1]))
                else:
                    plt.plot([x[0] for x in path], [x[1] for x in path], ':'+self.color[min(person_num, 6)], linewidth=2, alpha=0.5)
                    plt.plot(path[len(path)-1][0], path[len(path)-1][1], marker = "o", color = self.color[min(person_num, 6)],  markersize = 4)
                    plt.annotate('person'+str(person_num), (path[len(path)-1][0], path[len(path)-1][1]))

                plt.gcf().canvas.mpl_connect('key_release_event',
                                                lambda event:
                                                [exit(0) if event.key == 'escape' else None])
            person_num += 1

    def plot_nodes(self, nodelist, animation):
        if animation == True:
            del nodelist[0]
            count = 0
            for node in nodelist:
                count += 1
                if node.parent != None:
                    plt.plot(node.x, node.y, marker = "o", color = "r", markersize = 2)
                    plt.gcf().canvas.mpl_connect('key_release_event',
                                                 lambda event:
                                                 [exit(0) if event.key == 'escape' else None])
                    if count % 10 == 0:
                        plt.pause(0.001)
        else :
            for node in nodelist:
                plt.plot(node.x, node.y, marker = "o", color = "r", markersize = 2)
                plt.gcf().canvas.mpl_connect('key_release_event',
                                                lambda event:
                                                [exit(0) if event.key == 'escape' else None])
        
    def plot_robot(self, robots):
        robot_size = 8
        robot_color = 'k'
        robot_alpha = 0.7
        for robot in robots:
            plt.plot(robot.current_position[0], robot.current_position[1], marker="o", color=robot_color, markersize=robot_size, alpha=robot_alpha)

    def plot_observed_person(self, person_list):
        for person in person_list:
            plt.plot(person[1][0], person[1][1], marker="*", color=self.color[person[0]], markersize=10)
            plt.annotate(str(person[0]), (person[1][0], person[1][1]))
            if person[2] != None:
                self.plot_arrow(person[1], person[2])
            # plt.annotate('person'+str(person_num), (path[len(path)-1][0], path[len(path)-1][1]))

    def plot_arrow(self, x_root, velocity):
        x = [x_root[0], x_root[0]+velocity[0]]
        y = [x_root[1], x_root[1]+velocity[1]]
        plt.plot(x, y, 'k', linewidth=1)

    def graph_reset(self):
        plt.cla()

    def graph_draw(self):
        plt.draw()
        plt.pause(self.delay_time)

    def graph_show(self):
        plt.show()