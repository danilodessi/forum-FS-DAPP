# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import time
from libcontractvm import Wallet, ConsensusManager, DappManager
from datetime import date

class ForumManager (DappManager.DappManager):
	def __init__ (self, consensusManager, wallet = None):
		super (ForumManager, self).__init__(consensusManager, wallet)

	# This method is used to create a new post
	def createPost (self, title, body):
		print(' CREATE POST: ', title, body)
		# Retrieve the address of the user
		who = self.wallet.getAddress()
		# Start the transaction		
		cid = self.produceTransaction('forum.createPost', [title, body, who])
		return cid

	# This method is used to create a comment for a post
	def commentPost (self, id_post, comment):
		print(' CREATE COMMENT: ', id_post, comment)
		who = self.wallet.getAddress()
		cid = self.produceTransaction('forum.commentPost', [id_post, comment, who])
		return cid

	# this methhod shows the list of posts in the database without comments
	def listPost (self):
		posts = self.consensusManager.jsonConsensusCall('forum.listPost',[])['result']
		
		count = 0
		lista = "List of the posts...\n"
		for id_post in posts:
			post = self.consensusManager.jsonConsensusCall('forum.getPost',[id_post])['result']
			lista = lista + "Post " + str(count) +"\n"
			count = count + 1
			lista = lista + "Owner:  " + post['owner'] + "\n"
			lista = lista + "Title:  " + post['title'] + "\n"
			lista = lista + "Body:  " + post['body'] + "\n\n"
		print(lista)
			
	# This method shows a single post with comment
	def getPostInfo(self, id_post):
		posts = self.consensusManager.jsonConsensusCall('forum.listPost',[])['result']
		if id_post in posts:
			post = self.consensusManager.jsonConsensusCall('forum.getPost',[id_post])['result']
			info = 'POST(' + id_post + ')\n' + 'Title: '+ post['title'] + '\nBody: '+ post['body'] + '\nComments:\n'
			countComment = 1				
			for y in post['comments']:
				info = info + str(countComment) + " Owner: " + y['owner'] + " Text: " + y['commentValue']+"\n"
				countComment = countComment + 1
			
		else:
			info = 'Invalid argument: The post (' + id_post + ') not exists'

		print(info)

	# This method can be used to modify the title and the body of a post 
	def editPost(self,id_post, new_title, new_body):
		print(' EDIT POST post: ', id_post, new_title, new_body)
		who = self.wallet.getAddress()
		return self.produceTransaction('forum.editPost', [id_post, new_title, new_body, who])

	# This method is used to delete a post that is stored 	
	def deletePost(self,id_post):
		print(' DELETE POST id_post: ', id_post)
		who = self.wallet.getAddress()
		return self.produceTransaction('forum.deletePost', [id_post, who])

	# This method is used to edit a comment 
	def editComment(self,id_comment, new_comment):
		print(' EDIT COMMENT comment: ', id_comment, new_comment)
		who = self.wallet.getAddress()
		return self.produceTransaction('forum.editComment', [id_comment, new_comment, who])

	# This method is used to delete a comment
	def deleteComment(self,id_comment):
		print(' DELETE COMMENT id: ', id_comment)
		who = self.wallet.getAddress()
		return self.produceTransaction('forum.deleteComment', [id_comment, who])

	# This method is used to create a poll
	def createPoll(self,title, listAnswers, deadline):
		print(' CREATE POLL title: ', title)
		who = self.wallet.getAddress()
		return self.produceTransaction('forum.createPoll', [title, listAnswers, deadline, who])

	# This method shows the list of the polls stored in database without the score 
	def listPolls(self):
		polls = self.consensusManager.jsonConsensusCall('forum.getPolls',[])['result']
		info = ''
		count = 0
		for id_poll in polls:
			poll = self.consensusManager.jsonConsensusCall('forum.getPoll',[id_poll])['result']
			info = info + "Poll " + str(count) + ": \nID: "
			count = count + 1
			info = info + id_poll + " \nTitle:  "+ poll['title'] + "\nAnswer \n[ "
			for y in poll['listAnswersScore']:
				info = info + " - " + y['answer']
			info = info + " ]" + " \ndeadline: " +  poll['deadline']

			today = date.today()
			todayStr = str(today)
			if todayStr > poll['deadline']:
				info = info + " - close"
			else:
				info = info + " - open"

			info = info +"\n\n"
		print(info)
	
	# This method is used to vote a post
	def vote(self, id_poll, choice):
		print(' VOTE POLL poll:', id_poll, choice)
		who = self.wallet.getAddress()
		return self.produceTransaction('forum.votePoll', [id_poll, choice, who])

	# this method is used to retrieve the information of a poll with the score for all choices
	def getPollInfo(self, id_poll):
		info = ''
		polls = self.consensusManager.jsonConsensusCall('forum.getPolls',[])['result']
		if id_poll in polls:
			poll = self.consensusManager.jsonConsensusCall('forum.getPoll',[id_poll])['result']
			info = ''		
			info = info + "Poll "+ "\nID: " + id_poll
			info = info + " \nTitle:  "+ poll['title'] + "\nAnswers \n"
			for y in poll['listAnswersScore']:
				info = info + " - " + y['answer'] + " score: " + str(len(y['votes'])) +" [ "
				for vote in y['votes']:
					info = info + vote +"  "
				info = info + "]\n"
			info = info + "]\ndeadline: " +  poll['deadline']

			today = date.today()
			todayStr = str(today)
	
			if todayStr > poll['deadline']:
				info = info + " - close"
			else:
				info = info + " - open"

		print(info)

	# this method is used to delete a poll
	def deletePoll(self,id_poll):
		print(' DELETE POLL poll: ', id_poll)
		who = self.wallet.getAddress()
		return self.produceTransaction('forum.deletePoll', [id_poll, who])

	# This method is used to retrieve all information in the forum of the user
	def getUserInfo(self):
		print("GET USER INFO\n")
		who = self.wallet.getAddress()
		info = "USER: " + who + "\n"
		info = info + "Posts:\n"
		nPost = 0
		posts = self.consensusManager.jsonConsensusCall('forum.listPost',[])['result']
		for id_post in posts:
			info = info + "POST " + str(nPost) + ": "
			post = self.consensusManager.jsonConsensusCall('forum.getPost',[id_post])['result']
			info = info + id_post + " " + post['title'] + " " + post['body'] + "\n"
			nPost = nPost + 1

		info = info + "COMMENTS:\n"
		for id_post in posts:
			
			comment = ''
			if post['owner'] == who:
				info = info + "id post: " + id_post + "\n [ "
				for y in post['comments']:
					comment = comment + y['commentValue'] + " "
				
				info = info + comment + " ]\n"
		
		
		info = info + "\n\nPolls:\n"
		polls = self.consensusManager.jsonConsensusCall('forum.getPolls',[])['result']
		for id_poll in polls:
			poll = self.consensusManager.jsonConsensusCall('forum.getPoll',[id_poll])['result']
			if poll['owner'] == who:
				info = info + id_poll+ poll['title']+ "\n"

		print(info)


			
		
		
		
		
		
		
		