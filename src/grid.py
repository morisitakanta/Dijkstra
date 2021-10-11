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

    def show(self, g_map):
        for i in range(len(g_map)-1, -1, -1):
            print(g_map[i])