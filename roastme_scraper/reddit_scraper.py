import praw

user_agent = ('RedScrape 0.1')

reddit = praw.Reddit(user_agent=user_agent)

subreddit = reddit.get_subreddit('RoastMe')

iteration = 1

for submission in subreddit.get_top(limit=10):
	# print 'Title:', submission.title
	# print "Text: ", submission.selftext
	# print "Score: ", submission.score
	file = open('roasts_' + str(iteration), 'a')
	keys = submission.title
	key_str = keys + '\n-'*100

	try:
		file.write(key_str)
	except:
		print key_str

	try:
		submission.replace_more_comments(limit=10, threshold=0)
	except:
		continue

	comment_number = 1

	for comment in submission.comments:
		try:
			comment_str = '\t' + str(comment_number) + ') ' + comment.body + '\n\n'
			file.write(comment_str)
		except:
			pass

		comment_number += 1

	iteration += 1
	file.close()
