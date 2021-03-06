import docclass

classifier = docclass.Classifier(['Tech','NonTech'])

import feedparser


def stripHTML(h):
  p=''
  s=0
  for c in h:
    if c=='<': s=1
    elif c=='>':
      s=0
      p+=' '
    elif s==0:
      p+=c
  return p


trainTech=['http://rss.chip.de/c/573/f/7439/index.rss',
           'http://feeds.feedburner.com/netzwelt',
           'http://rss1.t-online.de/c/11/53/06/84/11530684.xml',
           'http://www.computerbild.de/rssfeed_2261.xml?node=13',
           'http://www.heise.de/newsticker/heise-top-atom.xml']

trainNonTech=['http://newsfeed.zeit.de/index',
              'http://newsfeed.zeit.de/wirtschaft/index',
              'http://www.welt.de/politik/?service=Rss',
              'http://www.spiegel.de/schlagzeilen/tops/index.rss',
              'http://www.sueddeutsche.de/app/service/rss/alles/rss.xml'
              ]
test=["http://rss.golem.de/rss.php?r=sw&feed=RSS0.91",
          'http://newsfeed.zeit.de/politik/index',
          'http://www.welt.de/?service=Rss'
           ]




for feed in trainTech:
    f=feedparser.parse(feed)
    for e in f.entries:
        fulltext=stripHTML(e.title+' '+e.description)
        classifier.train(fulltext,'Tech')

for feed in trainNonTech:
    f=feedparser.parse(feed)
    for e in f.entries:
        fulltext=stripHTML(e.title+' '+e.description)
        classifier.train(fulltext,'NonTech')

for feed in test:
    f=feedparser.parse(feed)
    for e in f.entries:
        fulltext=stripHTML(e.title+' '+e.description)
        print classifier.classify(fulltext)