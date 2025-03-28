#!/usr/bin/env python3
"""
Rocket Logbook - A terminal-based logbook for tracking model rocket launches

This script serves as the entry point for the application.
"""

import sys
import argparse
from rocket_logbook.main import main, list_all_launches, display_statistics, search_launches
from rocket_logbook.data_manager import DataManager

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Rocket Logbook - A terminal application for tracking model rocket launches"
    )
    parser.add_argument("--stats", action="store_true", help="Display launch statistics")
    parser.add_argument("--list", action="store_true", help="List all launches")
    parser.add_argument("--search", metavar="TERM", help="Search for launches by rocket type or date")
    parser.add_argument("--data-file", metavar="PATH", help="Specify a custom data file path")
    
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_arguments()
    
    # Set custom data file if specified
    data_manager = None
    if args.data_file:
        data_manager = DataManager(args.data_file)
    
    # Handle command line arguments
    if args.stats:
        display_statistics()
    elif args.list:
        list_all_launches()
    elif args.search:
        search_launches(args.search)
    else:
        # No arguments, run the interactive app
        main()