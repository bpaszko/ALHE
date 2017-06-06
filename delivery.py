from cityMap import *

#STORES INFO ABOUT BOUNDARY VERTEX
class SpaceVertex:
    def __init__(self, client_id, current_time, parent, gx, fx, clients, shortest_paths):
        self.id = client_id 
        self.parent = parent
        self.gx = gx
        self.fx = fx
        self.current_time = current_time
        self.clients_left = clients
        self.shortest_paths = shortest_paths

    def __repr__(self):
        return '%s, %s, %d, %d' % (self.id, self.parent, self.gx, len(self.clients_left))

#STORES MINIMAL NECESSERY INFORMATION ABOUT VERTEX IN SEARCH SPACE
class SpaceVertexMinimal:
    def __init__(self, id_, gx, fx, parent=None):
        self.id = id_
        self.parent = parent
        self.gx = gx
        self.fx = fx

    def __repr__(self):
        return self.id


class Delivery:
    def __init__(self, city, start, clients, current_time):
        self.city = city
        sp = city.count_shortest_paths(clients)
        self.boundaries = [SpaceVertex(start, current_time, parent=None, gx=0, fx=0, 
            clients=clients, shortest_paths=sp)]

    #HEURISTIC SEARCH FOR OPTIMAL ROUTE
    def A_star(self):
        next_v = self.boundaries[0]
        while next_v.clients_left:
            self.boundaries.remove(next_v)
            self.expand(next_v)
            next_v = self.find_lowest_fx()
        return self.get_track(next_v)

    #GET NEXT VERTEX FOR A_STAR
    def find_lowest_fx(self):
        return min(self.boundaries, key=lambda v: v.fx)

    #EXPAND SEARCH SPACE FROM LOWEST FX VERTEX
    def expand(self, vertex):
        travel_dict = self.city.dijkstra(vertex.id, list(vertex.clients_left), vertex.current_time)
        for next_client, time in travel_dict.items():
            new_v = self.create_next_vertex_in_search_space(vertex, next_client, time)
            self.boundaries.append(new_v)

    #CREATE VERTEX IN SEARCH SPACE
    def create_next_vertex_in_search_space(self, vertex, next_client, time):
        v_id, current_time, clients_left, gx, fx, parent, shortest_paths = vertex.id, vertex.current_time, \
            vertex.clients_left, vertex.gx, vertex.fx, vertex.parent, vertex.shortest_paths
        new_sp = Delivery.update_shortest_paths(shortest_paths, v_id, next_client)
        new_time = current_time + time
        new_clients = Delivery.update_remaining_clients(clients_left, next_client)
        waiting_clients_number = len(clients_left)
        new_gx = Delivery.countGX(gx, time, waiting_clients_number)
        new_fx = self.countFX(new_gx, waiting_clients_number-1, new_sp)
        new_parent = SpaceVertexMinimal(id_=v_id, gx=gx, fx=fx, parent=parent)
        return SpaceVertex(next_client, new_time, parent=new_parent, gx=new_gx,\
                fx=new_fx, clients=new_clients, shortest_paths=new_sp)

    #COMPUTE GX 
    @staticmethod
    def countGX(old_gx, time, waiting_num):
        return old_gx + time*waiting_num

    #COMPUTE FX
    def countFX(self, gx, waiting_num, shortest_paths):
        fx = gx
        tmp_paths = dict(shortest_paths) 
        for i in range(waiting_num):
            shortest_way, shortest_time = min(tmp_paths.items(), key=lambda x: x[1])
            tmp_paths.pop(shortest_way)
            fx += shortest_time * (waiting_num-i)
        return fx

    #FOLLOWS END VERTEX PARENTS TO CREATE VISITING ORDER
    def get_track(self, vert):
        track = []
        while vert.parent:
            track.append((vert.id, vert.gx, vert.fx))
            vert = vert.parent
        track.append((vert.id, vert.gx, vert.fx))
        return track[::-1]

    @staticmethod
    def update_shortest_paths(paths, from_id, to_id):
        paths = dict(paths)
        route = (from_id, to_id)
        if route in paths:
            paths.pop(route)
        return paths

    @staticmethod
    def update_remaining_clients(clients, next_client):
        new_clients = list(clients)
        new_clients.remove(next_client)
        return new_clients