from delivery import *
from cityMap import *
import unittest


def to_test(file,startTrafficTime,endTrafficTime,startPoint,road,startTime):
	def create_graph(filename,startTrafficTime,endTrafficTime):
	    city = CityMap((startTrafficTime, endTrafficTime))
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

	city = create_graph(file,startTrafficTime,endTrafficTime)
	delivery = Delivery(city, startPoint, road, startTime)
	track = delivery.A_star()
	return track


class TestStringMethods(unittest.TestCase):

    def test_1(self):
    	road=['2']
    	startPoint='1'
    	file='map.txt'
    	startTime=1020
    	result=[('1', 0, 0),('2', 9, 9)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_2(self):
    	road=['2']
    	startPoint='1'
    	file='map.txt'
    	startTime=1000
    	result=[('1', 0, 0),('2', 8, 8)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_3(self):
    	road=['2','4','5']
    	startPoint='1'
    	startTime=100
    	file='map.txt'
    	result=[('1', 0, 0),('4', 12, 17), ('2', 24, 25), ('5', 25, 25)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_4(self):
    	road=['5','4','8','2','3']
    	startPoint='7'
    	file='map.txt'
    	startTime=100
    	result=[('7', 0, 0), ('4', 20, 46), ('3', 40, 53), ('2', 55, 60), ('5', 57, 60), ('8', 63, 63)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_5(self):
    	road=['5','4','8','2','3']
    	startPoint='7'
    	file='map.txt'
    	startTime=1018
    	result=[('7', 0, 0), ('4', 25.0, 51.0), ('3', 57.0, 70.0), ('2', 75.0, 80.0), ('5', 83.0, 86.0), ('8', 95.0, 95.0)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_6(self):
    	road=['5','4','8','2','3']
    	startPoint='7'
    	file='map.txt'
    	startTime=1015
    	result=[('7', 0, 0), ('4', 20, 46), ('3', 50.0, 63.0), ('2', 68.0, 73.0), ('5', 76.0, 79.0), ('8', 88.0, 88.0)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_7(self):
    	road=['5','4','8','2','3']
    	startPoint='7'
    	file='map.txt'
    	startTime=1020
    	result=[('7', 0, 0), ('4', 30, 56), ('3', 62, 75), ('2', 80, 85), ('5', 88, 91), ('8', 100, 100)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_8(self):
    	road=['5','4','8','2','3']
    	startPoint='7'
    	file='map.txt'
    	startTime=1077
    	result=[('7', 0, 0), ('4', 25.0, 51.0), ('3', 45.0, 58.0), ('2', 60.0, 65.0), ('5', 62.0, 65.0), ('8', 68.0, 68.0)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_9(self):
    	road=['5','4','8','2','3']
    	startPoint='7'
    	file='map2.txt'
    	startTime=1018
    	result=[('7', 0, 0), ('3', 97.5, 123.5), ('2', 121.5, 134.5), ('5', 133.5, 143.5), ('4', 157.5, 160.5), ('8', 174.5, 174.5)]
    	self.assertEqual(to_test(file,1020,1080,startPoint,road,startTime), result)
    def test_10(self):
    	road=['1']
    	startPoint='7'
    	file='map3.txt'
    	startTime=100
    	result=[('7', 0, 0), ('1', 6, 6)]
    	self.assertEqual(to_test(file,1002,1006,startPoint,road,startTime), result)
    def test_11(self):
    	road=['1']
    	startPoint='7'
    	file='map3.txt'
    	startTime=1000
    	result=[('7', 0, 0), ('1', 7.333333333333333, 7.333333333333333)]
    	self.assertEqual(to_test(file,1002,1006,startPoint,road,startTime), result)
    def test_12(self):
    	road=['1','4']
    	startPoint='7'
    	file='map3.txt'
    	startTime=1000
    	result=[('7', 0, 0), ('4', 10.0, 12.0), ('1', 12.333333333333332, 12.333333333333332)]
    	self.assertEqual(to_test(file,1002,1006,startPoint,road,startTime), result)       
if __name__ == '__main__':
	unittest.main()


