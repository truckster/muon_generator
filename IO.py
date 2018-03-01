import math

def read_file(input_file):
    in_file = open(input_file, "r")
    return_array = []
    for index, line in enumerate(in_file):
        return_array.append(line)
    in_file.close()

    return return_array


def read_header(input_array):
    return_array = []
    for line in input_array[:6]:
        return_array.append(line)
    return return_array


def read_footer(input_array):
    return_array = []
    for line in input_array[-3:]:
        return_array.append(line)
    return return_array


def read_data(input_array):
    return_array = []
    for line in input_array[6:-3]:
        if len(line) > 5:
            muon_event = MuonData()
            muon_event.string = line
            data_cut = line.split('\t')
            data = data_cut[1][:-2].split(" ")
            muon_event.particle = int(data[0])
            muon_event.x_pos_init = float(data[8])
            muon_event.y_pos_init = float(data[9])
            muon_event.z_pos_init = float(data[10])
            muon_event.x_momentum_init = float(data[3])*1000
            muon_event.y_momentum_init = float(data[4])*1000
            muon_event.z_momentum_init = float(data[5])*1000
            muon_event.total_momentum = math.sqrt(muon_event.x_momentum_init**2
                                                  + muon_event.y_momentum_init**2
                                                  + muon_event.z_momentum_init**2)
            return_array.append(muon_event)

    return return_array


class MuonData:
    def __init__(self):  # this method creates the class object.
        self.particle = 0
        self.x_pos_init = 0
        self.y_pos_init = 0
        self.z_pos_init = 0
        self.x_momentum_init = 0
        self.y_momentum_init = 0
        self.z_momentum_init = 0
        self.total_momentum = 0
        self.string = 0


def arrange_data_to_string(data_array):
    return_array = []
    for index, event in enumerate(data_array):
        # event_string = "1" + '\t' + str(event.particle) \
        #                 + " " + "0 0 " \
        #                 + str(event.x_momentum_init) + " " \
        #                 + str(event.y_momentum_init) + " " \
        #                 + str(event.z_momentum_init) + " " \
        #                 + "0.105658 0 " \
        #                 + str(event.x_pos_init) + " " \
        #                 + str(event.y_pos_init) + " " \
        #                 + str(event.z_pos_init) + " "
        event_string = event.string
        return_array.append(event_string)
    return return_array


def write_new_file(output_file, event_array, muon_multiplicity, header_array, footer_array):
    out_file = open(output_file, 'w')
    for line in header_array:
        out_file.write(line)

    for event in range(len(event_array)//muon_multiplicity):
        out_file.write(str(muon_multiplicity) + '\n')
        for event_index in range(muon_multiplicity):
            out_file.write(event_array[muon_multiplicity*event + event_index])
            out_file.write('\n')

    for line in footer_array:
        out_file.write(line)


def write_single_mult_files(file_number, output_path, event_array, muon_multiplicity, header_array, footer_array):
    out_file = open(output_path, 'w')
    for index, line in enumerate(header_array):
        if index is 2:
            out_file.write("# Events number = 1." + '\n')
        else:
            out_file.write(line)

    out_file.write(str(muon_multiplicity) + '\n')
    for event_index in range(muon_multiplicity):
        out_file.write(event_array[muon_multiplicity*file_number + event_index])

    for line in footer_array:
        out_file.write(line)


def write_single_event_script(file_number, path, event_class_array, multiplicity):
    out_file = open(path, 'w')
    out_file.write("#!/bin/bash" + '\n')
    out_file.write("export JUNO_OFFLINE_OFF=1" + '\n')
    out_file.write("source /afs/ihep.ac.cn/soft/juno/JUNO-ALL-SLC6/Pre-Release/J17v1r2-branch/setup.sh" + '\n')
    out_file.write("source /junofs/users/mueller/J17v1r1/offline/Examples/Tutorial/cmt/setup.sh" + '\n')
    out_file.write("cd /junofs/users/mueller/output/2mult_xxl/" + '\n')
    out_file.write("python /junofs/users/mueller/J17v1r1/offline/Examples/Tutorial/share/tut_detsim.py --evtmax 1"
                   " --seed $(($1)) --output mu-$(($1)).root --user-output user-mu-$(($1)).root --no-gdml "
                   "--pmt20inch --no-pmt3inch --optical --detoption Acrylic --pmt-hit-type 2 "
                   "--no-anamgr-normal --anamgr-list NormalAnaMgrMin "
                   "--anamgr-list MuProcessAnaMgr --anamgr-list PMTPosAnaMgr gun ")

    out_file.write("--particles ")
    for i in range(multiplicity):
        if event_class_array[multiplicity*file_number + i].particle < 0:
            out_file.write("mu+ ")
        if event_class_array[multiplicity*file_number + i].particle > 0:
            out_file.write("mu- ")

    out_file.write("--momentums ")
    for i in range(multiplicity):
        out_file.write("%.0f " % event_class_array[multiplicity*file_number + i].total_momentum)

    out_file.write("--positions ")
    for i in range(multiplicity):
        out_file.write("%.0f %.0f %.0f "
                       % (event_class_array[multiplicity*file_number + i].x_pos_init,
                          event_class_array[multiplicity*file_number + i].y_pos_init,
                          event_class_array[multiplicity*file_number + i].z_pos_init))

    out_file.write("--directions ")
    for i in range(multiplicity):
        out_file.write("%.6f %.6f %.6f "
                       % (event_class_array[multiplicity * file_number + i].x_momentum_init
                          / event_class_array[multiplicity*file_number + i].total_momentum,
                          event_class_array[multiplicity * file_number + i].y_momentum_init
                          / event_class_array[multiplicity*file_number + i].total_momentum,
                          event_class_array[multiplicity * file_number + i].z_momentum_init
                          / event_class_array[multiplicity*file_number + i].total_momentum))








