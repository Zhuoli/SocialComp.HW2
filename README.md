Given a social network, predict the next few links that will be established

To run this program:
> ./5750linkpred <graph file> <# of edges to predict>

High level approach:

  First approach, we cutted the input graph into communities using networkx lib, and then make prediction in each communities inoredr to improve performance.Then we tried to implement several different prediction algorithms as voters, and use the training data to weight each voter. But since our code runs very slow (over minutes to finish one test example), and among the running time, the dividing to communities action cost half of time, so we give up communities approach and try to optimize our code in someother way.
  It's untill this time we found that the important thing is how to runs out the result in the limited time.

BIG BIG CHALLANGE: 
	Performance: I spent 4 days to improve performance, tried multithreading then find that multithreading in Python is merely a joke, then treid multiprocessing, somehow the communication between processings cost a lot and often cause processing going in sleeping state. Finally, with prof.'s advising, I turned my attention on optimize the code, aftering remove all the redundancy code, a miracle happens: a test data can be runned in seconds.
	Accuracy: When the performance issue done, it is nolonger a trade-off isue with accuracy and performance, I have large enough runnting time left to improve accuracy. But it is really NOT easy to improve accuracy. I tried tree algorithm about prediction: Preferential attachment, Common neighbors,Adamic/Adar. The worst prediction is preferential attachment, using which all the test score is zero. The best prediction till now is Adamic/Adar, which make a 1 percetange accuracy 

GOOD properties:
	 The best desigin I made is getting out all the networkx library. At first, I used Graph clas in Networkx to represent grap, but the initialization and calling of graph class methods cost huge amount of timei. Realized that what I need is just a out_degree_hashtable a in_degree_hashtable and a list of nodes, I tried to remove the graph class and build my own hashtable, to my surprise, the result of these changes lead to an outstanding performance which repalce the time cost from minutes to seconds. 
BAD approach:
	I wasted 4 days on trying to implement my code to multiprocessing. What I learned from this failed approach is: first, I mastered the skills to write multiprocessing code in Python. second, the performance of the algorithm its self is more important. Third, multithreading in Python is really a bad idea, since a so called GIL issue, all the threadings will only run on a single core alternately.

Conclusion:
	1: Jaccard's coefficient method can better predict model2-x test data
	2: It is NOT easy to make prediction
