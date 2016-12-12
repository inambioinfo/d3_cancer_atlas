#  import for flask
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)

import json

#Copy from StackOverflow-----------------------------
from os import path
import os

extra_dirs = ['static','templates']
extra_files = extra_dirs[:]
for extra_dir in extra_dirs:
    for dirname, dirs, files in os.walk(extra_dir):
        for filename in files:
            filename = path.join(dirname, filename)
            if path.isfile(filename):
                extra_files.append(filename)
#app.run(extra_files=extra_files)
#End copy-----------------------------------------------

#import for database
from db_interface import submit_event_to_db, submit_game_to_db, submit_result_to_db, submit_survey_to_db

#  import for generating session key
from os import urandom
app.secret_key = urandom(24)


#  import for ship-building funcitons
import random as r
from math import floor

#Session ID based on timing
import time

# 
# 
# 	Function to build the ships to play the game.  The ships are generated on the index page, so the player must not skip this step!
# 
# 

def build_ships():
	
	ships = []


	for j in range(3):

		# Somewhere to store the random numbers
		rands = []

		# Somewhere to store the ship information
		ship = {}
		ship['number'] = j
		# we need a lower, target and max value for the risk, so grab 3 random numbers
		for i in range(3):
			rands.append(round(r.random(),2))
			#The range could stand to be a bit narrower.

		rands.sort()
	
		# push min/max values of risk to the ship
		ship['min'] = rands[0]
		ship['target'] = rands[1]
		ship['max'] = rands[2]

		# push margin of error and median of min/max risk values to the ship
		ship['plus_minus'] = round((ship['max'] - ship['min'])/2,2)
		ship['median'] = round(ship['min'] + ship['plus_minus'], 2)

		# determine the type of ship based on the median value
		if ship['median'] <= 0.25:
			ship['type'] = "Sloop"
		elif ship['median'] <= 0.5:
			ship['type'] = "Cutter"
		elif ship['median'] <= 0.75:
			ship['type'] = "Schooner"
		else:
			ship['type'] = "Frigate"
		# ships.append(ship)

		# randomly pick reward for defeating the ship, and assign nationality based on this
		ship['reward'] = int(round(r.random()*40 + 10))
		if ship['reward'] <= 20:
			ship['nationality'] = "British"
		elif ship['reward'] <= 30:
			ship['nationality'] = "French"
		elif ship['reward'] <= 40:
			ship['nationality'] = "Dutch"
		else:
			ship['nationality'] = "Spanish"

		# determine semantic risk 
		if ship['min'] <= 0.15:
			ship['lower_semantic_risk'] = "Well below average"
		elif ship['min'] <= 0.30:
			ship['lower_semantic_risk'] = "Below average"
		elif ship['min'] <= 0.45:
			ship['lower_semantic_risk'] = "Slightly below average"
		elif ship['min'] <= 0.55:
			ship['lower_semantic_risk'] = "Average"
		elif ship['min'] <= 0.70:
			ship['lower_semantic_risk'] = "Slightly above average"
		elif ship['min'] <= 0.85:
			ship['lower_semantic_risk'] = "Above average"
		else:
			ship['lower_semantic_risk'] = "Well above average"


		if ship['max'] <= 0.15:
			ship['upper_semantic_risk'] = "Well below average"
		elif ship['max'] <= 0.30:
			ship['upper_semantic_risk'] = "Below average"
		elif ship['max'] <= 0.45:
			ship['upper_semantic_risk'] = "Slightly below average"
		elif ship['max'] <= 0.55:
			ship['upper_semantic_risk'] = "Average"
		elif ship['max'] <= 0.70:
			ship['upper_semantic_risk'] = "Slightly above average"
		elif ship['max'] <= 0.85:
			ship['upper_semantic_risk'] = "Above average"
		else:
			ship['upper_semantic_risk'] = "Well above average"


		if ship['median'] <= 0.15:
			ship['median_semantic_risk'] = "Well below average"
		elif ship['median'] <= 0.30:
			ship['median_semantic_risk'] = "Below average"
		elif ship['median'] <= 0.45:
			ship['median_semantic_risk'] = "Slightly below average"
		elif ship['median'] <= 0.55:
			ship['median_semantic_risk'] = "Average"
		elif ship['median'] <= 0.70:
			ship['median_semantic_risk'] = "Slightly above average"
		elif ship['median'] <= 0.85:
			ship['median_semantic_risk'] = "Above average"
		else:
			ship['median_semantic_risk'] = "Well above average"

		ship['allocated'] = 0	
		#  in case we need to remind that there is 30 doubloons to spend
		# add each ship to the list of ships
		ships.append(ship)


	return ships

# 
# 	Function to determine the game mode presented to the player
# 
def game_mode():
	game_mode = floor(r.random() * 3)
	if game_mode > 2:
		game_mode = 2
	return game_mode

# 
# 	Function to determine if the player wins
# 
def calculate_victories(allocation):

	for i, ship in enumerate(session['ships']):
		roll = round(r.random(),2)
		ship['player_roll'] = roll
		ship['allocated'] = int(allocation[i])
		if roll >= ship['target'] - int(allocation[i]):
			ship['victory'] = 1
			ship['outcome'] = 'victory'
			session['ships_data']['total_reward'] += ship['reward']
		else:
			ship['victory'] = 0	
			ship['outcome'] = 'defeat'


# 
# 
# 	Functions to return pages
# 
# 



# 
# 	index/landing page
# 
@app.route('/')
def index():
	if not session.has_key('db_id'):
		session['db_id'] = str(int(time.time() * 1000)) + str(r.randint(100,999)) #Let us hope that we don't need more than a few sessions per second... ...or that we operate in an environment where time.time has millisecond resolution. Just in case, add a 3-digit random number to the end.
		session['game_number'] = 0
		session['game_stage'] = 0
		session['surveyed'] = False
	session['ships'] = build_ships()
	session['game_mode'] = game_mode()
	session['ships_data'] = {}
	session['ships_data']['resources_allocated'] = 0
	session['ships_data']['total_reward'] = 0
	session['ships_data']['reminder'] = 0

	return render_template('index.html', ships = session['ships'], gameMode = session['game_mode'])

# 
# 	Map page
# 
@app.route('/map')
def map():
	if session.has_key('game_stage'):
		session['game_stage'] = 10 #Increment in 10s, use intermediate values for reload resistance.
		return render_template('map.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'])
	else :
		return redirect(url_for('index'))

# 
# 	Resource allocation page
# 
@app.route('/risk')
def risk():
	if session.has_key('game_stage'):
		session['game_stage'] = 20
		return render_template('risk.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'], reminder = False)
	else :
		return redirect(url_for('index'))


@app.route('/risk_reminder')
def risk_reminder():
	if session.has_key('game_stage'):
		submit_event_to_db("REMINDER", True, request.args.get('time'), session['db_id'])
		return render_template('risk.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'], reminder = True)
	else :
		return redirect(url_for('index'))


# 
# 	Map battle page
# 
@app.route('/map-battle', methods=['GET'])
def map_battle():
	if session.has_key('game_stage'):
		# check and see if they've spent all their money
		has_spent_all_money = request.args.get('sum') == '30'
		# print has_spent_all_money
		if has_spent_all_money:
			#  if we don't do this next bit, they can mash refresh until they win!
			if (session['game_stage'] < 30):
				session['game_stage'] = 30
				
				session['ships_data']['resources_allocated'] = 1
				
				allocation = [request.args.get('ship_1'), request.args.get('ship_2'), request.args.get('ship_3')]
				calculate_victories(allocation)

				submit_event_to_db("FINALISE", True, request.args.get('time'), session['db_id'])
				#Results are submitted away from generations, as the player may quit before getting a result.
				submit_result_to_db(session['ships'], session['game_number'], request.args.get('time'), session['db_id'])

			# print investments
			return render_template('map.html', ships = session['ships'], ships_data = session['ships_data'], message = r.choice([0,1]))
		else:
			# print "remember to spend all your money"
			return redirect(url_for('risk_reminder') + '?time=' + request.args.get('time'))
	else:
		return redirect(url_for('index'))



# 
# 	Play another round
# 
@app.route('/try_again')
def try_again():
	if session.has_key('game_stage') and session['game_stage'] == 30: #Don't let them reset their game too soon...
		session['game_number'] += 1
		session['game_stage'] = 0
	return redirect(url_for('index'))

#
#	Recieve data
#
@app.route('/log_submit', methods=['POST'])
def recieve_event_data():
	if (session.has_key('game_stage')):
		if 20 <= session['game_stage'] < 30:
			#print request.is_json
			result = request.get_json()
			#print "Result: ", result
			submit_event_to_db(result.get("event"), result.get("success"), result.get("time"), session['db_id'])
			if session['game_stage'] < 25: #In case of BACK/FORWARD, ensure that this only executes once...
				session['game_stage'] = 25 #Partway through this stage...
				submit_game_to_db(session['ships'], session['game_mode'], session['game_number'], result.get('time'), session['db_id']) #Here, to collect data from abandoned-later games.
		else:
			print "Someone hit BACK, this data is irrelevant..."
	return "" #This should never be navigated to.

@app.route('/survey')
def survey():
	if session.has_key('game_stage') and session['game_stage'] >= 30 and not session['surveyed']:
		return render_template('survey.html')
	else:
		return redirect(url_for('index'))


@app.route('/submit_survey', methods=['POST'])
def submit_survey():
	if session.has_key('game_stage') and session['game_stage'] >= 30 and not session['surveyed']:
		session['surveyed'] = True
		submit_survey_to_db(request.form, session['db_id'])
		return redirect(url_for('thank_you'))
	else:
		return redirect(url_for('index'))

@app.route('/thank_you' )
def thank_you():
	if session.has_key('surveyed') and session['surveyed']:
		if session.has_key('game_stage') and session['game_stage'] == 30: #Don't let them reset their game too soon...
			session['game_number'] += 1
			session['game_stage'] = 0
		return render_template('thankyou.html')
	else:
		return redirect(url_for('index'))

if __name__ == '__main__':
	#print(extra_files)
	app.run(extra_files=extra_files)



# import os
# from project import main

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     main.app.run(host='0.0.0.0', port=port)
