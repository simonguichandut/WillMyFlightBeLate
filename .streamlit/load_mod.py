
import pickle

def load_mod():
	model = pickle.load(open('../models/RF_2022_2023.pickle','rb'))
	return model
