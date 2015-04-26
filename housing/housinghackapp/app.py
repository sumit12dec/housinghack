from flask import Flask, render_template, request, session, flash
import requests
import json
import config
import flask
import oauth2 as oauth

app = Flask(__name__)
app.config.from_object(config)


# main index
@app.route("/")
def index():
	return render_template("index.html")

# cobrand session token
@app.route("/callYahoo", methods=["GET","POST"])
def callYahoo():
	statement = request.args.get("q")
	statement = statement.replace(' ','-')
	website = request.args.get("site")
	#print website,"___________"

	if website==None:
		website = "timesofindia.indiatimes.com,thehindu.com,indiatoday.intoday.in,telegraphindia.com,\
		ibnlive.in.com,indianexpress.com,hindustantimes.com,ndtv.com"

	# Create your consumer with the proper key/secret.
	consumer = oauth.Consumer(key="dj0yJmk9aW84dlozR2ZpdzdRJmQ9WVdrOVlUQktOa1pQTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lMg--", secret="0ae950117a5cf4f9a31c2542660c8c6cb51216b4")

	# Request token URL for Twitter.
	request_token_url = "https://yboss.yahooapis.com/ysearch/web?q="+ statement +"&sites="+website+"&format=json"
	#print request_token_url,"+++++++++"
	# Create our client.
	client = oauth.Client(consumer)

	# The OAuth Client request works just like httplib2 for the most part.
	resp, content = client.request(request_token_url, "GET")
	#print resp
	#print content
	json_object = json.loads(content)
	ret = validate(json_object,statement)
	if ret==1:
		return '1'
	else:
		return '0'


global rumour_words
rumour_words = ['rumour','gossip','hearsay','tittle-tattle','fake','alleged']
global score
score = {'timesofindia':22,'ndtv':8,'indiatoday':3,'ibnlive':3,'thehindu':2,'indianexpress':2,'hindustantimes':1,'telegraphindia':0}
def containsRumour(text,final_score,url):

	#url = "https://housinghack.herokuapp.com/API?url=" +url
	#a = requests.get(url)
	#obj = json.loads(a.text)
	to_be_substracted_score = site_based_score(url)
	print final_score,to_be_substracted_score,"88888888"
	#pure_text = obj['main_text']
	for each in rumour_words:
		if each in text:
			final_score -= to_be_substracted_score
	print final_score
	return final_score
			

def site_based_score(url):
	for each in score:
		if each in url:
			to_be_given_score = score[each]
	return to_be_given_score

def score_logic(text, statement, url):
	
	final_score = 0	
	found_count = 0
	to_be_given_score = site_based_score(url)
	print to_be_given_score,url,"44444444"
	statement_words = statement.split('-')
	for each_statement_word in statement_words:
		if each_statement_word in text:
			found_count+=1
	print found_count,len(statement_words),"55555555"
	if found_count/float(len(statement_words))>0.6:
		final_score+=to_be_given_score
	print final_score,"6666666666"
	final_score_after_rumour_check = containsRumour(text, final_score,url)
	print final_score_after_rumour_check,"77777777"
	return final_score_after_rumour_check

def max_score(list_of_dicts):
	scoring = 0
	for each in list_of_dicts:
		for each_name in score:
			if each_name in each['url']:
				scoring+=score[each_name]
	return scoring


def validate(json_object,statement):
	result_set = json_object
	list_of_dicts = result_set['bossresponse']['web'].get('results',-1)
	true_count = 0
	false_count = 0
	if list_of_dicts!=-1:
		max_possible_score = max_score(list_of_dicts)
		abstract_score = 0
		for each in list_of_dicts:
			abstract_score += score_logic(each['abstract']+' '+each['title'],statement,each['url'])
		if abstract_score>=max_possible_score/1.4: #70%
			true_count+=1
		else:
			false_count+=1
	else:
		false_count=999
	print true_count,false_count,"111111"
	#print max_possible_score,"2222222"
	#print abstract_score,"33333333"
	if true_count>false_count:
		return 1
	else:
		return 0



@app.route("/callYahooAPI", methods=["GET","POST"])
def callYahooAPI():
	statement = request.args.get("q")
	statement = statement.replace(' ','-')
	website = request.args.get("site")
	#print website,"_________"
	if website==None:
		website = "timesofindia.indiatimes.com,thehindu.com,indiatoday.intoday.in,telegraphindia.com,\
		ibnlive.in.com,indianexpress.com,hindustantimes.com,ndtv.com"
	else:
		website = website
	import oauth2 as oauth

	# Create your consumer with the proper key/secret.
	consumer = oauth.Consumer(key="dj0yJmk9aW84dlozR2ZpdzdRJmQ9WVdrOVlUQktOa1pQTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD1lMg--", secret="0ae950117a5cf4f9a31c2542660c8c6cb51216b4")

	# Request token URL for Twitter.
	request_token_url = "https://yboss.yahooapis.com/ysearch/web?q="+ statement +"&sites="+website+"&format=json"
	#print request_token_url,"+++++++++"
	# Create our client.
	client = oauth.Client(consumer)

	# The OAuth Client request works just like httplib2 for the most part.
	resp, content = client.request(request_token_url, "GET")
	#print resp
	#print content
	json_object = json.loads(content)
	return flask.jsonify(**json_object)

if __name__ == "__main__":
	app.run(debug=True)