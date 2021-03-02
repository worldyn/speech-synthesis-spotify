import json

obj = {
    'paths': ['7td2k4hXAbJsqc5Lvroyah.wav', '7td2k4hXAbJsqc5Lvroyah.wav', '7td2k4hXAbJsqc5Lvroyah.wav'],
    'timestamps': [(0.0, 5.5), (60, 75), (90, 100)]
}

with open('input_segments.json', 'w') as file:
    json.dump(obj, file, indent=4)


# Creating the intervals file
'''
intervals = {
    "f0_interval": 0.8,
    "pitch_interval": 0.5,
    "sr_interval": 0.2,
    "energy_interval": 0.5,
    "intensity_interval": 0.3
}

with open('intervals.json', 'w') as file:
    json.dump(intervals, file, indent=4)

'''

# Creating a sample input file
'''
obj = (['smaller7tmono.wav'],[[(0.0, 5.5), (8.2, 15.7), (17.2, 19)]])

pickle.dump(obj, open('data.in', 'wb'))
'''



