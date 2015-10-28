from RedditImages import RedditImageDownload as api


userlist =[ 'SL_Delight','wander_myway']

for user in userlist:
    print 'STARTING FOR %s'%user
    url='https://www.reddit.com/user/'+user+'/submitted/'
    x=api(user)
    x.RedditLinks(url)
    print 'DONE FOR %s'%user
