def with_print(parameters={}, **kwargs):
    """ Print parameters and measurements into a file, slightly organized"""
    for key, val in parameters.items():
        print("#", "%s: %s" % (key, val))
    print("#", *kwargs.keys())
    for row in zip(*kwargs.values()):
        print(*row)

def with_print_dump(**kwargs):
    """ Print data, not organized """
    print(kwargs)

def with_print_fancy(**kwargs):
    """ print data after separating lists of measurements from parameters"""

    print_as_list = []
    for key, val in kwargs.items():
        if not isinstance(val, list):
            print("#", "%s: %s" % (key, val))
        else:
            print_as_list.append(key)

    print("#", *print_as_list)
    for row in zip(*(kwargs[i] for i in print_as_list)):
        print(*row) 


def to_file(filename = "out", parameters={}, **kwargs):
    """ save data into a .txt file, it is basically function:with_print but we redirect the output to the file""" 
    filename = filename + ".txt"
    with open(filename, "w") as f:
        for key, val in parameters.items():
            print("#", "%s: %s" % (key, val), file=f)
        print("#", *kwargs.keys(), file=f)
        for row in zip(*kwargs.values()):
            print(*row, file=f)

def with_json(filename = "out", **kwargs):
    """ write data into a json file"""
    import json

    filename = filename + ".json"

    with open(filename, "w") as f:
        json.dump(kwargs, f)

def with_numpy(filename = "out", parameters={}, **kwargs):
    """ Write data to a .txt file with numpy""" 
    import numpy as np

    filename = filename + ".txt"
    header = ""
    for key, val in parameters.items():
        header += "{}: {} \n".format(key, val)
    header += " ".join(kwargs.keys())

    np.savetxt(filename, np.c_[ *kwargs.values() ], header=header)
    