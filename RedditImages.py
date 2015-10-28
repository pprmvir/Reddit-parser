# this works for all domains of imgur and viddle
from bs4 import BeautifulSoup as BS
from urllib import urlretrieve as download
import requests
import os

cookie = { # this cookie lets you bypass the age filter
            'over18' : '1',
            'path' : '/',
            'domain' : '.reddit.com'
            }

class RedditImageDownload():

    def __init__(self,user='Fancy',al_no=0,\
                 filepath=r'D:\Photos\Reddit-users',threshold=-1):
        self.user=user
        self.al_no=al_no
        self.filepath=filepath
        self.threshold=threshold
    
    def makerequest(self,url):
        
        header={'user-agent':'Mozilla-Firefox'}
        try:
            res = requests.get(url,headers=header,timeout=60\
                               ,cookies=cookie)
        except requests.exceptions.RequestException as e:
            print e
            res='empty'        
        return res

    def makesoup(self,res):    
        soup = BS(res.text,"html.parser")
        return soup

    def downloadImage(self,url,pic_no,path):
    # this function download the image. Before dowloading
    # it checks whether or not it is already present.
        #download(url,filepath)

        name = '%d'%pic_no+'.'
        extension = url.split('.')[-1]
        if '?' in extension:
            extension=extension.split('?')[-2]

        name=name+'%s'%extension
        #D:\Photos\Reddit-users\user\user(1)\name.jpg
        filepath = path+r'\%s'%name
        if not os.path.exists(filepath):
            download(url,filepath)
            print 'done.....'
        else:
            print 'photo already exists'

    def RedditLinks(self,url):
    # this function parses the "REDDIT" url provided to it
    # then go through the links and send it to function
    # "album2Image"
        
        res = self.makerequest(url)
        if res!='empty' and res.status_code==200:
            soup = self.makesoup(res)
            div_site = soup.body.find('div',id= lambda l:\
                                      l and l=='siteTable')        
            cut=0
            if div_site:            
                for x in div_site:
                    if x!='' and x.name=='div' and 'thing' in x.get('class'):
                        cut=cut+1
                        for y in x:
                            if y and y.name=='a':
                                url=y.get('href')
                                print url
                                self.al_no=self.album2Image(url)
                                break
                        if cut==self.threshold:
                            print 'reached threshold. Exiting.......'
                            return
                                
                    elif x!='' and x.name=='div' and 'nav-buttons' in x.get('class'):                
                        a = x.find('a',rel='nofollow next')
                        if a:
                            url=a.get('href')
                            self.RedditLinks(url)
                        else:
                            print 'finished..'
            else:
                print 'something went wrong.Try again.'

    def album2Image(self,url):
    # this function checks the url provided
    # whether or not if it is a album or not
    # in any case it parses and create a folder
    # if it is a link or else it directly downloades
    # the file
    # al_no: is the album number 

        urlsplit = url.split('/')
        if 'm.imgur.com' in urlsplit:
            x=urlsplit
            x[x.index('m.imgur.com')]='imgur.com'

        self.al_no=self.al_no+1

        #print 'urlsplit %s, al_no %d'%(urlsplit,self.al_no)
       
        retrace=path=self.filepath+r'\%s'%self.user
        # D:\Photos\Reddit-users\user
        if not os.path.exists(path):
            os.makedirs(path)

        if 'i.imgur.com' in urlsplit:
            #D:\Photos\Reddit-users\user\
            self.downloadImage(url,self.al_no,path)
            
        elif 'imgur.com' in urlsplit and 'a' in urlsplit:
            res = self.makerequest(url)
            if res!='empty' and res.status_code==200:
                
                soup = self.makesoup(res)
                #img=soup.find_all('img',class_=lambda l:l and 'thumb' in l)
                img=soup.findAll('img')

                if len(img):
                	# here need to be album number
                	print '%d images to download'%len(img)

                	path = path + r'\%s%d'%(self.user,self.al_no)

                	print 'Haleluyeah'

                	self.al_no=self.al_no+1
                	cnt = 1
                	for x in img:
                		
                		if 'i.imgur.com' in x['src']:

                			# here call the download image
                			# function
                			url = 'https://'+x['src']
                			self.downloadImage(url,cnt,path)
                			cnt=cnt+1


             
        elif 'imgur.com' in urlsplit:
            ## this is single picture
            print 'this is sigle picture'
            res = self.makerequest(url)
            if res!='empty' and res.status_code==200:

            	soup = self.makesoup(res)
                #img=soup.find_all('img',class_=lambda l:l and 'thumb' in l)
                img=soup.findAll('img')

                for x in img:                	
                	
                	if 'i.imgur.com' in x['src']:                	

                		# here call the download image
                		# function
                		url = 'https://'+x['src']
                		self.downloadImage(url,self.al_no,path)
                		break

                self.al_no=self.al_no+1

        
        elif 'vidble.com' in urlsplit and\
             'album' in urlsplit:
            
            print 'in viddle album'
            res = self.makerequest(url)
            if res!='empty' and res.status_code==200:
                
                path = path + r'\%s%d'%(self.user,self.al_no)
                #D:\Photos\Reddit-users\user\user(1)
                if not os.path.exists(path):        
                    os.makedirs(path)                            

                soup = self.makesoup(res)
                img=soup.find_all('img')
                if not img:
                    print 'something went wrong.Try again.'
                    return
                img=[x for x in img if 'title' not in x.attrs and 'src' in x.attrs]
                print "%d images to download....."%len(img)

                pic_no=1
                if img:
                    
                    for x in img:
                        # y has '/fZAFlXSHPI.jpg
                        y = x.get('src')
                        url='https://vidble.com'+y

                        print url
                        #D:\Photos\Reddit-users\user\user(1)
                        self.downloadImage(url,pic_no,path)
                        print '%d done..'%pic_no
                        pic_no=pic_no+1
                else:
                    print 'something went wrong.Try again. Make sure required cookies are enabled'

        elif 'vidble.com' in urlsplit:
            print 'in viddle image'
            #D:\Photos\Reddit-users\user\user(1)
            self.downloadImage(url,self.al_no,path)
                
        else:
            self.al_no=self.al_no-1
            print 'non-supported domain'        
            
        return self.al_no

if __name__=='__main__':
    
    user = 'sl_delight'
    #user = 'AliceAardvark'
    #user='pichuntersexbomb'
    #url = 'https://www.reddit.com/user/'+user+'/submitted/'
    #RedditLinks(url,user,0)#
#album2Image(url,user,78)
else:
    print 'import successfull'
