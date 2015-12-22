
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")


wallet = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
A = ForumManager.ForumManager (consMan, wallet=wallet)

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
B = ForumManager.ForumManager (consMan, wallet=wallet)



postid = A.createPost('Hello post', 'Post di test')
consMan.waitBlock()
A.listPost()                                                                  
commid = A.commentPost (postid, 'This is a comment')
A.getPostInfo(postid)
postid2 = B.createPost ('Hello post 2', 'Post di test2')
consMan.waitBlock()
commid2 = B.commentPost (postid, 'This is a comment of B')
consMan.waitBlock()
A.getPostInfo (postid)




pollid = A.createPoll ('Title', ['answer1', 'answer2'], '2015-12-20')
consMan.waitBlock()
A.listPolls ()                                                               
voteid1 = A.vote(pollid, 'answer1')
consMan.waitBlock()
voteid2 = A.vote (pollid, 'answer2') 
consMan.waitBlock()
B .getPollInfo (pollid)
voteid3 = B.vote (pollid, 'answer2')
consMan.waitBlock()
A.getPollInfo (pollid)  
pollid2 = B.createPoll ('Title', ['answer1', 'answer2'], '2015-12-07')
consMan.waitBlock()
A.listPolls ()   

consMan.waitBlock()
A.getUserInfo()
B.editComment(commid, 'New comment 1 message')  
consMan.waitBlock()
A.editComment(commid, 'New comment 2 message')
B.editPost(postid, 'New hello post', 'New message!') 
consMan.waitBlock()
A.editPost(postid, 'New hello post A', 'New message!')
B.listPost() 
A.deleteComment (commid)
consMan.waitBlock()
commid3 = B.commentPost (postid, 'This is a new comment') 
consMan.waitBlock()
A.deleteComment (commid3)
B.getPostInfo (postid)  
B.deletePost (postid)
consMan.waitBlock()
A.deletePost (postid)
A.listPost ()
B.deletePoll (pollid2)
consMan.waitBlock()
A.listPolls ()
B.getUserInfo ()
A.getUserInfo ()      

