# Copyright (c) 2015 Davide Gessa
# Distributed under the MIT software license, see the accompanying
# file COPYING or http://www.opensource.org/licenses/mit-license.php.

import logging
import time


from datetime import date
from contractvmd import config, dapp, proto
from contractvmd.chain import message

logger = logging.getLogger(config.APP_NAME)

class ForumProto:
	DAPP_CODE = [ 0x29, 0x01 ]
	METHOD_LIST_POST = 0x01
	METHOD_CREATE_POST = 0x02
	METHOD_COMMENT_POST = 0x03
	METHOD_GET_COMMENTS = 0x04
	METHOD_CREATE_POLL = 0x05
	METHOD_VOTE_POLL = 0x06
	METHOD_EDIT_POST = 0x07
	METHOD_DELETE_POST = 0x08
	METHOD_EDIT_COMMENT = 0x09
	METHOD_DELETE_COMMENT = 0x10
	METHOD_DELETE_POLL = 0x11
	METHOD_LIST = [METHOD_LIST_POST, METHOD_CREATE_POST, METHOD_COMMENT_POST, METHOD_GET_COMMENTS, METHOD_CREATE_POLL,METHOD_VOTE_POLL, METHOD_EDIT_POST, METHOD_DELETE_POST, METHOD_EDIT_COMMENT, METHOD_DELETE_COMMENT,METHOD_DELETE_POLL]


class ForumMessage (message.Message):

	# the message to create a post has the title, the body and who that rappresents the owner
	def createPost (title, body, who):
		m = ForumMessage ()
		m.Title = title
		m.Body = body
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_CREATE_POST
		return m
	
	# the message to comment a post has the id of the post, the text and who that rappresents the owner of the comment
	def commentPost (id_post, comment, who):
		m = ForumMessage ()
		m.Id_post = id_post
		m.Comment = comment
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_COMMENT_POST
		return m

	# the message to edit a post has the id , the new title, the new body and who want to edit the post
	def editPost(id_post, new_title, new_body, who):
		m = ForumMessage()
		m.Id_post = id_post
		m.New_title = new_title
		m.New_body = new_body
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_EDIT_POST
		return m

	# the message to delete a post has the id of the post and who want to delete the post
	def deletePost(id_post, who):
		m = ForumMessage()
		m.Id_post = id_post
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELETE_POST
		return m

	# the message to edit a comment has the id of the comment, the new comment and who want edit the comment
	def editComment(id_comment, new_comment, who):
		m = ForumMessage()
		m.Id_comment = id_comment
		m.New_comment = new_comment
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_EDIT_COMMENT
		return m

	# the message to delete a comment has the id of the comment and who want to delete the comment
	def deleteComment(id_comment, who):
		m = ForumMessage()
		m.Id_comment = id_comment
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELETE_COMMENT
		return m

	# the message to create a poll has the title of the poll, the list of the answers, a deadline and who that rappresents the owner
	def createPoll(title, listAnswers, deadline, who):
		m = ForumMessage()
		m.Title = title
		m.ListAnswers = listAnswers
		m.Deadline = deadline
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_CREATE_POLL
		return m

	# the message to vote a poll has the id of the poll, the choice and who has voted
	def votePoll(id_poll, choice, who):
		m = ForumMessage()
		m.Id_poll = id_poll
		m.Who = who
		m.Choice = choice
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_VOTE_POLL
		return m

	# the message to delete a comment has the id of the comment and who want delete poll
	def deletePoll(id_poll, who):
		m = ForumMessage()
		m.Id_poll = id_poll
		m.Who = who
		m.DappCode = ForumProto.DAPP_CODE
		m.Method = ForumProto.METHOD_DELETE_POLL
		return m

	def toJSON (self):
		data = super (ForumMessage, self).toJSON ()

		if self.Method == ForumProto.METHOD_CREATE_POST:
			data['title'] = self.Title
			data['body'] = self.Body
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_COMMENT_POST:
			data['id_post'] = self.Id_post
			data['comment'] = self.Comment
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_CREATE_POLL:
			data['title'] = self.Title
			data['listAnswers'] = self.ListAnswers
			data['deadline'] = self.Deadline
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_VOTE_POLL:
			data['id_poll'] = self.Id_poll
			data['choice'] = self.Choice
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_EDIT_POST:
			data['id_post'] = self.Id_post
			data['new_title'] = self.New_title
			data['new_body'] = self.New_body
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_DELETE_POST:
			data['id_post'] = self.Id_post
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_EDIT_COMMENT:
			data['id_comment'] = self.Id_comment
			data['new_comment'] = self.New_comment
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_DELETE_COMMENT:
			data['id_comment'] = self.Id_comment
			data['who'] = self.Who

		elif self.Method == ForumProto.METHOD_DELETE_POLL:
			data['id_poll'] = self.Id_poll
			data['who'] = self.Who
		
		else:
			return None
			
		return data


class ForumCore (dapp.Core):
	def __init__ (self, chain, database):
		database.init ('posts', [])
		database.init ('polls', [])
		super (ForumCore, self).__init__ (chain, database)


	# it is used to create a new post in database
	def createPost (self, id_post, title, body, owner):
		# initialization of the row to store a new post		
		self.database.init(id_post, None)
		
		# create the post with its features and save it
		value = {'title':title, 'body':body, 'owner':owner, 'comments':[]}
		self.database.set(id_post, value)
		
		# all ids are stored into a list
		self.database.listappend ('posts', id_post)


	# it is used to create a new comment for a post
	def commentPost (self, id_post, id_comment, commentValue, who):	
		posts = self.database.get('posts')
		# check if the post exists
		if id_post in posts:
			# create the comment with its features and save it in the attributes comments of the post
			value = {'owner':who, 'commentid':id_comment, 'commentValue':commentValue}
			post = self.database.get(id_post)
			post['comments'].append(value)
			self.database.set(id_post, post)


	# this method is used to retrieve the list of the ids of the posts	
	def listPost (self):
		return self.database.get('posts')

	# this method is used to retrieve a post	
	def getPost(self, id_post):		
		return self.database.get(id_post)
		

 
	#this method is used to create a new poll in database
	def createPoll(self,id_poll, title, listAnswers, deadline, who):
		# In the poll the title, the list of the answers with their votes and deadline are saved.
		# In listAnswersScore, the lists of the votes for all choices are empty at the start.
		listAnswersScore = []
		for answer in listAnswers:
			listAnswersScore.append({'answer':answer, 'votes':[]})
		
		# Save poll in the database
		value = {'title':title, 'listAnswersScore':listAnswersScore, 'deadline':deadline, 'owner':who}
		self.database.init(id_poll, None)
		self.database.set(id_poll, value)
		# the ids of the polls are stored into a list
		self.database.listappend('polls',id_poll)


	# this method return the list of the ids of the polls
	def getPolls(self):
		return self.database.get('polls')


	# this method is used to retrieve a poll
	def getPoll(self, id_poll):
		return self.database.get(id_poll)


	# this method is used to stored in database the votes of the polls
	def votePoll(self, id_poll, choice, who):

		polls = self.database.get('polls')
		# check if the poll exists
		if id_poll in polls:
			listAnswersScore = []

			# Retrieve the list of the votes (for all answers) and the deadline
			poll = self.database.get(id_poll)
			listAnswersScore = poll['listAnswersScore']
			deadline = poll['deadline']
			
			# Check if who has voted
			boolAlredyVoted = False
			for x in listAnswersScore:
				for y in x['votes']:
					if y == who:
						boolAlredyVoted = True

			# Check the date
			today = date.today()
			todayStr = str(today)
			boolDate = True
			if todayStr > deadline:
					boolDate = False

			# Add the vote in the list of the votes
			if not boolAlredyVoted and boolDate:
				for x in listAnswersScore:
					if x['answer'] == choice:
						x['votes'].append(who)

			# Save new modified poll in the database
			self.database.set(id_poll, poll)


	# this ethod is used to modify the attributes of post. Only owner can do
	def editPost(self, id_post, new_title, new_body, who):
		posts = self.database.get('posts')
		# check if the post exists
		if id_post in posts:
			# retrieve post
			post = self.database.get(id_post)
			# check if who is the owner
			if post['owner'] == who:
				post['title'] = new_title
				post['body'] = new_body
			# re-save the post
			self.database.set(id_post, post)


	# this method is used to delete a post. Only owner can do
	def deletePost(self, id_post, who):
		posts = self.database.get('posts')
		# check if the post exists
		if id_post in posts:
			# retrieve the post
			post = self.database.get(id_post)
			# check if who is the owner
			postRemovePermission = False
			if post['owner'] == who:
					postRemovePermission = True
			# remove the post from database and its id from the list 'polls'
			if postRemovePermission:
				self.database.listremove('posts', id_post)
				self.database.delete(id_post)


	# this method is used to modify a comment
	def editComment(self, id_comment, new_comment, who):
		# search the comment
		posts = self.database.get('posts')
		for postid in posts:
			post = self.database.get(postid)
			for comment in post['comments']:
				# when the comments is found, the owner is checked
				if comment['owner'] == who and comment['commentid'] == id_comment:
					# update a comment with the new value	
					comment['commentValue'] = new_comment					
					self.database.set(postid,post)
	

	# this method is used to delete a comment
	def deleteComment(self, id_comment, who):
		# search the comment
		posts = self.database.get('posts')
		for postid in posts:
			post = self.database.get(postid)
			for comment in post['comments']:
				# when the comments is found, the owner is checked
				if comment['owner'] == who and comment['commentid'] == id_comment:	
					#remove comment	
					commentRemove = comment
					post['comments'].remove(commentRemove)
					self.database.set(postid, post)


	# this method is used to remove a poll from database
	def deletePoll(self, id_poll, who):
		polls = self.database.get('polls')
		# check if the poll exists
		if id_poll in polls:
			# retrieve poll
			poll = self.database.get(id_poll)
			pollRemovePermission = False
			# check if who is the owner
			if poll['owner'] == who:
				pollRemove = poll
				pollRemovePermission = True
			# remove the poll from database
			if pollRemovePermission:
				self.database.delete(id_poll)
				self.database.listremove('polls', id_poll)

	
					
				



class ForumAPI (dapp.API):
	def __init__ (self, vm, dht, api):
		self.api = api
		self.vm = vm
		self.dht = dht
		rpcmethods = {}

		rpcmethods['createPost'] = {
			"call":self.method_createPost,	
			"help":{"args":["title", "body", "who"], "return":{}}

		}

		rpcmethods["commentPost"] = {
			"call":self.method_commentPost,	
			"help": {"args":["id_post","comment", "who"], "return":{}}

		}

		rpcmethods['listPost'] = {
			"call":self.method_listPost,	
			"help": {"args":[], "return":{}}

		}

		rpcmethods['getPost'] = {
			"call":self.method_getPost,	
			"help": {"args":["id_post"], "return":{}}

		}

		rpcmethods['getComments'] = {
			"call":self.method_getComments,	
			"help": {"args":[], "return":{}}

		}

		rpcmethods['createPoll'] = {
			"call":self.method_createPoll,
			"help":{"args":['title', 'listAnswers', 'deadline', 'who'], "return":{}}
		}

		rpcmethods['getPolls'] = {
			"call":self.method_getPolls,
			"help":{"args":[], "return":{}}
		}

		rpcmethods['getPoll'] = {
			"call":self.method_getPoll,
			"help":{"args":["id_poll"], "return":{}}
		}

		rpcmethods['votePoll'] = {
			"call":self.method_votePoll,
			"help":{"args":['id_poll', 'choice', 'who'], "return":{}}
		}


		rpcmethods['editPost'] = {
			"call":self.method_editPost,
			"help":{"args":['id_post', 'new_title', 'new_body', 'who'], "return":{}}
		}
	
		rpcmethods['deletePost'] = {
			"call":self.method_deletePost,
			"help":{"args":['id_post', 'who'], "return":{}}
		}

		rpcmethods['editComment'] = {
			"call":self.method_editComment,
			"help":{"args":['id_comment', 'new_comment', 'who'], "return":{}}
		}
		
		rpcmethods['deleteComment'] = {
			"call":self.method_deleteComment,
			"help":{"args":['id_comment', 'who'], "return":{}}
		}

		rpcmethods['deletePoll'] = {
			"call":self.method_deletePoll,
			"help":{"args":['id_poll', 'who'], "return":{}}
		}

		errors = {}

		super (ForumAPI, self).__init__(vm, dht, rpcmethods, errors)

	# The follow methods are used to create the message for the blockchain transaction
	def method_createPost (self,title, body, who):
		msg = ForumMessage.createPost(title,body, who)
		return self.createTransactionResponse(msg)
			

	def method_commentPost (self,id_post,comment, who):
		msg = ForumMessage.commentPost(id_post, comment, who)
		return self.createTransactionResponse(msg)


	def method_listPost (self):
		return self.core.listPost()

	def method_getPost(self, id_post):
		return self.core.getPost(id_post)


	def method_getComments(self):
		return self.core.getComments()


	def method_createPoll(self,title,listAnswers, deadline, who):
		msg = ForumMessage.createPoll(title, listAnswers, deadline, who)
		return self.createTransactionResponse(msg)

	
	def method_getPolls(self):
		return self.core.getPolls()


	def method_getPoll(self,id_poll):
		return self.core.getPoll(id_poll)
	

	def method_votePoll(self, id_poll, choice, who):
		msg = ForumMessage.votePoll(id_poll, choice, who)
		return self.createTransactionResponse(msg)


	def method_editPost(self, id_post, new_title, new_body, who):
		msg = ForumMessage.editPost(id_post, new_title, new_body, who)
		return self.createTransactionResponse(msg)


	def method_deletePost(self, id_post, who):
		msg = ForumMessage.deletePost(id_post, who)
		return self.createTransactionResponse(msg)


	def method_editComment(self, id_comment, new_comment, who):
		msg = ForumMessage.editComment(id_comment, new_comment, who)
		return self.createTransactionResponse(msg)


	def method_deleteComment(self, id_comment,who):
		msg = ForumMessage.deleteComment(id_comment, who)
		return self.createTransactionResponse(msg)


	def method_deletePoll(self, id_poll, who):
		msg = ForumMessage.deletePoll(id_poll, who)
		return self.createTransactionResponse(msg)

	
	def method_getPollInfo(self):
		return self.core.getPollInfo()
	



class forum (dapp.Dapp):
	def __init__ (self, chain, db, dht, apimaster):
		self.core = ForumCore (chain, db)
		api = ForumAPI (self.core, dht, apimaster)		
		super (forum, self).__init__(ForumProto.DAPP_CODE, ForumProto.METHOD_LIST, chain, db, dht, api)
		

	def handleMessage (self, m):
		if m.Method == ForumProto.METHOD_CREATE_POST:
			print("handle message")
			logger.pluginfo ('Found new message %s  %s:', m.Hash, m.Data['title'])
			self.core.createPost (m.Hash, m.Data['title'], m.Data['body'], m.Data['who'])	

		if m.Method == ForumProto.METHOD_COMMENT_POST:
			print("handle message")
			logger.pluginfo ('Found new comment %s  %s:', m.Data['id_post'], m.Data['comment'])
			self.core.commentPost (m.Data['id_post'], m.Hash, m.Data['comment'], m.Data['who'])	

		if m.Method == ForumProto.METHOD_CREATE_POLL:
			print("handle message")
			logger.pluginfo ('Found new poll %s  %s:', m.Hash, m.Data['title'])
			self.core.createPoll(m.Hash, m.Data['title'], m.Data['listAnswers'], m.Data['deadline'], m.Data['who'])

		if m.Method == ForumProto.METHOD_VOTE_POLL:
			print("handle message")
			logger.pluginfo ('Found new vote %s  %s:', m.Hash, m.Data['choice'])
			self.core.votePoll(m.Data['id_poll'], m.Data['choice'], m.Data['who'])

		if m.Method == ForumProto.METHOD_EDIT_POST:
			print("handle message")
			logger.pluginfo ('Edit post %s  %s:', m.Hash, m.Data['id_post'])
			self.core.editPost(m.Data['id_post'], m.Data['new_title'], m.Data['new_body'], m.Data['who'])

		if m.Method == ForumProto.METHOD_DELETE_POST:
			print("handle message")
			logger.pluginfo ('Delete post post %s  %s:', m.Hash, m.Data['id_post'])
			self.core.deletePost(m.Data['id_post'], m.Data['who'])

		if m.Method == ForumProto.METHOD_EDIT_COMMENT:
			print("handle message")
			logger.pluginfo ('Edit comment %s  %s:', m.Hash, m.Data['id_comment'])
			self.core.editComment(m.Data['id_comment'], m.Data['new_comment'], m.Data['who'])

		if m.Method == ForumProto.METHOD_DELETE_COMMENT:
			print("handle message")
			logger.pluginfo ('Delete comment %s  %s:', m.Hash, m.Data['id_comment'])
			self.core.deleteComment(m.Data['id_comment'], m.Data['who'])

		if m.Method == ForumProto.METHOD_DELETE_POLL:
			print("handle message")
			logger.pluginfo ('Delete poll %s  %s:', m.Hash, m.Data['id_poll'])
			self.core.deletePoll(m.Data['id_poll'], m.Data['who'])
				
		
