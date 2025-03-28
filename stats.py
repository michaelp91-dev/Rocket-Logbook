from collections import Counter
from datetime import datetime

def calculate_statistics(records):
    """
    Calculate various statistics about the launch records.
    
    Args:
        records: List of LaunchRecord objects
        
    Returns:
        dict: Dictionary containing various statistics
    """
    if not records:
        return {
            'total_launches': 0,
            'successful_launches': 0,
            'failed_launches': 0,
            'success_rate': 0,
            'avg_altitude': 0,
            'max_altitude': 0,
            'min_altitude': 0,
            'most_used_rocket': "None",
            'most_used_motor': "None",
            'first_launch_date': "None",
            'latest_launch_date': "None"
        }
    
    # Basic counts
    total_launches = len(records)
    successful_launches = sum(1 for r in records if r.success)
    failed_launches = total_launches - successful_launches
    
    # Success rate percentage
    success_rate = (successful_launches / total_launches) * 100 if total_launches > 0 else 0
    
    # Altitude statistics
    altitudes = [r.altitude for r in records]
    avg_altitude = sum(altitudes) / len(altitudes) if altitudes else 0
    max_altitude = max(altitudes) if altitudes else 0
    min_altitude = min(altitudes) if altitudes else 0
    
    # Most common rocket and motor
    rocket_counter = Counter(r.rocket_name for r in records)
    motor_counter = Counter(r.motor_type for r in records)
    
    most_used_rocket = rocket_counter.most_common(1)[0][0] if rocket_counter else "None"
    most_used_motor = motor_counter.most_common(1)[0][0] if motor_counter else "None"
    
    # Date ranges
    dates = [datetime.strptime(r.date, "%Y-%m-%d") for r in records]
    first_launch_date = min(dates).strftime("%Y-%m-%d") if dates else "None"
    latest_launch_date = max(dates).strftime("%Y-%m-%d") if dates else "None"
    
    return {
        'total_launches': total_launches,
        'successful_launches': successful_launches,
        'failed_launches': failed_launches,
        'success_rate': success_rate,
        'avg_altitude': avg_altitude,
        'max_altitude': max_altitude,
        'min_altitude': min_altitude,
        'most_used_rocket': most_used_rocket,
        'most_used_motor': most_used_motor,
        'first_launch_date': first_launch_date,
        'latest_launch_date': latest_launch_date
    }

def get_monthly_launch_count(records):
    """
    Get launch counts by month.
    
    Args:
        records: List of LaunchRecord objects
        
    Returns:
        dict: Dictionary with month-year keys and count values
    """
    if not records:
        return {}
    
    monthly_counts = {}
    
    for record in records:
        date_obj = datetime.strptime(record.date, "%Y-%m-%d")
        month_year = date_obj.strftime("%Y-%m")
        
        if month_year in monthly_counts:
            monthly_counts[month_year] += 1
        else:
            monthly_counts[month_year] = 1
    
    return monthly_counts

def get_rocket_success_rates(records):
    """
    Calculate success rates for each rocket type.
    
    Args:
        records: List of LaunchRecord objects
        
    Returns:
        dict: Dictionary with rocket names as keys and success rates as values
    """
    if not records:
        return {}
    
    # Count total and successful launches for each rocket
    rocket_totals = {}
    rocket_successes = {}
    
    for record in records:
        rocket_name = record.rocket_name
        
        if rocket_name not in rocket_totals:
            rocket_totals[rocket_name] = 0
            rocket_successes[rocket_name] = 0
        
        rocket_totals[rocket_name] += 1
        if record.success:
            rocket_successes[rocket_name] += 1
    
    # Calculate success rates
    success_rates = {}
    for rocket, total in rocket_totals.items():
        success_rates[rocket] = (rocket_successes[rocket] / total) * 100
    
    return success_rates
