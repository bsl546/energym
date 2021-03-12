import abc
import datetime


class ScheduleAbstract(object):

    """Abstract class for handling external schedules that are fed to the FMU"""

    @abc.abstractmethod
    def generate_profile(self, start: datetime.datetime, basefreq: int, seed: int):
        """Generate yearly profile"""
        pass

    @abc.abstractmethod
    def get(self, t: datetime.datetime):
        """Get schedule at time t"""
        pass

    @abc.abstractmethod
    def predict(self, t: datetime.datetime):
        """Get prediction at time t"""
        pass
