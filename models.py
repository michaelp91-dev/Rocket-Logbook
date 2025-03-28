class LaunchRecord:
    """Model class representing a single rocket launch record."""
    
    def __init__(self, id, date, rocket_name, motor_type, altitude, success, notes=""):
        """
        Initialize a new launch record.
        
        Args:
            id (int): Unique identifier for the record
            date (str): Date of the launch in YYYY-MM-DD format
            rocket_name (str): Name of the rocket
            motor_type (str): Type/model of motor used
            altitude (float): Estimated altitude reached in meters
            success (bool): Whether the launch was successful
            notes (str, optional): Additional notes about the launch
        """
        self.id = id
        self.date = date
        self.rocket_name = rocket_name
        self.motor_type = motor_type
        self.altitude = altitude
        self.success = success
        self.notes = notes
    
    def to_dict(self):
        """
        Convert the launch record to a dictionary for JSON serialization.
        
        Returns:
            dict: Dictionary representation of the launch record
        """
        return {
            'id': self.id,
            'date': self.date,
            'rocket_name': self.rocket_name,
            'motor_type': self.motor_type,
            'altitude': self.altitude,
            'success': self.success,
            'notes': self.notes
        }
    
    def __str__(self):
        """Return a string representation of the launch record."""
        status = "Successful" if self.success else "Failed"
        return f"Launch {self.id}: {self.date} - {self.rocket_name} ({status})"
