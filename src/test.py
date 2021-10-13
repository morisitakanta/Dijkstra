import person as per
import robot as rbt
import plotting

def main():
    print("test")
    # x_start = (4, 4)
    x_start = (25, 16)
    x_goal = (47, 25)

    plot = plotting.Plotting()

    person = [per.Person(x_start, 4), per.Person()]
    # person2 = per.Person(x_start)
    person_position = x_start
    paths = []

    robot = [rbt.robot(x_start, 4), rbt.robot()]

    for i in range(100):
        simulated_person_and_robot_process(person, robot, paths, plot)


def simulated_person_and_robot_process(person, robot, paths, plot):
    paths.clear()
    person_position = []
    for p in person:
        person_position.append(p.process())
        paths.append(p.path)
    for r in robot:
        r.process(person_position)
    plot.animation_robot_and_person(paths, robot)


if __name__ =='__main__':
    main()