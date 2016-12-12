#DB interface, using MongoDB

from pymongo import MongoClient #This interface uses MongoDB, but is kept modular just in case...
client = MongoClient()

db = client.dev_db #Change this later...

coll_events = db.events
coll_games = db.games
coll_results = db.results
coll_surveys = db.surveys

def submit_event_to_db(type, success, time, session_key):
	print "EVENT:", type, success, time, session_key
	result = coll_events.insert_one(
			{"event":type, 
			"success":success, 
			"timestamp":time, 
			"session":session_key})
	
def submit_game_to_db(ships, game_mode, game_number, time, session_key):
	print "GAME"
	result = coll_games.insert_one(
			{'ships':summarize_ships_generated(ships),
			'game_mode':game_mode,
			'game_number':game_number,
			'session':session_key})

def submit_result_to_db(ships, game_number, time, session_key):
	print "RESULT"
	result = coll_results.insert_one(
			{'results':summarize_ships_battles(ships),
			'game_number':game_number, 
			'time':time,
			'session':session_key})
			
def submit_survey_to_db(form, session_key):
	print "SURVEY"
	db_record = {} #Need to add a key, so it's best to just write out the dict again.
	db_record['is-a-student'] = (True if form.get('is-a-student') else False)
	db_record['training-math-stats'] = (True if form.get('training-math-stats') else False)
	db_record['language-background'] = (True if form.get('language-background') else False)
	db_record['age-group'] = form['ageGroup']
	db_record['location'] = form['location']
	db_record['occupation'] = form['occupation']
	db_record['session'] = session_key
	for arg in form:
		print arg, ":", form[arg]
	result = coll_surveys.insert_one(db_record)
	
def summarize_ships_generated(ships):	
	summaries = []
	for i, ship in enumerate(ships):
		summary = {}
		summary['number'] = ship['number']
		summary['min'] = ship['min']
		summary['target'] = ship['target']
		summary['max'] = ship['max']
		summary['reward'] = ship['reward']
		summaries.append(summary)
	return summaries

def summarize_ships_battles(ships):
	summaries = []
	for i, ship in enumerate(ships):
		summary = {}
		summary['player_roll'] = ship['player_roll']
		summary['allocated'] = ship['allocated']
		#summary[''] = ship['']
		summaries.append(summary)
	return summaries