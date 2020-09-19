"""
This module represent an interface to the argus exercise.
"""
from abc import ABCMeta, abstractmethod


class ArgusException(Exception):
    pass


class ArgusExerciseInterface(object):
    """
    Argus exercise interface - please inherit and override the abstract methods.
    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def detect_timing_anomalies(self, file_path):
        """
        Detect timing anomalies in the provided file, as defined in the exercise.
        You can assume that the provided file will not contain any anomalies other
        than timing anomalies.

        :param file_path: Full path to the log file with messages.
                          You can assume that if the file exists and is accessible,
                          it is in the proper format.
        :type file_path: string
        :return: a list of integers containing the ids of anomalous messages in the
                 order of appearance in the provided file.
        """
        raise NotImplementedError()

    @abstractmethod
    def detect_behavioral_anomalies(self, file_path):
        """
         Detect behavioral anomalies in the provided file, as defined in the exercise.
         You can assume that the provided file will not contain any anomalies other
         than behavioral anomalies.

        :param file_path: Full path to the log file with messages.
                          You can assume that if the file exists and is accessible,
                          it is in the proper format.
        :type file_path: string
        :return: a list of integers containing the ids of anomalous messages in the
                 order of appearance in the provided file.
        """
        raise NotImplementedError()

    @abstractmethod
    def detect_correlation_anomalies(self, file_path):
        """
        Detect correlation anomalies in the provided file, as defined in the exercise.
        You can assume that the provided file will not contain any anomalies other
        than correlation anomalies.

        :param file_path: Full path to the log file with messages.
                          You can assume that if the file exists and is accessible,
                          it is in the proper format.
        :type file_path: string
        :return: a list of integers containing the ids of anomalous messages in the
                 order of appearance in the provided file.
        """
        raise NotImplementedError()
