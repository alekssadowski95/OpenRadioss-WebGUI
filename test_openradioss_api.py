import importlib.util

def module_from_file(module_name, file_path):
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

runopenradioss = module_from_file("runopenradioss", "C:/Users/Work/Documents/Github/OpenRadioss2/OpenRadioss_libs/openradioss_gui/runopenradioss.py")

if __name__ == "__main__":
    print(runopenradioss)
    print(dir(runopenradioss))

    # construct OpenRadioss command
    command = [
        'C:/Users/Work/Desktop/OpenRadioss-Examples/mars-rover/mars-rover-suspension-2_1_0.inp', # input file path
        '16', # number of threads                                                                  
        '1', # number of processes
        'dp', # precision "sp"/ "dp"
        'no', # anim_to_vtk "yes"/ "no"
        'no', # th_to_csh "yes"/ "no"
        'no', # starter only "yes"/ "no"
        'no', # anim_to_d3plot "yes"/ "no"
        'no' # anim_to_vtkhdf "yes"/ "no"
    ]
    debug = True

    # Run OpenRadioss
    openradioss = runopenradioss.RunOpenRadioss(command, debug)