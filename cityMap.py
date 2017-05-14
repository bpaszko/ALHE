from collections import defaultdict

class Vertex:
    def __init__(self, id_):
        self.id = id_
        self.adjacent = defaultdict(tuple())

    def add_neighbour(self, description):
        end, *times = description
        self.adjacent[end] = tuple(times)


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

    def dijkstra(self, start, end_points, current_time):
        result = {}
        vertexes = dict()
        for key in self.graph:
            vertexes[key] = [float('inf'), 0, current_time]
        vertexes[start] = [0, 1, current_time]
        
        while end_points:
            u = min_distance(vertexes)
            if u in end_points:
                end_points.remove(u)
                result[u] = vertexes[u][0]
                if not end_points:
                     break
            for v, times in u.adjacent.items():
                travel_time = self.compute_travel_time(times, vertexes[u][2])
                if vertexes[v][0] > vertexes[u][0] + travel_time:
                    vertexes[v][0] = vertexes[u][0] + travel_time
                    vertexes[v][2] = vertexes[u][2] + travel_time
        return result


    def count_shortest_paths(clients):
        my_dict = dict()
        for start_client in clients:
            end_points = list(clients)
            end_points.remove(start_client)
            find_times_from_to(start_client, end_points, my_dict)


    def find_times_from_to(start, end_points, my_dict):
        vertexes = dict()
        for key in self.graph:
            vertexes[key] = [float('inf'), 0]
        vertexes[start] = [0, 1]
        
        while end_points:
            u = min_distance(vertexes)
            if u in end_points:
                end_points.remove(u)
                my_dict[(start, u)] = vertexes[u][0]
                if not end_points:
                     break
            for v, times in self.graph[u].adjacent.items():
                travel_time = times[0]
                if vertexes[v][0] > vertexes[u][0] + travel_time:
                    vertexes[v][0] = vertexes[u][0] + travel_time
        return result

    def min_distance(vertexes):
        min_dist = float('inf')
        best = None
        for v, desc in vertexes.items():
            if desc[1] and desc[0] < min_dist:
                min_dist = desc[0]
                best = v
        return best

    def compute_travel_time(self, times, current_time):
        normal_time, peek_time = times
        peek_start, peek_end = self.peek_hours
        if current_time < peek_start and current_time + normal_time <= peek_start:
            return normal_time
        if current_time > peek_end:
            return normal_time
        if current_time >= peek_start and current_time + peek_time <= peek_end:
            return peek_time
        if current_time <= peek_start and current_time + normal_time <= peek_end:
            time = peek_start - current_time
            driven_part = time/normal_time
            left_time = (1-driven_part)*peek_time
            return current_time + time + left_time
        if current_time >= peek_start and current_time + peek_time >= peek_end:
            time = peek_end - current_time
            driven_part = time/peek_time
            left_time = (1-driven_part)*normal_time
            return current_time + time + left_time
