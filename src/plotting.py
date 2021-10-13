"""
Plotting tools for Sampling-based algorithms
@author: huiming zhou
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import env


class Plotting:
    def __init__(self, x_start=(0,0), x_goal=(0,0)):
        self.xI, self.xG = x_start, x_goal
        self.env = env.Env()
        self.obs_bound = self.env.obs_boundary
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.init_flag = True
        self.delay_time = 0.001

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

    def animation_robot(self, robot_position):
        self.plot_grid("robot random walk", self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, True)
        self.plot_robot(robot_position)
        self.graph_draw()

    def animation_robot_and_person(self, paths, robots):
        self.plot_grid("robot & person random walk", self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, True)
        self.plot_paths(paths)
        self.plot_robot(robots)
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
            plt.plot([x[0] for x in path], [x[1] for x in path], ':r', linewidth=2, alpha=0.5)
            plt.pause(0.01)
        # print("len(path) =", len(path))
        if animation:
            plt.show()

    def plot_paths(self, paths):
        color = [':r', ':g']
        color_num = 0
        for path in paths:
            if len(path) != 0:
                plt.plot([x[0] for x in path], [x[1] for x in path], color[color_num], linewidth=2, alpha=0.5)
                if color_num+1 < len(color):
                    color_num += 1
                # plt.pause(0.01)
            # print("len(path) =", len(path))

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

    def graph_reset(self):
        plt.cla()

    def graph_draw(self):
        plt.draw()
        plt.pause(self.delay_time)