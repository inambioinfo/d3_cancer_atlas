#  import for flask
from flask import Flask, render_template, request, session, redirect, url_for
app = Flask(__name__)


#  import for generating session key
from os import urandom
app.secret_key = urandom(24)

#  import for ship-building funcitons
import random as r
from math import floor

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

		# push the middle value to the 'target' variable of the ship

		# Start with it being the same as the minimum value, just incase it's the same as either the max or min value
		ship['target'] = min(rands)
		for k in range(3):
			if rands[k] != min(rands) and rands[k] != max(rands):
				ship['target'] = rands[k]
				
		# push min/max values of risk to the ship
		ship['min'] = min(rands)
		ship['max'] = max(rands)

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
	if session.has_key('ships'):
		return render_template('map.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'])
	else :
		return redirect(url_for('index'))

# 
# 	Resource allocation page
# 
@app.route('/risk')
def risk():
	if session.has_key('ships'):
		return render_template('risk.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'], reminder = False)
	else :
		return redirect(url_for('index'))


@app.route('/risk_reminder')
def risk_reminder():
	if session.has_key('ships'):
		return render_template('risk.html', ships = session['ships'], gameMode = session['game_mode'], ships_data = session['ships_data'], reminder = True)
	else :
		return redirect(url_for('index'))


# 
# 	Map battle page
# 
@app.route('/map-battle', methods=['GET'])
def map_battle():
	if session.has_key('ships'):

		# check and see if they've spent all their money
		has_spent_all_money = request.args.get('sum') == '30'
		# print has_spent_all_money
		if has_spent_all_money:
			#  if we don't do this next bit, they can mash refresh until they win!
			if not session.has_key('resources_are_allocated'):
				session['ships_data']['resources_allocated'] = 1
				session['resources_are_allocated'] = True
				allocation = [request.args.get('ship_1'), request.args.get('ship_2'), request.args.get('ship_3')]
				calculate_victories(allocation)

			# this is where we should dump the data to the server, I guess...

			# print investments
			return render_template('map.html', ships = session['ships'], ships_data = session['ships_data'])
		else:
			# print "remember to spend all your money"
			return redirect(url_for('risk_reminder'))
	else :
		return redirect(url_for('index'))



# 
# 	Play another round
# 
@app.route('/try_again')
def try_again():
	if session.has_key('ships'):
		# clear the flag that says that the player has assigned resources to each ship
		del session['resources_are_allocated']
	return redirect(url_for('index'))



@app.route('/survey')
def survey():
	if session.has_key('ships'):
		return render_template('survey.html', ships = session['ships'], ships_data = session['ships_data'], gameMode = session['game_mode'])
	else:
		redirect(url_for('index'))


@app.route('/submit_survey', methods=['POST'])
def submit_survey():
	for arg in request.form:
		print arg, ':', request.form[arg]
	return redirect(url_for('thank_you'))

@app.route('/thank_you' )
def thank_you():
	return render_template('thankyou.html')



if __name__ == '__main__':
   app.run()




# import os
# from project import main

# if __name__ == '__main__':
#     port = int(os.environ.get('PORT', 5000))
#     main.app.run(host='0.0.0.0', port=port)
