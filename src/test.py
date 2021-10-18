import manager

def main():
    # print("test")
    sim = manager.SimManager(person_num=3, robot_num=3, sim_time_max=10000, sim_time_step=1.0, real_time_simulate=False)
    sim.process()


if __name__ =='__main__':
    main()