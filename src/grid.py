import env
import utils
import node as nd

class GridMap:
    def __init__(self,size):
        self.env = env.Env()
        self.x_range = self.env.x_range
        self.y_range = self.env.y_range
        self.g_size = size

        self.utils = utils.Utils()

    def is_occupied(self, grid):
        return self.utils.is_inside_obs(grid)

    def create_grid_map(self):
        g_map = []
        for i in range(self.x_range[0], self.x_range[1]+self.g_size, self.g_size):
            y_ray=[]
            for j in range(self.y_range[0], self.y_range[1]+self.g_size, self.g_size):
                node = nd.Node((i,j))
                y_ray.append(int(self.is_occupied(node)))
            g_map.append(y_ray)
        return g_map

    def create_reduced_grid_map(self):
        g_map = self.create_grid_map()
        new_g_map = []
        check_points = self.env.check_points
        connection = self.env.check_points
        x_list = []
        y_list = []
        for c_point in check_points:
            is_listed_x = False
            is_listed_y = False
            if g_map[c_point[0]][c_point[1]] == 1:
                print("check point at", c_point, "is inside obstacle")
                exit(1)
            for x in x_list:
                if c_point[0] == x:
                    is_listed_x = True
            for y in y_list:
                if c_point[1] == y:
                    is_listed_y = True
            if is_listed_x == False:
                x_list.append(c_point[0])
            if is_listed_y == False:
                y_list.append(c_point[1])

        index_x = 0
        for x in g_map:
            if index_x in x_list:
                new_g_map.append(x)
            else:
                new_y_ray = []
                index_y = 0
                for y in x:
                    if index_y in y_list:
                        new_y_ray.append(0)
                    else:
                        new_y_ray.append(y+1)
                    index_y += 1
                new_g_map.append(new_y_ray)
            index_x += 1
        return new_g_map

    def show(self, g_map):
        for i in range(len(g_map)-1, -1, -1):
            print(g_map[i])