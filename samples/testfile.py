
from libcontractvm import Wallet, WalletExplorer, ConsensusManager
from forum import ForumManager
import sys
import time

consMan = ConsensusManager.ConsensusManager ()
consMan.bootstrap ("http://127.0.0.1:8181")

consManB = ConsensusManager.ConsensusManager ()
consManB.bootstrap ("http://127.0.0.1:8181")

wallet = WalletExplorer.WalletExplorer (wallet_file='A.wallet')
A = ForumManager.ForumManager (consMan, wallet=wallet)

wallet = WalletExplorer.WalletExplorer (wallet_file='test.wallet')
B = ForumManager.ForumManager (consManB, wallet=wallet)



postid = A.createPost('Hello post', 'Post di test')

 
A.listPost()                                                                          
commid = A.commentPost (postid, 'This is a comment')


#commid = 'c5a6ca14cc3f53de281116d9b0eb6f720b47ee3f1ba4dfa4c30955d0b373b4bc'
A.getPostInfo(postid)
postid2 = B.createPost ('Hello post 2', 'Post di test2')
#postid2 = 'a5b12f90b9f3384bb0137aa56338e6220a92ce457b4fc0f146e3470e2dbb981b'


commid2 = B.commentPost (postid, 'This is a comment of B')


#commid2 = '5591c8af87542af9a6337713aea17a1c7b9ad85323f297e003c6b613954666f1'
A.getPostInfo (postid)


pollid = A.createPoll ('Title', ['answer1', 'answer2'], '2015-12-20')



#pollid = '280819a0dd9d4eabb0bcf677dafd981742fd354092a59a85f96d326d8f4bc922'
A.listPolls ()         

                                                                      
voteid1 = A.vote(pollid, 'answer1')


voteid2 = A.vote (pollid, 'answer2') 

B.getPollInfo (pollid)
voteid3 = B.vote (pollid, 'answer2')


A.getPollInfo (pollid)  
pollid2 = B.createPoll ('Title', ['answer1', 'answer2'], '2015-12-07')

A.listPolls ()   


A.getUserInfo ()
B.editComment (commid, 'New comment 1 message')  
time.sleep(30)     
#print('ok')              
A.editComment (commid, 'New comment 2 message')
#print('ok')
time.sleep(10) 
B.editPost (postid, 'New hello post', 'New message!') 
time.sleep(10)           
A.editPost (postid, 'New hello post A', 'New message!')

time.sleep(10)
B.listPost () 
A.deleteComment (commid)
commid3 = B.commentPost (postid, 'This is a new comment') 
time.sleep(10)


A.deleteComment (commid3)
time.sleep(10)
B.getPostInfo (postid)  
B.deletePost (postid)
time.sleep(10)
A.deletePost (postid)
A.listPost ()
time.sleep(10) 
B.deletePoll (pollid2)
time.sleep(10)
A.listPolls ()
B.getUserInfo ()
A.getUserInfo ()      

