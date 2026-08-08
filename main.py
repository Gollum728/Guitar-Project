from tuner import tune
    
   
IN_TUNE_THRESHOLD = 5


while True:
    result = tune()
    if result is None:
        continue
    note, pitchPlayed, targetFrequency, cents = result
    output = f"Note : {note} \n Played frequency : {pitchPlayed} \n Expected frequency : {targetFrequency} \n Cents : {cents} \n"
    if abs(cents) <= IN_TUNE_THRESHOLD:
        output += f"In tune"
    elif cents > 0:
        output += f"Tune down"
    else:
        output += f"Tune up"
    print(output)





