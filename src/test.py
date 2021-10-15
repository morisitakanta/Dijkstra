import manager

def main():
    print("test")
    sim = manager.SimManager(person_num=3, robot_num=5, sim_time_max=1000, real_time_simulate=False)
    sim.process()


if __name__ =='__main__':
    main()