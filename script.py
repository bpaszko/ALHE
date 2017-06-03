from delivery import *
from cityMap import *

def create_graph(filename):
    city = CityMap((1020, 1080))
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

city = create_graph('map.txt')
delivery = Delivery(city, '7', ['5','4','8','2','3'], 1018)
track = delivery.A_star()
print(track)
#self, city, start, clients, current_time, peek_hours)
#print(city)