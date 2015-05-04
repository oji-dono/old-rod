# old-rod
-------------------------
"""Shoplift is a bug in the popular Magento e-commerce software that allows a hacker to take full control of a shop. It was discovered by Check Point and fixed by patch SUPEE-5344. However, a survey at April 14th revealed that 60% of Magento installations have not applied the patch yet. This translates to 140,000 vulnerable Magento shops worldwide.""" --https://shoplift.byte.nl/


old-rod.py* is a custom python script for exploiting the Magento Shoplift Vulnerability.

*oldrod is the fishing rod tool from Pokemon. In the Gen I Pokemon games, all it could catch was Lvl.5 Magikarp
*Although, at the time of writing, there are 65,377 vulnerable Magento installs and counting^, They all seem like Lvl.5 Magikarp to me. All the Gyrados wisened up.

*And counting because the main Magento install does not come with any previous patches installed. 
*As such, Magento is propogating victims quicker than they're customers are patching, with new customers being potential targets for malicous actors.

http://s16.postimg.org/nlc7i1of9/vic_Increase.jpg

***I have NO motive for writing this. I just wanted to write practical code that Does have the potential to affect another human's life, for better or worse.

Main Usage:
python old-rod.py example.com

old-rod will run in Test mode. It will report back if site was vulnerable.

python old-rod.py -a

old-rod.py will run in Heavy mode. It will attempt to create an admin account via SQL injection with credentials:
Username: defaultmanager
password: password
It will report back with it's success.
Note: This attack has highest chance of success compared with others

python old-rod.py -m

old-rod.py will run in Sneaky Sneaky mode. It will attempt to install PHP based malware on remote server using SQL injection, then try to instantiate them with Magento Installations' get.php page. Filename's are:
- hook.php {Navigate to 'victim.com/media/wysiwyg/hook.php?cmd=' Anything appended here will attempt to run as a system command if alls well}
- sinker.php {Navigate to 'victim.com/media/wysiwyg/sinker.php' As having PHP files in a picture directory is suspicious, visiting this link will make them self-destruct.
- Use hook.php system injection to drop a msfvenom-made PHP shell on the remote server then use sinker.php to remove the php files after you've setup a persistent entry.
python old-rod.py -a -m

old-rod.py will run in Going In Loud mode. It will attempt both of the above operations:
- !Not Recommended!
- I feel like when one fails, they both fail. Not quite grounded in science, but I don't feel like experimenting, only threw it in because it seems intuitive to have an option for running both Ops at once.

As a second opinion, old-rod.py will consult the shoplift.byte.nl api and report back.
If both old-rod.py & shoplift.byte.nl return positive, site is likely vulnerable.
If there is a disagreement, someone has a false-positive. Some sites don't respond like others and the shoplift.byte.nl api doesn't actually try to exploit the Shoplift bug. It runs in a manner almost identical to old-rod.py's Test Mode.

------------------------------------------------------------------------------------------------------------

If server responds, especially if similar to responses of those in the wild, with either:
- a default image
- an image encoded in base64
- a Magento error page complaining of an unsupported image type,
Then old-rod.py will report back as site being vulnerable.
