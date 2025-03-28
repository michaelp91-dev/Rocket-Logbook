#!/usr/bin/env python3

import os
import sys
import argparse
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from rich.markdown import Markdown
from datetime import datetime
from rocket_logbook.data_manager import DataManager
from rocket_logbook.models import LaunchRecord
from rocket_logbook.stats import calculate_statistics
from rocket_logbook.utils import validate_date, clear_screen, format_date_for_display

console = Console()
data_manager = DataManager()

def main():
    """Main entry point of the application."""
    parser = argparse.ArgumentParser(description="Model Rocket Launch Logbook")
    parser.add_argument("--stats", action="store_true", help="Display statistics about launches")
    parser.add_argument("--list", action="store_true", help="List all launches")
    parser.add_argument("--search", type=str, help="Search for launches by rocket type or date (YYYY-MM-DD)")
    parser.add_argument("--data-file", type=str, help="Specify a custom data file path")
    
    args = parser.parse_args()
    
    # If a custom data file is specified, use it
    if args.data_file:
        global data_manager
        data_manager = DataManager(args.data_file)
    
    if args.stats:
        display_statistics()
        return
    elif args.list:
        list_all_launches()
        return
    elif args.search:
        search_launches(args.search)
        return
    
    # If no command line arguments, start interactive mode
    show_main_menu()
    
def show_main_menu():
    """Display the main menu and handle user choices."""
    while True:
        clear_screen()
        console.print(Panel.fit("[bold blue]Model Rocket Launch Logbook[/bold blue]", 
                               border_style="blue"))
        
        console.print("\n[bold]Please select an option:[/bold]")
        console.print("1. Add New Launch Record")
        console.print("2. View Launch Records")
        console.print("3. Edit Launch Record")
        console.print("4. Delete Launch Record")
        console.print("5. Search/Filter Launch Records")
        console.print("6. Display Statistics")
        console.print("0. Exit")
        
        choice = Prompt.ask("Enter your choice", choices=["0", "1", "2", "3", "4", "5", "6"])
        
        if choice == "1":
            add_launch_record()
        elif choice == "2":
            list_all_launches()
        elif choice == "3":
            edit_launch_record()
        elif choice == "4":
            delete_launch_record()
        elif choice == "5":
            search_menu()
        elif choice == "6":
            display_statistics()
        elif choice == "0":
            console.print("[bold green]Thank you for using the Model Rocket Launch Logbook![/bold green]")
            sys.exit(0)

def add_launch_record():
    """Add a new launch record to the logbook."""
    clear_screen()
    console.print(Panel("[bold]Add New Launch Record[/bold]", border_style="green"))
    
    try:
        # Get and validate date
        date_str = Prompt.ask("Date of launch (YYYY-MM-DD)")
        if not validate_date(date_str):
            console.print("[bold red]Invalid date format. Please use YYYY-MM-DD.[/bold red]")
            input("\nPress Enter to continue...")
            return
        
        # Get remaining details
        rocket_name = Prompt.ask("Rocket name")
        motor_type = Prompt.ask("Motor type")
        
        altitude_valid = False
        altitude = 0
        while not altitude_valid:
            try:
                altitude = float(Prompt.ask("Estimated altitude (meters)"))
                altitude_valid = True
            except ValueError:
                console.print("[bold red]Please enter a valid number for altitude[/bold red]")
        
        success = Confirm.ask("Was the launch successful?")
        notes = Prompt.ask("Notes (optional)", default="")
        
        # Create and save the new record
        new_record = LaunchRecord(
            id=data_manager.get_next_id(),
            date=date_str,
            rocket_name=rocket_name,
            motor_type=motor_type,
            altitude=altitude,
            success=success,
            notes=notes
        )
        
        data_manager.add_record(new_record)
        console.print("[bold green]Launch record added successfully![/bold green]")
    
    except Exception as e:
        console.print(f"[bold red]Error adding launch record: {str(e)}[/bold red]")
    
    input("\nPress Enter to continue...")

def list_all_launches():
    """Display all launch records in a table."""
    clear_screen()
    records = data_manager.get_all_records()
    
    if not records:
        console.print("[bold yellow]No launch records found.[/bold yellow]")
        input("\nPress Enter to continue...")
        return
    
    display_launch_records(records)
    input("\nPress Enter to continue...")

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

def edit_launch_record():
    """Edit an existing launch record."""
    clear_screen()
    console.print(Panel("[bold]Edit Launch Record[/bold]", border_style="yellow"))
    
    records = data_manager.get_all_records()
    if not records:
        console.print("[bold yellow]No launch records found to edit.[/bold yellow]")
        input("\nPress Enter to continue...")
        return
    
    display_launch_records(records)
    
    try:
        record_id = int(Prompt.ask("Enter ID of the record to edit"))
        record = data_manager.get_record_by_id(record_id)
        
        if not record:
            console.print(f"[bold red]No record found with ID {record_id}[/bold red]")
            input("\nPress Enter to continue...")
            return
        
        console.print(f"\n[bold]Editing record {record_id}:[/bold]")
        
        # Prompt for updated values, using current values as defaults
        date_str = Prompt.ask("Date of launch (YYYY-MM-DD)", default=record.date)
        if not validate_date(date_str):
            console.print("[bold red]Invalid date format. Using original date.[/bold red]")
            date_str = record.date
            
        rocket_name = Prompt.ask("Rocket name", default=record.rocket_name)
        motor_type = Prompt.ask("Motor type", default=record.motor_type)
        
        altitude_str = Prompt.ask("Estimated altitude (meters)", default=str(record.altitude))
        try:
            altitude = float(altitude_str)
        except ValueError:
            console.print("[bold red]Invalid altitude value. Using original value.[/bold red]")
            altitude = record.altitude
            
        success = Confirm.ask("Was the launch successful?", default=record.success)
        notes = Prompt.ask("Notes", default=record.notes)
        
        # Update the record
        updated_record = LaunchRecord(
            id=record_id,
            date=date_str,
            rocket_name=rocket_name,
            motor_type=motor_type,
            altitude=altitude,
            success=success,
            notes=notes
        )
        
        data_manager.update_record(updated_record)
        console.print("[bold green]Launch record updated successfully![/bold green]")
        
    except ValueError:
        console.print("[bold red]Please enter a valid ID number[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error updating record: {str(e)}[/bold red]")
    
    input("\nPress Enter to continue...")

def delete_launch_record():
    """Delete an existing launch record."""
    clear_screen()
    console.print(Panel("[bold]Delete Launch Record[/bold]", border_style="red"))
    
    records = data_manager.get_all_records()
    if not records:
        console.print("[bold yellow]No launch records found to delete.[/bold yellow]")
        input("\nPress Enter to continue...")
        return
    
    display_launch_records(records)
    
    try:
        record_id = int(Prompt.ask("Enter ID of the record to delete"))
        record = data_manager.get_record_by_id(record_id)
        
        if not record:
            console.print(f"[bold red]No record found with ID {record_id}[/bold red]")
            input("\nPress Enter to continue...")
            return
        
        console.print(f"\n[bold]Record to delete:[/bold]")
        console.print(f"Date: {format_date_for_display(record.date)}")
        console.print(f"Rocket: {record.rocket_name}")
        console.print(f"Motor: {record.motor_type}")
        
        confirm = Confirm.ask("Are you sure you want to delete this record?")
        if confirm:
            data_manager.delete_record(record_id)
            console.print("[bold green]Launch record deleted successfully![/bold green]")
        else:
            console.print("Deletion cancelled.")
            
    except ValueError:
        console.print("[bold red]Please enter a valid ID number[/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error deleting record: {str(e)}[/bold red]")
    
    input("\nPress Enter to continue...")

def search_menu():
    """Display search/filter options menu."""
    clear_screen()
    console.print(Panel("[bold]Search/Filter Launch Records[/bold]", border_style="blue"))
    
    console.print("\n[bold]Search options:[/bold]")
    console.print("1. Search by date")
    console.print("2. Search by rocket type")
    console.print("0. Back to main menu")
    
    choice = Prompt.ask("Enter your choice", choices=["0", "1", "2"])
    
    if choice == "1":
        date_search()
    elif choice == "2":
        rocket_type_search()

def date_search():
    """Search for launch records by date."""
    clear_screen()
    console.print(Panel("[bold]Search by Date[/bold]", border_style="blue"))
    
    date_str = Prompt.ask("Enter date (YYYY-MM-DD) or part of it (YYYY or YYYY-MM)")
    search_launches(date_str)

def rocket_type_search():
    """Search for launch records by rocket type."""
    clear_screen()
    console.print(Panel("[bold]Search by Rocket Type[/bold]", border_style="blue"))
    
    rocket_type = Prompt.ask("Enter rocket type or name")
    search_launches(rocket_type)

def search_launches(search_term):
    """Search for launches by date or rocket type."""
    clear_screen()
    console.print(Panel(f"[bold]Search Results for: {search_term}[/bold]", border_style="blue"))
    
    records = data_manager.search_records(search_term)
    
    if not records:
        console.print(f"[bold yellow]No records found matching '{search_term}'.[/bold yellow]")
    else:
        console.print(f"[bold green]Found {len(records)} matching records:[/bold green]")
        display_launch_records(records)
    
    input("\nPress Enter to continue...")

def display_statistics():
    """Display statistics about the launch records."""
    clear_screen()
    console.print(Panel("[bold]Launch Statistics[/bold]", border_style="green"))
    
    records = data_manager.get_all_records()
    
    if not records:
        console.print("[bold yellow]No launch records found for statistics.[/bold yellow]")
        input("\nPress Enter to continue...")
        return
    
    stats = calculate_statistics(records)
    
    # Create a new table for statistics
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Statistic")
    table.add_column("Value")
    
    table.add_row("Total Launches", str(stats['total_launches']))
    table.add_row("Successful Launches", str(stats['successful_launches']))
    table.add_row("Failed Launches", str(stats['failed_launches']))
    table.add_row("Success Rate", f"{stats['success_rate']:.2f}%")
    table.add_row("Average Altitude", f"{stats['avg_altitude']:.2f} meters")
    table.add_row("Max Altitude", f"{stats['max_altitude']:.2f} meters")
    table.add_row("Min Altitude", f"{stats['min_altitude']:.2f} meters")
    table.add_row("Most Used Rocket", stats['most_used_rocket'])
    table.add_row("Most Used Motor", stats['most_used_motor'])
    table.add_row("First Launch Date", format_date_for_display(stats['first_launch_date']))
    table.add_row("Latest Launch Date", format_date_for_display(stats['latest_launch_date']))
    
    console.print(table)
    
    input("\nPress Enter to continue...")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[bold green]Thank you for using the Model Rocket Launch Logbook![/bold green]")
        sys.exit(0)