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

    UNITS = {"speedometer": "0x100",
             "pedals": "0x200",
             "abs": "0x400",
             "tire_pressure": "0x800"}

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
        with open(file_path) as fp:
            lines = fp.readlines()

        indicies = []

        units_last_record = {unit: None for unit in
                             ArgusExercise.UNITS.values()}

        units_freq = {"0x100": 50, "0x200": 5,
                      "0x400": 10, "0x800": 100}

        for line in lines:
            index, timestamp, ID, value1, value2 = line.strip().split()

            # type conversion
            timestamp, index = int(timestamp), int(index)

            if units_last_record[ID] is None:
                units_last_record[ID] = timestamp

            else:
                if timestamp - units_last_record[ID] < units_freq[ID]:
                    indicies.append(index)
                units_last_record[ID] = timestamp

        return indicies

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
        with open(file_path) as fp:
            lines = fp.readlines()

        indicies = set()

        units_last_record = {unit: None for unit in
                             ArgusExercise.UNITS.values()}

        units_range = {"0x100": ((0, 0), (0, 300)),
                       "0x200": ((0, 100), (0, 100)),
                       "0x400": ((0, 0), (0, 1)),
                       "0x800": ((0, 0), (0, 100))}

        crash, pressed_for = False, [[0, 10], [0, 10]]

        for line in lines:
            index, timestamp, ID, value1, value2 = line.strip().split()

            # type conversion
            index, timestamp, value1, value2 = map(int, (index, timestamp,
                                                         value1, value2))

            l1, l2 = units_range[ID][0]
            h1, h2 = units_range[ID][1]

            # range anomaly 1
            if not l1 <= value1 or not value1 <= l2:
                indicies.add(index)

            # range anomaly 2
            if not h1 <= value2 or not value2 <= h2:
                indicies.add(index)

            # pedal
            if ID == "0x200":

                # gas and brakes
                if value1 * value2 != 0:
                    indicies.add(index)

                # press duration
                for n, v in enumerate((value1, value2)):

                    if v == 0:

                        delta = pressed_for[n][1] - pressed_for[n][0]

                        if delta < 10:
                            indicies.add(index)
                        pressed_for[n] = [0, 10]

                    else:
                        if pressed_for[n] == [0, 10]:
                            pressed_for[n] = [timestamp, timestamp]
                        else:
                            pressed_for[n][1] = timestamp

            # speed
            if ID == "0x100":

                # check if crash
                if crash:
                    if value2 > 0:
                        indicies.add(index)
                        crash = False

                elif units_last_record[ID] is not None:

                    prev_tmp, prev_v1, prev_v2 = units_last_record[ID]

                    # pedal pressing
                    if (timestamp - prev_tmp <= 50 and
                       abs(value2 - prev_v2) > 5):

                        # register crash
                        if value2 == 0:
                            crash = True
                        else:
                            indicies.add(index)
                            pressed_for = [[0, 10], [0, 10]]

            # update the record
            units_last_record[ID] = (timestamp, value1, value2)

        return sorted(list(indicies))

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
        with open(file_path) as fp:
            lines = fp.readlines()

        indicies = []

        units_last_record = {}

        for line in lines:
            index, timestamp, ID, value1, value2 = line.strip().split()

            # type conversion
            index, timestamp, value1, value2 = map(int, (index, timestamp,
                                                         value1, value2))

            # accelaration and brake correlations
            if ID == "0x100":

                # accelaration
                if "0x200" in units_last_record and "0x100" in units_last_record:

                    _, acc, dec = units_last_record["0x200"]
                    _, _, speed = units_last_record["0x100"]

                    if acc > 0 and value2 - speed < 0:
                        indicies.append(index)

                    elif dec > 0 and value2 - speed > 0:
                        indicies.append(index)

                # pressure (flat tire)
                if "0x800" in units_last_record:

                    _, _, pressure = units_last_record["0x800"]

                    if pressure < 30 and value2 > 50:
                        indicies.append(index)

            # ABS check
            if ID == "0x400":

                if "0x200" in units_last_record:

                    _, acc, dec = units_last_record["0x200"]

                    if value2 == 0 and dec >= 80:
                        indicies.append(index)

            # pressure while moving
            if ID == "0x800":

                if "0x100" in units_last_record and "0x800" in units_last_record:

                    _, _, speed = units_last_record["0x100"]
                    _, _, pressure = units_last_record["0x800"]

                    if (value2-pressure) > 0 and speed > 0:
                        indicies.append(index)

                    elif value2 < 30 and speed > 50:
                        indicies.append(index)

            units_last_record[ID] = [timestamp, value1, value2]

        return indicies
