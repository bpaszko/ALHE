from delivery import *
from cityMap import *
import sys 

#CONFIG - STRUCTURE
#START START_TIME 
#PEEK_START PEEK_END
#CLIENTS

class Config:
    def __init__(self, start, start_time, peek_hours, clients):
        self.start = start
        self.start_time = start_time
        self.peek_hours = peek_hours
        self.clients = clients

def read_config(path):
    with open(path, 'r') as f:
        start, start_time = f.readline().split()[:2]
        peek_start, peek_end = f.readline().split()[:2]
        clients = f.readline().split()
        return Config(start, int(start_time), (int(peek_start), int(peek_end)), clients)

def create_map(path, config):
    city = CityMap(config.peek_hours)
    with open(path, 'r') as f:
        while True:
            line = f.readline()
            if line == '':
                break
            start, end, t1, t2 = line.split()[:4]
            t1, t2 = int(t1), int(t2)
            city.add_edge((start, end, t1, t2))
    return city


def prepare_space(map_path, config_path):
    config = read_config(config_path)
    city = create_map(map_path, config)
    delivery = Delivery(city, config.start, config.clients, config.start_time) 
    return config, city, delivery



if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('usage: %s map_file param_file' % sys.argv[0])
        sys.exit(1)
    map_path = sys.argv[1]
    config_path = sys.argv[2]
    config, city, delivery = prepare_space(map_path, config_path)
    track = delivery.A_star()
    print(track)
    print(city.find_route(track, config.start_time))