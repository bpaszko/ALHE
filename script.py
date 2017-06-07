from delivery import *
from cityMap import *
import sys 

#CONFIG - STRUCTURE
#START START_TIME 
#PEEK_START PEEK_END
#CLIENTS

class Config:
    def __init__(self, start, start_time, peek_hours, clients):
        self.start = starts
        self.start_time = start_time
        self.peek_hours = peek_hours
        self.clients = clients

def read_config(path):
    with open(path, 'r') as f:
        start, start_time = f.readline().split(' ')[:2]
        peek_start, peek_end = f.readline().split(' ')[:2]
        clients = f.readline().split(' ')
        return Config(start, start_time, (peek_start, pee), clients)

def create_map(path, config):
    city = CityMap(config.peek_hours)
    with open(filename, 'r') as f:
        while True:
            line = f.readline()
            if line == '':
                break
            start, end, t1, t2 = line.split(' ')
            t2 = t2.replace('\n', '')
            t1, t2 = int(t1), int(t2)
            city.add_edge((start, end, t1, t2))
    return city


def prepare_space(map_path, config_path):
    config = read_config(config_path)
    city_map = create_map(map_path, config)
    delivery = Delivery(city, config.start, config.clients, config.start_time) 
    return city_map, delivery



if __name__ == '__main__':
    if len(sys.argv) != 3:
        sys.stderr.write('usage: %s map_file param_file' % sys.argv[0])
        sys.exit(1)
    map_path = sys.argv[1]
    config_path = sys.argv[2]
    city, delivery = prepare_space(map_path, config_path)
    track = delivery.A_star()
    print(track)
    print(city.find_route(track, current_time))