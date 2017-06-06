#from collections import namedtuple

class Vertex:
    def __init__(self, id_):
        self.id = id_
        self.adjacent = dict()

    def add_neighbour(self, description):
        end, *times = description
        self.adjacent[end] = tuple(times)

    def __repr__(self):
        return "%s: %s" % (self.id, self.adjacent)


class CityMap:
    def __init__(self, peek_hours):
        self.graph = dict()
        self.peek_hours = peek_hours

    def add_edge(self, edge):
        #egde = (from_v, to_v, normal_t, peek_t)
        start, *route = edge
        if start not in self.graph:
            self.graph[start] = Vertex(start)
        self.graph[start].add_neighbour(tuple(route))


    #COMPUTE REAL TIMES FROM FROM ONE CLIENT (START) TO THE REST
    def dijkstra(self, start, end_points, current_time):
        result = {}
        vertices = dict()
        #Info = named
        for key in self.graph:
            vertices[key] = [float('inf'), 0, current_time]
        vertices[start] = [0, 0, current_time]
        
        while end_points:
            u = self.min_distance(vertices)
            vertices[u][1] = 1
            if u in end_points:
                end_points.remove(u)
                result[u] = vertices[u][0]
                if not end_points:
                     break
            for v, times in self.graph[u].adjacent.items():
                travel_time = self.compute_travel_time(times, vertices[u][2])
                if vertices[v][0] > vertices[u][0] + travel_time:
                    vertices[v][0] = vertices[u][0] + travel_time
                    vertices[v][2] = vertices[u][2] + travel_time
        return result


    #COMPUTE SHORTEST TIMES (NORMAL HOURS) BETWEEN ALL CLIENTS
    def count_shortest_paths(self, clients):
        my_dict = dict()
        for start_client in clients:
            end_points = list(clients)
            end_points.remove(start_client)
            self.find_times_from_to(start_client, end_points, my_dict)
        return my_dict


    #COMPUTE SHORTEST TIMES (NORMAL HOURS) FROM ONE CLIENT (START) TO THE REST
    def find_times_from_to(self, start, end_points, my_dict):
        vertices = dict()
        for key in self.graph:
            vertices[key] = [float('inf'), 0]
        vertices[start] = [0, 0]
        
        while end_points:
            u = self.min_distance(vertices)
            vertices[u][1] = 1
            if u in end_points:
                end_points.remove(u)
                my_dict[(start, u)] = vertices[u][0]
                if not end_points:
                     break
            for v, times in self.graph[u].adjacent.items():
                travel_time = times[0]
                if vertices[v][0] > vertices[u][0] + travel_time:
                    vertices[v][0] = vertices[u][0] + travel_time


    #HELPER FOR DIJKSTRA - FIND VERTEX WITH SHORTEST PATH TO
    def min_distance(self, vertices):
        min_dist = float('inf')
        best = None
        for v, desc in vertices.items():
            if not desc[1] and desc[0] < min_dist:
                min_dist = desc[0]
                best = v
        return best


    #RETURN SHORTEST ROUTE BETWEEN CLIENTS IN GIVEN ORDER
    def find_route(self, clients, current_time):
        route = []
        time = current_time
        for i in range(len(clients)-1):
            part_route, time = self.find_route_between_clients(clients[i][0], clients[i+1][0], time)
            route += part_route
        route.append(clients[len(clients)-1][0])
        return route


    #DIJKSTRA BETWEEN 2 CLIENTS - RETURN EXACT ROUTE
    def find_route_between_clients(self, start, end, current_time):
        result = {}
        vertices = dict()
        for key in self.graph:
            vertices[key] = [float('inf'), 0, current_time]
        vertices[start] = [0, 0, current_time]
        u = None
        while True:
            prev = u
            u = self.min_distance(vertices)
            vertices[u][1] = 1
            if u == end:
                return CityMap.make_route(result, start, end), vertices[u][2]
            for v, times in self.graph[u].adjacent.items():
                travel_time = self.compute_travel_time(times, vertices[u][2])
                if vertices[v][0] > vertices[u][0] + travel_time:
                    result[v] = u
                    vertices[v][0] = vertices[u][0] + travel_time
                    vertices[v][2] = vertices[u][2] + travel_time
        return result


    #RECREATES ROAD BETWEEN VERTICES FROM DIJKSTRA TABLE
    @staticmethod
    def make_route(vertices, start, end):
        current = end
        route = []
        while current != start:
            prev = vertices[current]
            route.append(prev)
            current = prev
        return route[::-1]


    #COMPUTE TIME NEEDED TO DRIVE THROUGH ROAD
    def compute_travel_time(self, times, current_time, remaining_part=1):
        if self.is_in_peek_hours(current_time):
            travel_time = times[1]*remaining_part
            end_time = current_time + travel_time
            peek_end = self.peek_hours[1]
            overtime = end_time - peek_end
            if overtime > 0:
                new_part = overtime / travel_time
                res = travel_time - overtime + self.compute_travel_time(times, peek_end, new_part)
                return res
            else: 
                return travel_time
        elif current_time < self.peek_hours[0]:
            travel_time = times[0]*remaining_part
            end_time = current_time + travel_time
            peek_start = self.peek_hours[0]
            overtime = end_time - peek_start
            if overtime > 0:
                new_part = overtime / travel_time
                res = travel_time - overtime + self.compute_travel_time(times, peek_start, new_part)
                return res
            else: 
                return travel_time
        else:
            return times[0]*remaining_part


    def is_in_peek_hours(self, current_time):
        return current_time >= self.peek_hours[0] and current_time < self.peek_hours[1]

    def __repr__(self):
        return str(self.graph)