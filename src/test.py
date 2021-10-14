import person as per
import robot as rbt
import plotting

def main():
    print("test")
    # x_start = (4, 4)
    x_start = (25, 16)

    plot = plotting.Plotting()

    person = [per.Person(), per.Person((4,15), 3)]
    person_position = x_start
    person_paths = []

    robot = [rbt.Robot(x_start, 4)]

    for i in range(400):
        simulated_person_and_robot_process(person, robot, person_paths, plot)
        plot.animation_robot_and_person(person_paths, robot)


def simulated_person_and_robot_process(person, robot, paths, plot):
    paths.clear()
    person_position = []
    for p in person:
        person_position.append(p.process())
        paths.append(p.path)
    for r in robot:
        r.process(person_position)


if __name__ =='__main__':
    main()