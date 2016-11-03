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


		ships.append(ship)

		# print these to the console
		# print " "
		# print "Ship " + str(j+1)
		# for key in ship:
		# 	print key +': '+ str(ship[key])


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
# 	Function to determine the player's dice rolls
# 
# def player_rolls(num_rolls):
# 	rolls = []
# 	for i in range(num_rolls):
# 		rolls.append(r.random())
# 	return rolls


# # 
# 	Function to determine if the player wins
# 
def calculate_victories():
	# for i, roll in enumerate(rolls):
		# if roll > session['ships'][i]['target']:
			# session['ships'][i]['victory'] = True
		# else:
			# session['ships'][i]['victory'] = False
	for i, ship in enumerate(session['ships']):
		# print ship['target']
		roll = round(r.random(),2)
		ship['player_roll'] = roll
		if roll >= ship['target']:
		# if rolls[i] >= ship['target']:
			ship['victory'] = 1
			session['ships_data']['total_reward'] += ship['reward']
		else:
			ship['victory'] = 0	



def ships_data():
	ships_data = {}
	ships_data['resources_allocated'] = 0
	ships_data['total_reward'] = 0
	return ships_data

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
	session['ships_data'] = ships_data()
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
		return render_template('risk.html', ships = session['ships'], gameMode = session['game_mode'])
	else :
		return redirect(url_for('index'))

# 
# 	Map battle page
# 
@app.route('/map-battle', methods=['GET'])
def map_battle():
	if session.has_key('ships'):
		print session['ships_data']
		#  if we don't do this, they can mash refresh until they win!
		# if not session['ships_data']['resources_allocated']:
			# session['ships_data']['resources_allocated'] = True

			# print session['ships_data']['resources_allocated']
		if not session.has_key('resources_are_allocated'):
			session['ships_data']['resources_allocated'] = 1
			session['resources_are_allocated'] = True
			calculate_victories()

		# print investments
		return render_template('map.html', ships = session['ships'], ships_data = session['ships_data'])
	else :
		return redirect(url_for('index'))




# 
# 	result page
# 
@app.route('/result', methods=['GET'])
def result():
	if session.has_key('ships'):
		reward = request.args.get('r')
		return reward
		# return render_template("game-over.html" reward=reward)
	else:
		return redirect(url_for('index'))

@app.route('/try_again')
def try_again():
	del session['resources_are_allocated']
	return redirect(url_for('index'))



if __name__ == '__main__':
   app.run(debug = True)