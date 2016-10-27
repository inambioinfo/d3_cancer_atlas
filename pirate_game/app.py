from flask import Flask, render_template
app = Flask(__name__)

@app.route('/risk')
def risk():
	import random as r
	from math import floor
	ships = []
	game_mode = floor(r.random() * 2.9999999999)

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
		ship['reward'] = round(r.random()*40 + 10)
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
		print " "
		print "Ship " + str(j+1)
		for key in ship:
			print key +': '+ str(ship[key])


	return render_template('risk.html', ships = ships, gameMode = game_mode)

if __name__ == '__main__':
   app.run(debug = True)