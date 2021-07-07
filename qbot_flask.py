from flask import Flask, Markup, redirect

from qbot_actions import QbotActions

app = Flask(__name__)

qa = QbotActions()
player_list = []

@app.route('/')
def dashboard():
	with open('dashboard.html', 'r') as f:
		html = f.read()
	return html

@app.route('/discord')
def discord():
	return redirect('https://discord.gg/2eqKB828GA')

@app.route('/dashlist')
def dash_list():
	if len(player_list) == 0:
		return 'The list is empty! Use !challenge to join!'
	response = 'On Stream: <br>'
	response += player_list[0]+'<br>'
	response += 'Up Next:<br>'
	response += '<br>'.join(player_list[1:]) if len(player_list) > 1 else 'None'
	return Markup(response)

@app.route('/list')
def list():
	response = 'On Stream: '
	response += (player_list[0]+' ('+qa.get_pronouns(player_list[0])+')' if len(player_list) > 0 else 'None') + '         '
	response += 'Up Next: '
	response += ', '.join(player_list[1:2]) if len(player_list) > 1 else 'None'
	return response

@app.route('/add/<name>')
def add(name):
	if name in player_list:
		response = '@'+name+' you are already in the list!'
	else:
		player_list.append(name)
		i = player_list.index(name)
		if i == 0:
			response = '@'+name+' you are up!'
		elif i == 1:
			response = '@'+name+' you are up next!'
		else:
			response = '@'+name+' you will be up in '+str(i)+' matches!'
	return response

@app.route('/clear')
def clear():
	while len(player_list) > 0:
		player_list.pop()
	return 'The list has been cleared'

@app.route('/drop/<name>')
def drop(name):
	try:
		player_list.remove(name)
		response = 'Removed @'+name+' from the list'
	except:
		response = '@'+name+' is not in the list!'
	return response

@app.route('/next')
def next():
	last = player_list.pop(0)
	response = 'Thanks for playing @'+last+'!'
	if len(player_list) > 0:
		 response += ' @'+player_list[0]+' is up next!'
	return response

@app.route('/win')
def win():
	last = player_list[0]
	data = qa.db.read()
	if last not in data:
		data[last] = qa.db.new_user()
	data[last]['wins'] += 1
	qa.db.write(data)
	response = 'Nice one @'+last+'!'
	return response

@app.route('/loss')
def loss():
	last = player_list[0]
	data = qa.db.read()
	if last not in data:
		data[last] = qa.db.new_user()
	data[last]['losses'] += 1
	qa.db.write(data)
	response = 'Try again!'
	return response

@app.route('/record/<name>')
def record(name):
	data = qa.db.read()
	if name not in data:
		response = 'You aren\'t in the database!'
	else:
		response = 'Your record is '+str(data[name]['wins'])+' wins and '+str(data[name]['losses'])+' losses'

	return response

@app.route('/pronouns/<name>/<choice>')
def pronouns(name, choice):
	data = qa.db.read()
	if name not in data:
		data[name] = qa.db.new_user()
	data[name]['pronouns'] = choice
	qa.db.write(data)
	response = 'Thank you @'+name+' for setting your pronouns!'
	return response

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000, ssl_context='adhoc')