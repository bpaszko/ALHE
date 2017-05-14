from CityMap import *

class SpaceVertex:
    def __init__(self, client_id, current_time, parent, gx, fx, clients):
        self.client_id = client_id 
        self.parent = parent
        self.gx = gx
        self.fx = fx
        self.current_time = current_time
        self.clients_left = clients

class SpaceVertexMinimal:
    def __init__(self, id_, parent=None):
        self.id_ = id_
        self.parent = parent



class Delivery:
    def __init__(self, start, clients, current_time, peek_hours):
        self.city = CityMap(peek_hours)
        self.boundaries = [SpaceVertex(start, current_time, parent=None, gx=0, fx=0, clients=clients)]
        self.shortest_paths = city.count_shortest_paths(clients)

    def A_star(self):
        next_v = self.boundaries[0]
        while next_v.clients_left:
            self.boundaries.remove(next_v)
            self.expand(next_v)
            next_v = self.find_lowest_fx()
        return self.getTrack(next_v)

    def find_lowest_fx(self):
        return min(self.boundaries, key=lambda v: v.fx)

    def expand(self, vertex):
        v_id = vertex.id
        current_time = vertex.current_time
        clients_left = vertex.clients_left
        travel_dict = self.city.dijkstra(v_id, clients_left, current_time)
        for next_client, time in travel_dict.items():
            self.remove_path_from_shortest(v_id, next_client)
            new_time = current_time + time
            new_clients = list(clients)
            new_clients.remove(next_client)
            new_gx = self.countGX(vertex.gx, time, len(clients_left))
            new_fx = self.countFX(new_gx, len(new_clients))
            parent = SpaceVertexMinimal(id_=v_id, parent=vertex.parent)
            new_v = SpaceVertex(next_client, new_time, parent=parent, gx=new_gx,\
                fx=new_fx, clients=new_clients)
            boundaries.append(new_v)


    def countGX(old_gx, time, waiting_num):
        return old_gx + time*waiting_num

    def countFX(gx, waiting_num):
        fx = gx
        tmp_paths = dict(shortest_paths) 
        for i in range(waiting_num):
            shortest_way, shortest_time = min(tmp_paths.items(), key=lambda x, y: y)
            tmp_paths.remove(shortest_way)
            fx += shortest_time * (waiting_num-i)
        return fx

    def remove_path_from_shortest(self, from_id, to_id):
        route = (from_id, to_id)
        if route in self.shortest_paths:
            self.shortest_paths.pop(route)