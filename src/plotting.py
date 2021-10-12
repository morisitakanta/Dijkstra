"""
Plotting tools for Sampling-based algorithms
@author: huiming zhou
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import env


class Plotting:
    def __init__(self, x_start, x_goal):
        self.xI, self.xG = x_start, x_goal
        self.env = env.Env()
        self.obs_bound = self.env.obs_boundary
        self.obs_circle = self.env.obs_circle
        self.obs_rectangle = self.env.obs_rectangle
        self.init_flag = True

    def animation(self, nodelist, path, name, animation=False):
        self.plot_grid(name, self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, 0)
        self.plot_nodes(nodelist, animation)
        self.plot_path(path)

    def animation_realtime(self, nodelist, name, count):
        self.plot_grid("Dijkstra realtime.ver", self.obs_bound, self.obs_rectangle, self.obs_circle, self.xI, self.xG, count)
        self.plot_nodes(nodelist, False)
        self.graph_draw()

    def animation_connect(self, V1, V2, path, name):
        self.plot_grid(name)
        self.plot_visited_connect(V1, V2)
        self.plot_path(path)

    def plot_grid(self, name, obs_bound, obs_rectangle, obs_circle, xI, xG, count):
        if count == 0:
            fig = plt.figure()
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

        plt.plot(xI[0], xI[1], "bs", linewidth=3)
        plt.plot(xG[0], xG[1], "gs", linewidth=3)

        plt.title(name)
        plt.axis("equal")

    def plot_path(self, path):
        if len(path) != 0:
            plt.plot([x[0] for x in path], [x[1] for x in path], '-r', linewidth=2)
            plt.pause(0.01)
        print("len(path) =", len(path))
        plt.show()

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

    def graph_reset(self):
        plt.cla()

    def graph_draw(self):
        plt.draw()
        plt.pause(0.001)