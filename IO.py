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
            data_cut = line.split('\t')
            data = data_cut[1][:-2].split(" ")
            muon_event.particle = int(data[0])
            muon_event.x_pos_init = float(data[8])
            muon_event.y_pos_init = float(data[9])
            muon_event.z_pos_init = float(data[10])
            muon_event.x_momentum_init = float(data[3])
            muon_event.y_momentum_init = float(data[4])
            muon_event.z_momentum_init = float(data[5])
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


def arrange_data_to_string(data_array):
    return_array = []
    for event in data_array:
        event_string = "1" + '\t' + str(event.particle) \
                        + " " + "0 0 " \
                        + str(event.x_momentum_init) + " " \
                        + str(event.y_momentum_init) + " " \
                        + str(event.z_momentum_init) + " " \
                        + "0.105658 0 " \
                        + str(event.x_pos_init) + " " \
                        + str(event.y_pos_init) + " " \
                        + str(event.z_pos_init) + " "
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


