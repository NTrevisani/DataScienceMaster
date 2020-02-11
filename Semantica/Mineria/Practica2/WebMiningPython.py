import re
from dateutil.parser import parse
from bs4 import BeautifulSoup
from urllib import request
from datetime import datetime
import time



###currentdate=time.strftime('%Y-%m-%d')
currentdate='2018-01-01'



############# To be modified #############                                                                  
TOPIC = "[Cc]onference|[Rr]oadshow|[Ii]nvestor"#[ *][Dd]ay[(*s*)*]"                                         
pagename="Straumann"
ID="1199"
address="https://www.straumann.com/group/en/home/investors/news-an-events/investor-calendar.html"
##########################################

def altnames(mydict):
    aux_mydict = mydict.copy()
    for elem in mydict.keys():
        if "/" in elem:
            for alt in elem.split("/"):
                aux_mydict[alt] = mydict[elem]
            del aux_mydict[elem]
    return aux_mydict   

def findrows(soup_browser):
    """This method receives as parameter a BeautifulSoup object and
    returns a list of strings, one for each event to be processed"""
    rows = []
    try:
    ############# To be modified #############
        # This was the original, example code
        # rows=["13/14 November 2018$UBS Conference - London$UBS"]
        
        # Get all the lines from the web page
        all_lines = soup_browser.find_all("table")[0].find_all("td", {"class": "search-result-entry"})
        #print(all_lines)
        
        # Get the text from the lines
        text_lines = ["$".join([e.strip() for e in lines.recursiveChildGenerator() if isinstance(e,str) and len(e.strip())]) for lines in all_lines]
        #print(text_lines)
        
        # The sponsor is embedded in the event title
        # Let's see if there is a match between the list of sponsors in the dictionary
        for line in text_lines:
            if line != "":
                for sponsor in psponsors.keys():
                    if sponsor in line:
                        # Now add the sponsor value
                        sponsor_line = "$".join((line, sponsor)).strip()
                        break
                    else:
                        # If no sponsor found, add an empty line
                        sponsor_line = "$".join((line, '')).strip()
                # Append to the list of lines
                rows.append(sponsor_line)
                   
    ##########################################

    except e:
        print(e, "Could not process webpage")
    return rows


def output(m,spondict,citydict):
    ############# To be modified #############
    # This was the original, example code
    #ti,d,c,s="UBS Conference","2018-11-13/14","London","UBS"

    try:
        # Start by defining groups 
        # group 1: title
        title = m.group(1)
        #print("title", title)
            
        # group 2: date
        date = m.group(2)
        date = date.replace(".","")
        date = datetime.strptime(date, "%d %b %Y")
        date = date.strftime('%Y-%m-%d')
        #print("date:", date)        
        
        # group 3: city
        city = m.group(3)
        # transform the city into a code
        if city in pcities.keys():
            city = pcities.get(city,city)
        else:
            city = "Not available"
            
        #print("city:", city)        
        
        # group 4: country
        country = m.group(4)
        #print("country:", country)        
        
        # group 5: sponsor
        sponsor = m.group(5)
        if sponsor == "":
            sponsor = "Not available"
        ###print("SPONSOR:", sponsor)        
        
        ##solucion problema (cojo los parametros en una lista)
        val=m.group(1).split('$')

        ##tomo valores de fecha
        fech=val[-1]

        ##valores de conferencia
        conf=val[0:len(val)-1]
        conf=' '.join(conf)        

        ##defino todos los valores
        ti,d,c,s=title,date,city,sponsor

        ###########################################
        return ti.strip(), d, c.strip(), s.strip()    
    except e:
        return e,0,currentdate,0,0

    
def processhtml(pageID,pageAddress,pcities,psponsors):
    """This method reads in the webpage with id pageID and url pageAddress
    and prints out the requested information for each of the relevant events found"""
    ############# To be modified #############
    url=request.urlopen(pageAddress,timeout=None).read()
    soup = BeautifulSoup(url,"lxml")
    #print(soup)
    r="(.*)\$(.*)\$(.*)\$(.*)\$(.*)"   
    for line in findrows(soup):
        m1=re.search(TOPIC,line)
        if m1:
            # Type of event: 1 = Roadshow; 2 = Conference; 3 = Investor
            t = 0 # this must be changed accordingly
            print("M1 =", m1.group(0))
            pattern_road = re.compile("[Rr]oadshow")
            pattern_conf = re.compile("[Cc]onference")
            pattern_inve = re.compile("[Ii]nvestor")
            if pattern_road.match(m1.group(0)):
            #if m1.group(0) == "Roadshow":
                t = 1
            elif pattern_conf.match(m1.group(0)):
            #elif m1.group(0) == "Conference":
                t = 2
            elif pattern_inve.match(m1.group(0)):
                #elif m1.group(0) == "Investor":
                t = 3
            else:
                t = "Not available"
            m2=re.search(r,line)
            if m2:
                ti,d,c,s=output(m2,psponsors,pcities)
                if d[:10]>currentdate:
                    c=pcities.get(c,c)
                    s=psponsors.get(s,s)
                    newrecord="Company: %s\nType: %s\nDate: %s\nTitle: %s\nCity: %s\nSponsor: %s\n"%(pageID,t,d,ti,c,s)
                    print(newrecord)
    ##########################################                    
    
                            

if __name__ == "__main__":
    ## Read cities list from file    
    cities=dict([line.strip().split(";") for line in open("city.csv", encoding='ISO-8859-1').readlines()[1:]])
    pcities = dict(zip([x for x in cities.values()],cities.keys()))
    pcities=altnames(pcities)
    ## Read sponsors list from file     
    sponsors=dict([line.strip().split(";") for line in open("sponsor.csv").readlines()[1:]])
    psponsors = dict(zip(sponsors.values(),sponsors.keys()))
    psponsors = altnames(psponsors)  

    print("Extract information from %s webpage"%pagename)
    processhtml(ID,address,pcities,psponsors)

                






