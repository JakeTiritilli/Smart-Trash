import json
from datetime import datetime

class AverageTime:
	
	def __init__(self, can_id: str):
		self._can_id = can_id
		self._trash_can_data = []
				
	@staticmethod
	def str_to_datetime(iso_date: str):
		return datetime.strptime(iso_date, "%Y-%m-%dT%H:%M:%S")
		
	@staticmethod
	def time_delta_to_secs(time_delta):
		return time_delta.seconds + (time_delta.days * 86400)
				
	def display(self):
		self._load_data()
		for cycle in self._trash_data:
			for time_type, time in cycle.items():
				print("Type:", time_type, end="  ")
				print("Time:", time)
			print()
			
	def _get_avg_time(self, starting_time: str, ending_time: str):
		total_time = 0
		cycle_count = 0
		for cycle in self._trash_data:
			if cycle.get(ending_time) != None and cycle.get(starting_time) != None:
				start_time = self.str_to_datetime(cycle[starting_time])
				end_time = self.str_to_datetime(cycle[ending_time])
				time_diff = end_time - start_time
				total_time += self.time_delta_to_secs(time_diff)
				cycle_count += 1
		return round(total_time / cycle_count)
		
	def _get_heighest_trash_month(self):
		trash_frequency = [0 for _ in range(12)]
		for cycle in self._trash_data:
			if cycle.get("time taken out") != None and cycle.get("starting time") != None:
				start_time = self.str_to_datetime(cycle["starting time"])
				index = start_time.month - 1
				trash_frequency[index] += 1
		return trash_frequency
		
	def _load_data(self):
		with open(self._can_id + ".json", "r") as data_file:
			self._trash_data = json.load(data_file)
		
	def avg_trash_cycle(self):
		"""Gets the average time that the garbage collectors went from being empty
		to being taken out.
		"""
		self._load_data()
		return self._get_avg_time("starting time", "time taken out")
		
	def avg_full_time(self):
		"""Gets the average time that the garbage collectors went from begin 100% full
		to being taken out.
		"""
		self._load_data()
		return self._get_avg_time("init time full", "time taken out")
		
	def avg_time_to_full(self):
		"""Gets the average time that the garbage collectors went from being empty to
		being full.
		"""
		self._load_data()
		return self._get_avg_time("starting time", "init time full")
		
	def heighest_trash_month(self):
		self._load_data()
		months = self._get_heighest_trash_month()
		return months.index(max(months))
		
					
if __name__ == '__main__':		
		test = AverageTime("can1")
		test.display()
		print("Avg time to take out:", test.avg_trash_cycle())
		print("Avg time full:", test.avg_full_time())
		print(test.heighest_trash_month())