from trainSet_util import TrainingSet_util

dataset = {}
dataset['training'] = '../dataset/training.txt'
 
util = TrainingSet_util(dataset)

usersetfile = 'user.dat'

util.filterUsers(usersetfile, 'user.filter')
