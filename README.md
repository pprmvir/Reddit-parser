# Reddit-parser
this program goes through reddit.com and generate list of all the subreddits. Then it generates a csv file which has the list sorted in the decreasing order of subscribers.

this program is tested on Windows 7, python 2.7.9

libraries required:
BeautifulSoup4, requests.

this script will generate the list of all the subs(including NSFW subs).
If you want only sfw, replace "div_midcol" with "not div_midcol" in the line 76
