import datetime


class Utils():
    """
    """
    @staticmethod
    def date_now():
        current_time = datetime.datetime.now()
        current_time_str = current_time.strftime("%Y-%m-%d %H:%M:%S")
        return current_time_str


utils = Utils()
