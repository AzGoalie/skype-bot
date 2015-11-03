import config
import time
import random
import operator
import itertools
import time
import os

players = dict()    # Players dictionary, PLAYER_NAME : SCORE
questionAsked = False

question = ''
answer = ''
mask = ''
leaderboard = 'Trivia Scores.txt'

def updateScoreFile():
    # load the leaderboards into a dictionary
    tmp = dict()
    f = open(leaderboard, 'r')
    for line in f:
	split = line.split(': ')
	name = split[0]
	score = split[1]
	tmp[name] = int(score)
    f.close()

    # add the current scores to the leaderboards
    for player in players:
	tmp.setdefault(name, 0)
	tmp[player] += int(players[player])

    f = open(leaderboard, 'w')
    sort = sorted( ((v,k) for k,v in tmp.iteritems()), reverse=True)
    scores = ''
    for s,p in sort:
    	scores += p + ': ' + str(s) + '\n'
    f.write(scores)
    f.close()

def triviaStart(Message):
    global questionAsked
    questionAsked = False
    if config.trivia:
	config.trivia = False
	Message.Chat.SendMessage('Trivia ended')
	printScore(Message)
	printLeaderboard(Message)
	players.clear()
    else:
	config.trivia = True
	Message.Chat.SendMessage('Welcome to the SkypeBot Trivia Game!')
	Message.Chat.SendMessage('To answer the questions, prefix your answers with a \'!\'\n!next for skiping questions')
	time.sleep(2)
	triviaLoop(Message)

def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
      if random.randrange(num + 2): continue
      line = aline
    return line

def getQuestion():
    global question
    global answer
    global mask

    bad = True
    mask = ''
    while bad:
    	fileName = 'trivia_questions/' + random.choice(os.listdir('trivia_questions/'))
    	print 'Getting question from file: ' + fileName
    	f = open(fileName, 'r')
    	line = random_line(f)
    	question = line.lower().rstrip().split('`')[0]
	
	try:    	
	    answer = line.lower().rstrip().split('`')[1]
	except:
	    print 'Broken Question!!!'
	    print question
	    continue
    	
	bad = False
	for i in answer:
	    if i.isalnum():
	    	mask += '*'
	    else:
	    	mask += i
    	print 'Question: ' + question
    	print 'Answer: ' + answer

def printScore(Message):
    sort = sorted( ((v,k) for k,v in players.iteritems()), reverse=True)
    scores = 'Current score:\n'
    for s,p in sort:
        scores += p + ': ' + str(s) + '\n'
    Message.Chat.SendMessage(scores)

def printLeaderboard(Message):
    f = open(leaderboard, 'r')
    leaders = ''
    count = 0
    for line in f:
	leaders += line
	count += 1
	if count > 5:
	    break;
    Message.Chat.SendMessage('Trivia Leaderboard (Top 5):\n' + leaders)

def checkAnswer(currentAnswer):
    if currentAnswer == answer:
	return True
    else:
	return False

def giveHint(Message):
    global mask
    global questionAsked
    if mask == answer:
	Message.Chat.SendMessage('No one got the answer: ' + answer)
	questionAsked = False
	mask = ''		
	triviaLoop(Message)
    else:
	Message.Chat.SendMessage('Hint: ' + mask)
	letter = ' '
	while not letter.isalnum():
	    index = random.randint(0, len(answer)-1)
	    letter = answer[index]
	    if mask[index] == letter:
		letter = ' '
	tmp = list(mask)
	tmp[index] = letter
	mask = ''.join(tmp)

def triviaLoop(Message, skip = False):
    global questionAsked
    global question
    global answer
    global mask
    global players

    currentAnswer = Message.Body.replace('!', '').lower()
    currentPlayer = Message.FromDisplayName

    if (currentAnswer == 'next' and not skip):
	questionAsked = False
	triviaLoop(Message, True)

    if questionAsked:
	# Handle answers
	if (checkAnswer(currentAnswer)):
	    Message.Chat.SendMessage(currentPlayer + ' is correct!\nAnswer: ' + currentAnswer)
	    if currentPlayer not in players:
		players[currentPlayer] = 0		
	    players[currentPlayer] += 1
	    printScore(Message)
	    updateScoreFile()
	    questionAsked = False;
	    time.sleep(2)
	    triviaLoop(Message)
	else:
	    # Give hint
	    if currentAnswer != 'next':    
		giveHint(Message)
    else:
	# Find and ask a question
	getQuestion()
	Message.Chat.SendMessage(question)
	giveHint(Message)	
	questionAsked = True
