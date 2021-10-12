import person as per
import grid
import plotting

def main():
    print("test")
    x_start = (4, 4)
    x_goal = (47, 25)

    g_map = grid.GridMap(1)
    grid_map = g_map.create_grid_map()

    plot = plotting.Plotting(x_start, x_goal)
    person = per.Person(x_start, 0, 0, grid_map)
    for i in range(100):
    # while person.motion_control:
        person.process()
    plot.animation([], person.path, "person", False)

if __name__ =='__main__':
    main()