from flask import Flask, redirect, request, render_template
import requests
import random
import enums
import rr
import ssl
import logging

# Bungie API credentials
API_KEY = '7c32dbde2d5c4d719d0b6e610a6901e6'
API_SECRET = 'v9RSYBGvGNrhjPk7TTjYILf3XuWIIfNtOoy0d0YXVwc'
CLIENT_ID = '34226'

app = Flask(__name__, template_folder="static")
app.logger.setLevel(logging.DEBUG)

def getAuthToken(authCode):
	url = 'https://www.bungie.net/platform/app/oauth/token/'
	headers = {'Content-Type': 'application/x-www-form-urlencoded'}

	data = {
    'grant_type': 'authorization_code',
    'code': authCode,
    'client_id': CLIENT_ID,
    'client_secret': API_SECRET,
	}

	response = requests.post(url, headers=headers, data=data)

	if response.status_code == 200:
		access_token = response.json()['access_token']
		return access_token
	else:
		return f'Error: {response.json()["error_description"]}'
		
		
def getMembershipId(auth_token):	
	headers = {
		"X-API-Key": API_KEY,
		"Authorization": f"Bearer {auth_token}"
	}
	response = requests.get("https://www.bungie.net/Platform/User/GetMembershipsForCurrentUser/", headers=headers)
	if response.status_code == 200:
		memberships = response.json()["Response"]["destinyMemberships"]
		for membership in memberships:
			membership_id = membership["membershipId"]
			return membership_id
	else:
		return f'Error: {response.json()["error_description"]}'


@app.route('/')
def index():
    # store the variable
    discord_id = request.args.get("discord_id")
    
    # redirect the user to an OAuth page
    oauth_url = 'https://www.bungie.net/en/OAuth/Authorize'
    params = {
        'client_id': CLIENT_ID,
        'response_type': 'code',
        'state': discord_id
    }
    oauth_redirect_url = f'{oauth_url}?' + ''.join([f'{k}={v}&' for k, v in params.items()])[:-1]    
    return redirect(oauth_redirect_url)



@app.route('/auth')
def auth():
	auth_token = getAuthToken(request.args.get("code"))
	if auth_token[0:5] == "Error":
		return render_template('index.html', title="Error while authorizing", message=auth_token)
	else:
		membership_id = getMembershipId(auth_token)
		print(membership_id)
		if membership_id[0:5] == "Error":
			return render_template('index.html', title="Error while authorizing", message=membership_id)
		else:
			discord_id = request.args.get("state")
			print(f"Membership ID: {membership_id}")
			print(f'Discord ID: {request.args.get("state")}')
			rr.dodajKonto(membership_id, discord_id)
			return render_template('index.html', title="Authorization success!", message="Thank you for registering with Elitist! You can now safely close this page")
	

if __name__ == "__main__":
	#context = ssl.SSLContext(ssl.PROTOCOL_TLS)
	#context.load_cert_chain('cert/cert.pem', 'cert/key.pem')
	app.run(host="0.0.0.0", port=8000, ssl_context=('cert/cert.pem', 'cert/key.pem'))
