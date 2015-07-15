import webbrowser
import csv
import requests

def wiki(word1, word2='', word3='', word4='', state=' '):
	if word2 <> '' and word3 <> '' and word4 <> '':
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s+%s+%s+%s' % (word1, word2, word3, word4)
	elif word2<> '' and word3 <> '':
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s+%s+%s' % (word1, word2, word3)	
	elif word2 <> '':
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s+%s' % (word1, word2)
	else:
		addr = 'https://en.wikipedia.org/w/index.php?title=Special:Search&search=%s' % (word1)
	search = requests.get(addr)
	url = search.url
	if state in search.text:
		return url
	else:
		print 'No Match for %s' % (word1 + ' ' + word2 + ' ' + word3 + ' ' + word4)

def wordsplit(names):

	names = names.lower()
	names = names.replace(' & ', ' and ')

	if ' ' in names:
		space1 = names.find(' ')
		first = names[0:space1]
		names = names[space1+1:]
		if ' ' in names:
			space2 = names.find(' ')
			second = names[0:space2]
			names = names[space2+1:]
			if ' ' in names:
				space3 = names.find(' ')
				third = names[0:space3]
				fourth = names[space3+1:]
			else:
				third = names
				fourth = ''
		else:
			second = names
			third = ''
			fourth = ''
	else:
		first = names
		second = ''
		third = ''
		fourth = ''

	print first		
	print second
	print third
	print fourth
	
	return first, second, third, fourth

crpdict = {
	' Assoc':' Associates',
	' Corp':' Corporation',
	' Assn':' Association',
	' Inc':' ',
	' Corp':' '
	}

file = open('orgs.csv', 'rU')
readfile = csv.reader(file)
data = list(readfile)

file2 = open('abbrevs.csv')
readfile2 = csv.reader(file2)
states = list(readfile2)

statedict = {}

for row in states:
	statedict[row[2]] = row[1]

item = 0

while item < len(data) and int(data[item][1]) > 9999:

	place = item
	
	if len(data[item][0]) < 6:
		item = item + 1
#	elif int(data[item][1]) > 14999:
#		item = item + 1	
	else:
		orgname = data[item][0]
		print orgname
		first, second, third, fourth = wordsplit(orgname)
		
		state = statedict[data[item][2]]
		url = wiki(first, second, third, fourth, state)
		
		try:
			if 'index' not in url and 'disambiguation' not in url:
				webbrowser.open(url)
				item = place + 1
			
		except:
			while item == place:
				for i in crpdict.keys():	
					if i in orgname and len(orgname.replace(i, crpdict[i])) > 5:
						orgname2 = orgname.replace(i, crpdict[i])
						first, second, third, fourth = wordsplit(orgname2)
						url2 = wiki(first, second, third, fourth, state)
						try:
							if 'index' not in url2 and 'disambiguation' not in url2:
								webbrowser.open(url2)
								item = place + 1
						except:
							print ''
				item = place + 1

		item = place + 1
		
	

