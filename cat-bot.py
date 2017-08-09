#! python3

import time
import praw
import sqlite3

def main():
        print('Connecting to Reddit...')
        reddit = praw.Reddit(user_agent='Reply Cat. to hot posts in r/CatsStandingUp (by /u/pyropause)',
                                client_id='', 
                                client_secret='',
                                username='', 
                                password='')
        
        conn = sqlite3.connect('sql.db')
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS commentedPosts(id TEXT)')
	
        if reddit.user.me() == 'pyropause':
                subreddit = reddit.subreddit('CatsStandingUp')
                for submission in subreddit.new(limit=25):
                        c.execute('SELECT * FROM commentedPosts WHERE id = ?', [submission.id])	
                        if c.fetchone():
                                continue
				
                        if comment(submission, 'Cat.'):
                                c.execute('INSERT INTO commentedPosts VALUES(?)', [submission.id])
                                conn.commit()

                        wait(5)
			
        print('Done!')
		
def comment(submission, text):
	try:
		submission.reply(text)
		print('Replied to post id: {}'.format(submission.id))
	except:
		print('Error in submiting a reply ({})'.format(submission.id))
		return False
	
	return True
	
def wait(minutes):
	for i in range(minutes):
		print('sleeping... {0} out of {1} minutes.'.format(i + 1, minutes))
		time.sleep(60)
	
	
if __name__ == '__main__':
    main()
