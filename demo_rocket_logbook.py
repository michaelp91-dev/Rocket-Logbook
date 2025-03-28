#!/usr/bin/env python3
"""
Demo script for Rocket Logbook that showcases key features
"""

import sys
import random
from datetime import datetime, timedelta
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rocket_logbook.models import LaunchRecord
from rocket_logbook.data_manager import DataManager
from rocket_logbook.stats import calculate_statistics
from rocket_logbook.utils import format_date_for_display

console = Console()

# Create a temporary data manager for demo purposes
data_manager = DataManager("demo_rocket_launches.json")

def display_launch_records(records):
    """Display the provided launch records in a formatted table."""
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim")
    table.add_column("Date")
    table.add_column("Rocket Name")
    table.add_column("Motor Type")
    table.add_column("Altitude (m)")
    table.add_column("Success")
    table.add_column("Notes")
    
    for record in records:
        success_str = "[green]Yes[/green]" if record.success else "[red]No[/red]"
        table.add_row(
            str(record.id),
            format_date_for_display(record.date),
            record.rocket_name,
            record.motor_type,
            str(record.altitude),
            success_str,
            record.notes[:30] + ('...' if len(record.notes) > 30 else '')
        )
    
    console.print(table)

def demo_features():
    """Demo the key features of the rocket logbook."""
    # Clear any existing demo data
    import os
    if os.path.exists("demo_rocket_launches.json"):
        os.remove("demo_rocket_launches.json")
    
    # Generate some sample data
    console.print(Panel("[bold]Generating Sample Launch Data[/bold]", border_style="green"))
    
    # Create sample rocket data
    rockets = [
        {"name": "Estes Alpha III", "motors": ["A8-3", "B6-4", "C6-5"]},
        {"name": "Quest Big Dog", "motors": ["B4-4", "B6-4", "C6-5"]},
        {"name": "FlisKits Deuce's Wild", "motors": ["A8-3", "B4-2"]},
        {"name": "Estes Crossfire ISX", "motors": ["D12-5", "E9-6"]},
        {"name": "LOC Precision Onyx", "motors": ["E9-4", "E12-4", "F10-4"]}
    ]
    
    # Generate random dates over the last year
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)  # One year ago
    
    # Sample notes
    notes_options = [
        "Perfect flight, straight as an arrow!",
        "Slight wind drift but good recovery.",
        "Parachute failed to deploy fully.",
        "Motor ejection was delayed, minor damage to rocket.",
        "Great flight but landed in a tree.",
        "First flight with this rocket.",
        "Modified rocket with custom fins.",
        "Recovery was in tall grass, almost lost it!",
        "Crowd favorite at the club launch.",
        ""  # Empty note option
    ]
    
    # Generate 15 random launch records
    for i in range(1, 16):
        # Random date within the last year
        days_offset = random.randint(0, 365)
        launch_date = (start_date + timedelta(days=days_offset)).strftime("%Y-%m-%d")
        
        # Random rocket and motor
        rocket = random.choice(rockets)
        rocket_name = rocket["name"]
        motor_type = random.choice(rocket["motors"])
        
        # Random altitude based on motor type
        if motor_type.startswith("A"):
            altitude = random.uniform(50, 150)
        elif motor_type.startswith("B"):
            altitude = random.uniform(100, 250)
        elif motor_type.startswith("C"):
            altitude = random.uniform(200, 400)
        elif motor_type.startswith("D"):
            altitude = random.uniform(300, 500)
        elif motor_type.startswith("E"):
            altitude = random.uniform(400, 700)
        else:  # F motors
            altitude = random.uniform(600, 900)
        
        # 80% success rate
        success = random.random() < 0.8
        
        # Random notes
        notes = random.choice(notes_options)
        
        # Create and save the record
        record = LaunchRecord(
            id=i,
            date=launch_date,
            rocket_name=rocket_name,
            motor_type=motor_type,
            altitude=altitude,
            success=success,
            notes=notes
        )
        
        data_manager.add_record(record)
    
    console.print("[bold green]Sample data generated![/bold green]")
    console.print()
    
    # Demo 1: List all records
    console.print(Panel("[bold]Demo: Viewing All Launch Records[/bold]", border_style="blue"))
    all_records = data_manager.get_all_records()
    display_launch_records(all_records)
    console.print()
    
    # Demo 2: Search functionality
    console.print(Panel("[bold]Demo: Searching for Records[/bold]", border_style="yellow"))
    console.print("[bold]1. Search by rocket name (Estes):[/bold]")
    estes_records = data_manager.search_records("Estes")
    display_launch_records(estes_records)
    console.print()
    
    # Demo 3: Statistics
    console.print(Panel("[bold]Demo: Launch Statistics[/bold]", border_style="green"))
    stats = calculate_statistics(all_records)
    
    # Create a statistics table
    stats_table = Table(show_header=True, header_style="bold magenta")
    stats_table.add_column("Statistic")
    stats_table.add_column("Value")
    
    stats_table.add_row("Total Launches", str(stats['total_launches']))
    stats_table.add_row("Successful Launches", str(stats['successful_launches']))
    stats_table.add_row("Failed Launches", str(stats['failed_launches']))
    stats_table.add_row("Success Rate", f"{stats['success_rate']:.2f}%")
    stats_table.add_row("Average Altitude", f"{stats['avg_altitude']:.2f} meters")
    stats_table.add_row("Max Altitude", f"{stats['max_altitude']:.2f} meters")
    stats_table.add_row("Most Used Rocket", stats['most_used_rocket'])
    stats_table.add_row("Most Used Motor", stats['most_used_motor'])
    stats_table.add_row("First Launch Date", format_date_for_display(stats['first_launch_date']))
    stats_table.add_row("Latest Launch Date", format_date_for_display(stats['latest_launch_date']))
    
    console.print(stats_table)
    
    # Cleanup
    console.print("\n[italic]Note: Demo data was stored in 'demo_rocket_launches.json'[/italic]")
    console.print("[italic]Run the actual application with 'python rocket_logbook.py'[/italic]")

if __name__ == "__main__":
    try:
        demo_features()
    except KeyboardInterrupt:
        console.print("\n[bold]Demo interrupted.[/bold]")
        sys.exit(0)
    except Exception as e:
        console.print(f"[bold red]Error during demo: {str(e)}[/bold red]")
        sys.exit(1)