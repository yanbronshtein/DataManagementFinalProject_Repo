def get_json_data(filename):
    with open(filename, "r") as read_file:
        json_data = json.load(read_file)
    return json_data