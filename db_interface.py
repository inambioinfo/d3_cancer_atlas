#DB interface, using MongoDB

import pymongo #This interface uses MongoDB, but is kept modular just in case...

def submit_event_to_db(type, success, time, session_key):
	print "EVENT"
	print type, success, time, session_key