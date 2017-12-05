import urllib.request
import re
import config
import time
from time import gmtime, strftime

def set_configs():
	# create a password manager
	password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()

	# Add the username and password.
	# If we knew the realm, we could use it instead of None.
	password_mgr.add_password(None, config.ip, config.user, config.password)

	handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

	# create "opener" (OpenerDirector instance)
	opener = urllib.request.build_opener(handler)

	# Install the opener.
	# Now all calls to urllib.request.urlopen use our opener.
	urllib.request.install_opener(opener)

def run():
	content = str(urllib.request.urlopen(config.url).read())
	snr = re.search('(?<=SNR Margin).*?(?=db)', content).group(0)[114:118]
	if(snr == 'N/A<'):
		snr = '-'
	else:
		snr = str(float(snr))
		
	with open("status.txt", "a") as fw:
				fw.write(snr+ "," + strftime("%Y-%m-%d %H:%M:%S") + "\n")
	


set_configs()
while True:
	run()
	time.sleep(config.wait)