class Weather:
    """
    Stores weather forecast
    """

    def __init__(self, time, degrees, precipitation):
        self.time = time
        self.degrees = degrees
        self.precipitation = precipitation

    def __str__(self):
        return (f"At {self.time} weather is going to be: {self.degrees} degrees with {self.precipitation} probability "
                f"of rain")
