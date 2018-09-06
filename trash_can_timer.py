import json
import time
import os.path
from datetime import datetime


class TrashCanTimer:
	
	def __init__(self, trash_id: str):
		self._trash_id = trash_id
		self._in_progress = False
		self._left_unfinished = False
		self._became_full = False
		is_existing_can = os.path.isfile(self._trash_id + ".json")
		mode = "r" if is_existing_can else "w"
		with open(self._trash_id + ".json", mode) as data_file:
			if not is_existing_can:
				json.dump([], data_file)
				self._cycles = 0
			else:
				data = json.load(data_file)
				self._left_unfinished = True if len(data[-1]) == 1 else False
		
	def set_start_time(self):
		"""Sets the time that the trash was intially empty (reset when the
		trash is taken out).
		"""
		if not self._in_progress:
			self._in_progress = True
			self._time_emptied = datetime.today()
			self._write_data("starting time", self._time_emptied.isoformat(timespec='seconds'), not self._left_unfinished)
			return self._time_emptied
		
	def set_taken_out(self):
		"""Sets the time that the trash became full (or was taken out)."""
		self._time_taken_out = datetime.today()
		self._write_data("time taken out", str(self._time_taken_out.isoformat(timespec='seconds')), False)
		self._in_progress = False
		self._left_unfinished = False
		return self._time_taken_out
	
	def set_time_full(self):
		"""Set the time that the trash can became full, in order to calculate
		how long the garbage was comletely full before being emtied.
		"""
		if not self._became_full:
			self._became_full = True
			self._time_full = datetime.today()
			self._write_data("init time full", self._time_full.isoformat(timespec='seconds'), False)
			return self._time_full		
		
	def _write_data(self, time_type: str, time: str, create_new: bool):
		"""Writes the specified data in JSON format to a file, by either
		creating a new entry in the array if a new cycle is being started
		or adding data to an existing object in the JSON text.
		"""
		with open(self._trash_id + ".json", "r+") as datafile:
			time_data = json.load(datafile)
			if create_new:
				time_data.append({time_type: time})
			else:
				time_data[-1][time_type] = time
			datafile.seek(0)
			json.dump(time_data, datafile)
		
	def get_id(self):
		"""Returns the id of the trash can."""
		return self._trash_id
		
	def is_in_progress(self):
		"""Returns whether or not the trash can timer is currently running
		or ready to be set again.
		"""
		return self._in_progress


if __name__ == '__main__':
	# Driver code for testing the TrashCanTimer Class
	can1 = TrashCanTimer("can3")
	print("Setting Init Time")
	can1.set_start_time()
	time.sleep(3)
	print("The trash can is full")
	can1.set_time_full()
	time.sleep(3)
	print("The trash can is being taken out")
	can1.set_taken_out()
	print("Starting Next Round\n---------------------")
	print("Setting Init Time")
	can1.set_start_time()
	time.sleep(2)
	print("The trash can is full")
	can1.set_time_full()
	time.sleep(2)
	print("The trash can is being taken out")
	can1.set_taken_out()
	time.sleep(4)
	print("Setting only start time")
	can1.set_start_time()
	