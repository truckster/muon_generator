import IO, track_check

file_path = "/home/gpu/Simulation/muon_gen/"
input_file_name = "gen.txt"

file_data = IO.read_file(file_path+input_file_name)
header = IO.read_header(file_data)
footer = IO.read_footer(file_data)
event_data = IO.read_data(file_data)
data_new = track_check.is_detector_hit(event_data)
event_string_data = IO.arrange_data_to_string(data_new)

IO.write_new_file(file_path + "test.txt", event_string_data, 2, header, footer)

