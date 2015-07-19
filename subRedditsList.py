from bs4 import BeautifulSoup as bs
from csv import writer
from time import sleep
import requests as req
import cookielib
import mechanize

def write_to_csv(l):
        n = open('SUBS.csv','w')
        w = writer(n,dialect='excel')        
        l.sort(key=lambda l:int(l[2].replace(',','')),reverse=True)
        w.writerows(l)
        n.close()
        return

headers = {'User-Agent':'My User Agent 1.0'}

cookie = { # this cookie lets you bypass the age filter
            'over18' : '1',
            'path' : '/',
            'domain' : '.reddit.com'
            }

try:        
        link_to_sub_reddits = 'http://www.reddit.com/subreddits'

        L=[]
        navigate_the_pages=1

        while navigate_the_pages:
                
                if link_to_sub_reddits == 'end':
                        break
                
                try:
                        
                        res = req.get(link_to_sub_reddits,headers=headers,timeout=10
                                      , cookies=cookie)
                        print navigate_the_pages
                        navigate_the_pages=navigate_the_pages+1                        
                        
                except req.ConnectionError as e:
                        print e                        
                        print len(L)
                        print link_to_sub_reddits
                        print 'writing to .csv .......'
                        write_to_csv(L)
                        print 'done'
                        break
                
                soup = bs(res.text,"html.parser")
                # soup created

                div = soup.body.find('div', class_=lambda(class_):class_ and class_=='content')
                div = div.find('div', id= lambda(id):id and id=='siteTable')

                cnt=0

                for iterator in div:

                    div_thing = div.contents[cnt]

                    
                    if div_thing:
                            div_midcol = div_thing.find('img')                            
                                                      
                            if div_midcol and div_midcol['title']=='over18':
                                    hijj = 'llsls' # just command to fill in the
                                    # space of if clause, feel free to change
                                    # of you wish
                            else:                                    
                                    div_midcol = None 
                    else:
                            div_midcol = None 
        
                    if div_midcol and not div_thing=='' and div_thing.name=='div' and 'thing' in div_thing['class']:
                    # if you want sfw subs, replace "div_midcol"  with "not div_midcol"
                    # in the above if clause
                        
                        div_entry = div_thing.find('div',class_=lambda(class_):class_ and 'entry' in class_)
                        # div with class='entry......'
                        
                        link = div_entry.find('a')['href']
                        print link
                        # link of the subreddit
                        name_of_sub = link.split('/')[-2]
                        # http://www.reddit.com/subreddits/
                        # ['http:', '', 'www.reddit.com', 'subreddits', '']

                        description = div_entry.find('div',class_='md')
                        if description:
                                description = description.text
                        else:
                                description = '------'                                
                        # something about the community

                        p_tagline = div_entry.find('p',class_='tagline')
                        subscribers = p_tagline.find('span',class_='number')
                        if subscribers:
                                subscribers = subscribers.text
                        else:
                                subscribers = u'-1'

                        temp = [name_of_sub, description, subscribers, link]
                        temp = [s.encode('ascii','ignore') for s in temp]
                        L.append(temp)

                    elif not div_thing=='' and div_thing.name=='div' and 'nav-buttons' in div_thing['class']:
                        # case when we find 'nav' button

                        link_to_sub_reddits = div_thing.find('a',rel = 'nofollow next')
                        
                        if link_to_sub_reddits:
                                link_to_sub_reddits = link_to_sub_reddits['href']
                        else:
                                link_to_sub_reddits = 'end'
                        break

                    cnt = cnt + 1
                print 'NEXT LINK TO VISIT'
                print link_to_sub_reddits                
            
except req.ConnectionError as e:        
        print e
