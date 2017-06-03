
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


    def dijkstra(self, start, end_points, current_time):
        result = {}
        vertexes = dict()
        for key in self.graph:
            vertexes[key] = [float('inf'), 0, current_time]
        vertexes[start] = [0, 0, current_time]
        
        while end_points:
            u = self.min_distance(vertexes)
            vertexes[u][1] = 1
            if u in end_points:
                end_points.remove(u)
                result[u] = vertexes[u][0]
                if not end_points:
                     break
            for v, times in self.graph[u].adjacent.items():
                travel_time = self.compute_travel_time(times, vertexes[u][2])
                if vertexes[v][0] > vertexes[u][0] + travel_time:
                    vertexes[v][0] = vertexes[u][0] + travel_time
                    vertexes[v][2] = vertexes[u][2] + travel_time
        return result


    #SHOULD WORK
    def count_shortest_paths(self, clients):
        my_dict = dict()
        for start_client in clients:
            end_points = list(clients)
            end_points.remove(start_client)
            self.find_times_from_to(start_client, end_points, my_dict)
        return my_dict

    #SHOULD WORK
    def find_times_from_to(self, start, end_points, my_dict):
        vertexes = dict()
        for key in self.graph:
            vertexes[key] = [float('inf'), 0]
        vertexes[start] = [0, 0]
        
        while end_points:
            u = self.min_distance(vertexes)
            vertexes[u][1] = 1
            if u in end_points:
                end_points.remove(u)
                my_dict[(start, u)] = vertexes[u][0]
                if not end_points:
                     break
            for v, times in self.graph[u].adjacent.items():
                travel_time = times[0]
                if vertexes[v][0] > vertexes[u][0] + travel_time:
                    vertexes[v][0] = vertexes[u][0] + travel_time

    #SHOULD WORK
    def min_distance(self, vertexes):
        min_dist = float('inf')
        best = None
        for v, desc in vertexes.items():
            if not desc[1] and desc[0] < min_dist:
                min_dist = desc[0]
                best = v
        return best

    def compute_travel_time(self, times, current_time, remaining_part=1):
        if self.is_in_peek_hours(current_time):
            travel_time = times[1]*remaining_part
            end_time = current_time + travel_time
            peek_end = self.peek_hours[1]
            overtime = end_time - peek_end
            if overtime > 0:
                new_part = 1 - overtime / travel_time
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
                new_part = 1 - overtime / travel_time
                res = travel_time - overtime + self.compute_travel_time(times, peek_start, new_part)
                return res
            else: 
                return travel_time
        else:
            return times[0]


    def is_in_peek_hours(self, current_time):
        return current_time >= self.peek_hours[0] and current_time < self.peek_hours[1]

    def __repr__(self):
        return str(self.graph)