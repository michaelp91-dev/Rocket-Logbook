import os
import json
from datetime import datetime
from rocket_logbook.models import LaunchRecord
import appdirs

class DataManager:
    """Handles all data persistence operations for the rocket logbook."""
    
    def __init__(self, data_file=None):
        """Initialize the data manager with the specified data file."""
        if data_file is None:
            # Use a default data file in the user's app data directory
            app_data_dir = appdirs.user_data_dir("rocket-logbook", "rocket-logbook")
            # Create app data directory if it doesn't exist
            os.makedirs(app_data_dir, exist_ok=True)
            self.data_file = os.path.join(app_data_dir, "rocket_launches.json")
        else:
            self.data_file = data_file
        
        self.ensure_data_file_exists()
    
    def ensure_data_file_exists(self):
        """Ensure the data file exists, creating it if necessary."""
        if not os.path.exists(self.data_file):
            with open(self.data_file, 'w') as f:
                json.dump([], f)
    
    def get_all_records(self):
        """Retrieve all launch records from the data file."""
        try:
            with open(self.data_file, 'r') as f:
                data = json.load(f)
                return [LaunchRecord(**record) for record in data]
        except (json.JSONDecodeError, FileNotFoundError):
            # If the file is empty or has invalid JSON, return an empty list
            return []
    
    def get_record_by_id(self, record_id):
        """
        Retrieve a specific launch record by ID.
        
        Args:
            record_id: The ID of the record to retrieve
            
        Returns:
            LaunchRecord object if found, None otherwise
        """
        records = self.get_all_records()
        for record in records:
            if record.id == record_id:
                return record
        return None
    
    def get_next_id(self):
        """Generate the next available ID for a new record."""
        records = self.get_all_records()
        if not records:
            return 1
        
        # Find the maximum ID and increment by 1
        max_id = max(record.id for record in records)
        return max_id + 1
    
    def add_record(self, record):
        """
        Add a new launch record to the data file.
        
        Args:
            record: LaunchRecord object to add
        """
        records = self.get_all_records()
        records.append(record)
        self._save_records(records)
    
    def update_record(self, updated_record):
        """
        Update an existing launch record.
        
        Args:
            updated_record: LaunchRecord object with the updated data
        
        Returns:
            bool: True if successful, False if record not found
        """
        records = self.get_all_records()
        for i, record in enumerate(records):
            if record.id == updated_record.id:
                records[i] = updated_record
                self._save_records(records)
                return True
        return False
    
    def delete_record(self, record_id):
        """
        Delete a launch record by ID.
        
        Args:
            record_id: ID of the record to delete
            
        Returns:
            bool: True if successful, False if record not found
        """
        records = self.get_all_records()
        initial_length = len(records)
        
        records = [record for record in records if record.id != record_id]
        
        if len(records) < initial_length:
            self._save_records(records)
            return True
        return False
    
    def search_records(self, search_term):
        """
        Search for records matching a search term.
        
        Args:
            search_term: String to search for in dates or rocket names/types
            
        Returns:
            List of matching LaunchRecord objects
        """
        records = self.get_all_records()
        results = []
        
        # Convert search term to lowercase for case-insensitive comparison
        search_term = search_term.lower()
        
        for record in records:
            # Check if search term is in date
            if search_term in record.date:
                results.append(record)
                continue
                
            # Check if search term is in rocket name or motor type
            if (search_term in record.rocket_name.lower() or 
                search_term in record.motor_type.lower()):
                results.append(record)
                
        return results
    
    def _save_records(self, records):
        """
        Save the records list to the data file.
        
        Args:
            records: List of LaunchRecord objects to save
        """
        # Convert LaunchRecord objects to dictionaries
        records_dict = [record.to_dict() for record in records]
        
        with open(self.data_file, 'w') as f:
            json.dump(records_dict, f, indent=4)