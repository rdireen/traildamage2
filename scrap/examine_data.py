import pickle
import json


strng = pickle.load( open( r'tddata\trail_254.p', "rb" ) )
dat = json.loads(strng)


a = 0