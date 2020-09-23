"""
This module represent an implementation to the argus exercise.
"""
from argus_exercise_interface import ArgusExerciseInterface, ArgusException


class ArgusExercise(ArgusExerciseInterface):
    """
    Argus exercise implementation.
    Please inherit from ArgusExerciseInterface and override the
    abstract methods.
    """

    #constants
    SPEEDOMETER = "0x100"
    PEDALS = "0x200"
    ABS = "0x400"
    TIRE_PRESSURE = "0x800"
   

    #unit name with hex value
    UNITS = {"speedometer": "0x100",
             "pedals": "0x200",
             "abs": "0x400",
             "tire_pressure": "0x800"}
    
    #function to opwn and read the file
    def openFile(self, file_path):
        with open(file_path) as fp:
            lines = fp.readlines()
        return lines


    def detect_timing_anomalies(self, file_path):
        """
        Detect timing anomalies in the provided file,
        as defined in the exercise.
        You can assume that the provided file will not contain any
        anomalies other than timing anomalies.

        :param file_path: Full path to the log file with messages.
                          You can assume that if the file exists and
                          is accessible, it is in the proper format.
        :type file_path: string
        :return: a list of integers containing the ids of anomalous
                 messages in the order of appearance in the provided file.
        """

        # read file
        lines = ArgusExercise.openFile(self, file_path)
        
        # list that holds the anomalies
        anomalies = []
        
        # init units dicanary key -> ecuID and vlaue -> None to save the last record in each unit
        units_last_record = {unit: None for unit in
                             ArgusExercise.UNITS.values()}
        
        #units frequency in timing anomaly
        units_frequency = {"0x100": 50, "0x200": 5,
                      "0x400": 10, "0x800": 100}

        for line in lines:
            index, timestamp, ecuID, value1, value2 = line.strip().split()

            # type conversion to time and index
            timestamp, index = int(timestamp), int(index)
            
            # if the unit is None save the last timestamp to the dictionary
            if units_last_record[ecuID] is None:
                units_last_record[ecuID] = timestamp
            
            # else if the ecu unit already have a timestamp check if there is anomaly
            else:
                if timestamp - units_last_record[ecuID] < units_frequency[ecuID]:
                    anomalies.append(index)
                units_last_record[ecuID] = timestamp

        return anomalies

    def detect_behavioral_anomalies(self, file_path):
        """
         Detect behavioral anomalies in the provided file,
         as defined in the exercise. You can assume that the provided
         file will not contain any anomalies other than behavioral anomalies.

        :param file_path: Full path to the log file with messages.
                          You can assume that if the file exists and
                          is accessible, it is in the proper format.
        :type file_path: string
        :return: a list of integers containing the ids of anomalous
                 messages in the order of appearance in the provided file.
        """

        # read file
        lines = ArgusExercise.openFile(self,file_path)
        
        # set that holds the anomalies
        anomalies = set()

        # init units dicanary key -> ecuID and vlaue -> None to save the last record in each unit
        units_last_record = {unit: None for unit in
                             ArgusExercise.UNITS.values()}
        
        #units range by specific unit
        units_range = {"0x100": ((0, 0), (0, 300)),
                       "0x200": ((0, 100), (0, 100)),
                       "0x400": ((0, 0), (0, 1)),
                       "0x800": ((0, 0), (0, 100))}
        
        # crash flag init to false
        crash = False

        #pedals pressed range
        pressed_for =  [[0, 10], [0, 10]]

        for line in lines:
            index, timestamp, ecuID, value1, value2 = line.strip().split()

            # type conversion
            index, timestamp, value1, value2 = map(int, (index, timestamp,
                                                         value1, value2))
            
            # init lower and upper ranges
            lowerRange1, lowerRange2 = units_range[ecuID][0]
            upperRange1, upperRange2 = units_range[ecuID][1]

            # range anomaly 1
            if not lowerRange1 <= value1 or not value1 <= lowerRange2:
                anomalies.add(index)

            # range anomaly 2
            if not upperRange1 <= value2 or not value2 <= upperRange2:
                anomalies.add(index)

            # pedal
            if ecuID == self.PEDALS:

                # if gas and brakes pressed simultaneously
                if value1 * value2 != 0:
                    anomalies.add(index)

                #check press duration
                for n, v in enumerate((value1, value2)):

                    if v == 0:
                        
                        # calculating the delta time the pedals are pressed
                        delta = pressed_for[n][1] - pressed_for[n][0]
                        
                        #if the delta time is lower then 10 miliseconds add to anomaly
                        if delta < 10:
                            anomalies.add(index)
                        pressed_for[n] = [0, 10]

                    else:
                        if pressed_for[n] == [0, 10]:
                            pressed_for[n] = [timestamp, timestamp]
                        else:
                            pressed_for[n][1] = timestamp

            # speedometer
            if ecuID == self.SPEEDOMETER:

                # check if crash happened
                if crash and value2 > 0:
                    anomalies.add(index)
                    crash = False
                    
                # checking if there is record in this unit
                elif units_last_record[ecuID] is not None:
                    
                    # taking the last records
                    prev_timestamp, prev_value1, prev_value2 = units_last_record[ecuID]

                    # checking that car speed is not faster then 5kmh within 50 miliseconds
                    if (timestamp - prev_timestamp <= 50 and
                       abs(value2 - prev_value2) > 5):

                        # register crash if value == 0 else add anomaly
                        if value2 == 0:
                            crash = True
                        else:
                            anomalies.add(index)
                            pressed_for = [[0, 10], [0, 10]]

            # update the record
            units_last_record[ecuID] = (timestamp, value1, value2)

        return sorted(list(anomalies))

    def detect_correlation_anomalies(self, file_path):
        """
        Detect correlation anomalies in the provided file,
        as defined in the exercise. You can assume that the provided
        file will not contain any anomalies other than correlation anomalies.

        :param file_path: Full path to the log file with messages.
                          You can assume that if the file exists and
                          is accessible, it is in the proper format.
        :type file_path: string
        :return: a list of integers containing the ids of anomalous
        messages in the order of appearance in the provided file.
        """

        # read file
        lines = ArgusExercise.openFile(self,file_path)
        
         # list that holds the anomalies
        anomalies = []
        
        # dictionary that holds the last records
        units_last_record = {}

        for line in lines:
            index, timestamp, ecuID, value1, value2 = line.strip().split()

            # type conversion
            index, timestamp, value1, value2 = map(int, (index, timestamp,
                                                         value1, value2))

            # accelaration and brake correlations
            if ecuID == self.SPEEDOMETER:

                # accelaration
                if self.PEDALS in units_last_record and self.SPEEDOMETER in units_last_record:

                    _, accelaration, brakes = units_last_record[self.PEDALS]
                    _, _, speed = units_last_record[self.SPEEDOMETER]
                    
                    # checking if accelaration is actice and speed should not decrease
                    if accelaration > 0 and value2 - speed < 0:
                        anomalies.append(index)
                    
                    # if brakes are active and the speed should not increase
                    elif brakes > 0 and value2 - speed > 0:
                        anomalies.append(index)

                # tire pressure (flat tire) check
                if self.TIRE_PRESSURE in units_last_record:

                    _, _, pressure = units_last_record[self.TIRE_PRESSURE]
                    
                    # check if tire pressure is below 30 and speed is above 50kmh add anomaly
                    if pressure < 30 and value2 > 50:
                        anomalies.append(index)

            # ABS check of a brake pedal is pressed hard
            if ecuID == self.ABS:

                if self.PEDALS in units_last_record:

                    _, accelaration, brakes = units_last_record[self.PEDALS]
                    
                    # check if brakes hard pressed(80+) and value 2 is 0 add anomaly
                    if value2 == 0 and brakes >= 80:
                        anomalies.append(index)

            # tire pressure while moving
            if ecuID == self.TIRE_PRESSURE:

                if self.SPEEDOMETER in units_last_record and self.TIRE_PRESSURE in units_last_record:

                    _, _, speed = units_last_record[self.SPEEDOMETER]
                    _, _, pressure = units_last_record[self.TIRE_PRESSURE]
                    
                    
                    if (value2-pressure) > 0 and speed > 0:
                        anomalies.append(index)
                    
                    # check if tire pressure below 30 and speed above 50kmh add anomaly
                    elif value2 < 30 and speed > 50:
                        anomalies.append(index)

            units_last_record[ecuID] = [timestamp, value1, value2]

        return anomalies
