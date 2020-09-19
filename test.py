from argus_exercise import ArgusExercise

argus = ArgusExercise()

# testing timing anomalies
a = argus.detect_timing_anomalies("./example_inputs/timing/100.txt")
assert a == [100]
a = argus.detect_timing_anomalies("./example_inputs/timing/1255_1256_1273_1275_1313_1316.txt")
assert a == [1255, 1256, 1273, 1275, 1313, 1316]

# testing behavioral anomalies
a = argus.detect_behavioral_anomalies("./example_inputs/behavioral/27_35_52_86306_86307.txt")
assert a == [27, 35, 52, 86306, 86307]

a = argus.detect_behavioral_anomalies("./example_inputs/behavioral/547_1289_1306.txt")
assert a == [547, 1289, 1306]

a = argus.detect_behavioral_anomalies("./example_inputs/behavioral/9839_9840_24686_24694_24703.txt")
assert a == [9839, 9840, 24686, 24694, 24703]

# correlation anomalies 
a = argus.detect_correlation_anomalies("./example_inputs/correlation/136_104183_197608_197623_197639_197641.txt")
assert a == [136, 104183, 197608, 197623, 197639, 197641]

a = argus.detect_correlation_anomalies("./example_inputs/correlation/18344.txt")
assert a == [18344]

a = argus.detect_correlation_anomalies("./example_inputs/correlation/22195_26468.txt")
assert a == [22195, 26468]

# no anomalie
for i in range(1, 5):

    file_path = "./example_inputs/no_anomalies/test{}.txt".format(i)
    a = argus.detect_timing_anomalies(file_path)
    b = argus.detect_behavioral_anomalies(file_path)
    c = argus.detect_correlation_anomalies(file_path)

    assert a+b+c == []
