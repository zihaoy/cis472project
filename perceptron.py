import sys
import re
from math import log
from math import exp
#Some code use the homework code provided by Daniel Lowd <lowd@cs.uoregon.edu>
MAX_ITERS = 100

# Load data from a file
def read_data(filename):
  f = open(filename, 'r')
  p = re.compile(',')
  data = []
  header = f.readline().strip()
  varnames = p.split(header)
  namehash = {}
  for k in f.readlines():
    temp = []
    if filename == "test.csv":
	  temp += ["test"]+k.strip().split(",")
    elif filename == "gender_submission.csv":
	  temp += k.strip().split(",") + ["1"]*8
    else:
      temp += k.strip().split(",")
    #not include Name and Passenger ID (useless)
    #add Pclass in array
    array = [temp[2]]
    #append sex as male = 0, female = 1
    if temp[-8] == "male":
      array.append(1)
    else:
      array.append(2)
    #add age, sibsp and parch in array
    l = temp[-7]
    #if l != "":
    #  array.append(abs(float(l)-18))  
    #else:
	#  array.append(l)
    array.append(l)
    array.append(temp[-6])
    array.append(temp[-5])
    #not include ticket number(useless)
    #add Fare
    array.append(temp[-3])
    #not include cabin since a lot of passenger not have. 
    #add Embarked as S = 0, C = 1, Q = 2
    if temp[-1] == "S":
      array.append(0)
    elif temp[-1] == "C":
      array.append(1)
    else:
      array.append(2)
    if temp[1] == "0":
	  data.append((array,-1))
    else:
	  data.append((array,1))
  #for l in f:
  #  example = [int(x) for x in p.split(l.strip())]
  #  x = example[0:-1]
  #  y = example[-1]
    # Each example is a tuple containing both x (vector) and y (int)
  #  data.append( (x,y) )
  return (data, varnames)


# Learn weights using the perceptron algorithm
def train_perceptron(data):
  max = 0;
  # Initialize weight vector and bias
  numvars = len(data[0][0])
  w = [0.0] * numvars
  b = 0.0
  #
  # YOUR CODE HERE!
  #
  passes = MAX_ITERS
  for i in xrange(0,passes):
    for (x,y) in data:
      a = b
      for j in xrange(0,numvars):
        if x[j] != "":
		  a += w[j] * float(x[j])
      if y * a <= 0:
        for k in xrange(0,numvars):
          if x[k] != "":
            w[k] = w[k]+y*float(x[k])
        b = b + y
    if (allcorr(data,(w,b))>= len(data)):
	   break
  return (w,b)


def allcorr(test,model):
  correct = 0
  for (x,y) in test:
    activation = predict_perceptron( model, x )
    if activation * y > 0:
      correct += 1 
  return correct
  
# Compute the activation for input x.
# (NOTE: This should be a real-valued number, not simply +1/-1.)
def predict_perceptron(model, x):
  (w,b) = model

  #
  # YOUR CODE HERE!
  #
  a = b
  for i in xrange(len(x)):
    if x[i] != "":
      a += w[i]*float(x[i]) 
  return a


# Load train and test data.  Learn model.  Report accuracy.
def main(argv):
  # Process command line arguments.
  # (You shouldn't need to change this.)
  if (len(argv) != 3):
    print('Usage: perceptron.py <train> <test> <gender_sub>')
    sys.exit(2)
  (train, varnames) = read_data(argv[0])
  (test, testvarnames) = read_data(argv[1])
  (gen, genvarnames) = read_data(argv[2])
  model = train_perceptron(train)
  print allcorr(train,model)/float(len(train))
  correct = 0
  for i in xrange(len(test)):
    x = test[i][0]
    y = gen[i][1]
    activation = predict_perceptron( model, x )
    if activation * y > 0:
      correct += 1
  print correct/float(len(test))
  print model
  
if __name__ == "__main__":
  main(sys.argv[1:])
