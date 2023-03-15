#import what we need

import tracemalloc

tracemalloc.start()

import asyncio
async def getNews(getUrl):
    import asyncio
    import pyppeteer

    from requests_html import HTMLSession, AsyncHTMLSession
    URL = getUrl
    # URL = 'https://news.google.com/topstories?hl=en-GB&gl=GB&ceid=GB:en'
    session = HTMLSession()
    session = AsyncHTMLSession()


    browser = await pyppeteer.launch({ 
        'ignoreHTTPSErrors':True, 
        'headless':True, 
        'handleSIGINT':False, 
        'handleSIGTERM':False, 
        'handleSIGHUP':False
    })
    session._browser = browser
    resp_page = await session.get(URL)
    await resp_page.html.arender(sleep=1, scrolldown=1, keep_page=True)

    #use session to get the page
    # HTMLSession.browser
    # r = session.get(URL)

    #render the html, sleep=1 to give it a second to finish before moving on. scrolldown= how many times to page down on the browser, to get more results. 5 was a good number here
    # r.html.render(sleep=1, scrolldown=1, keep_page=True)

    #find all the articles by using inspect element and create blank list
    articles = resp_page.html.find('article')
    newslist = []
    titleList =[]
    linkList =[]
    authList =[]
    timeList =[]

    #loop through each article to find the title and link. try and except as repeated articles from other sources have different h tags.
    for item in articles:
        try:
            newsitem = item.find('h4', first=True)
            title = newsitem.text
            titleList.append(title)

            gettime = item.find('time', first=True)
            time = gettime.text
            timeList.append(time)
            
            getauth = item.find('span', first=True)
            auth = getauth.text
            authList.append(auth)

            getlinks = item.find('a', first=True)
            link = getlinks.absolute_links
            for x in link:
                linkList.append(x)

            
            await asyncio.sleep(1)
        except:
            pass
        if len(titleList) is 5:
            break
    #print the length of the list

    # return(newslist)
    return(titleList, timeList, authList, linkList)


