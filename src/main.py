import grid
import dijkstra as di

def main():
    x_start = (4, 4)
    # x_start = (25, 16)
    x_goal = (47, 25)
    # x_goal = (25, 14)
    grid_size = 1
    iter_max = 100
    motion_size_x = 7
    motion_size_y = 3

    g_map = grid.GridMap(1)
    grid_map = g_map.create_grid_map()

    dijkstra = di.Dijkstra(grid_map, grid_size, iter_max, motion_size_x, motion_size_y)
    path = dijkstra.planning(x_start, x_goal)
    # path = dijkstra.planning(x_goal, (47, 5))


if __name__ =='__main__':
    main()