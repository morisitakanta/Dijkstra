import node as nd
import math
import plotting


class Dijkstra:
    def __init__(self, s_start, s_goal, grid_map, grid_size, iter_max, motion_size_x=1, motion_size_y=1):
        self.s_start = nd.Node(s_start)
        self.s_goal = nd.Node(s_goal)
        self.g_map = grid_map
        self.g_size = grid_size
        self.iter_max = iter_max

        self.motion_size_x = motion_size_x
        self.motion_size_y = motion_size_y
        self.motion = self.define_motion()

        self.plot = plotting.Plotting(s_start, s_goal)

    def planning(self):
        current_cost = self.s_start.cost
        node_closed = []
        node_closed.append(self.s_start)
        for i in range(self.iter_max):
            node_next = []
            for node in node_closed:
               if node.condition == 0:
                   for motion in self.motion:
                       nn = self.generate_node_next(node, motion)
                       if self.is_goal(nn, self.s_goal, self.motion_size_x, self.motion_size_y):
                           print("goal")
                           path = self.generate_path(nn, self.s_goal)
                           self.plot.animation(node_closed, path, "Dijkstra")
                           return path
                       if nn.x > 0 and nn.x < len(self.g_map) and nn.y > 0 and nn.y < len(self.g_map[0]):
                            if self.g_map[nn.x][nn.y] == 0:
                                nn_flag = True
                                nc_flag = True
                                if len(node_next) == 0:
                                    node_next.append(nn)
                                for nn_list in node_next:
                                    if nn.x == nn_list.x and nn.y == nn_list.y:
                                        nn_flag = False
                                        if nn.cost < nn_list.cost:
                                            nn_list = nn
                                        break
                                for nc_list in node_closed:
                                    if nn.x == nc_list.x and nn.y == nc_list.y:
                                        nc_flag = False
                                        if nn.cost < nc_list.cost:
                                            nc_list = nn
                                        break
                                if nn_flag and nc_flag:
                                        node_next.append(nn) 

            for node in node_next:
                node_closed.append(node)
        self.plot.animation(node_closed, [], "Dijkstra")
        return []

    def define_motion(self):
        motions = [(-self.motion_size_x, 0), (self.motion_size_x, 0), (0, self.motion_size_y), (0, -self.motion_size_y),
                        (self.motion_size_x, self.motion_size_y), (-self.motion_size_x, -self.motion_size_y), (self.motion_size_x, -self.motion_size_y), (-self.motion_size_x, self.motion_size_y)]
        print(motions)
        return motions

    def generate_node_next(self, node, motion):
        node_next = nd.Node((node.x + motion[0], node.y + motion[1]))
        node_next.parent = node
        node_next.cost = self.cost(node, motion)
        return node_next 

    def cost(self, node, motion):
        return node.cost + math.hypot(motion[0], motion[1])

    def is_goal(self, node, goal, motion_size_x, motion_size_y):
        if node.x >= goal.x-motion_size_x and node.x <= goal.x+motion_size_x and node.y >= goal.y - motion_size_y and node.y <= goal.y+motion_size_y:
            return True
        return False

    def generate_path(self, node_near, goal):
        path = [(goal.x, goal.y)]
        node_now = node_near
        while node_now.parent != None:
            path.append((node_now.x, node_now.y))
            node_now = node_now.parent
        path.append((self.s_start.x, self.s_start.y))
        return path