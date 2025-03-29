# Rocket Logbook

A terminal-based logbook application for tracking model rocket launches.

## Features

- Record details of your model rocket launches including date, rocket name, motor type, altitude, success, and notes
- View all launch records in a formatted table
- Edit and delete existing records
- Search for records by date or rocket type
- View statistics about your launches including success rates, altitude records, and most used rockets/motors

## Installation

You can install Rocket Logbook directly from this repository:

```bash
pip install git+https://github.com/michaelp91-dev/rocket-logbook.git
```

Or install it locally for development:

```bash
git clone https://github.com/michaelp91-dev/rocket-logbook.git
cd rocket-logbook
pip install -e .
```

### Installation on Termux (Android)

To install and use Rocket Logbook on Termux:

1. Install Termux from the F-Droid store
2. Update packages and install Python:
   ```bash
   pkg update && pkg upgrade
   pkg install python
   ```
3. Install Rocket Logbook:
   ```bash
   pip install git+https://github.com/michaelp91-dev/rocket-logbook.git
   ```

## Usage

After installation, you can run Rocket Logbook using:

```bash
rocket-logbook
```

Or run it directly from the repository:

```bash
python rocket_logbook.py
```

### Command Line Arguments

- `--stats`: Display statistics about your launches
- `--list`: List all launches
- `--search [TERM]`: Search for launches by rocket type or date
- `--data-file [PATH]`: Specify a custom data file path

## Data Storage

By default, Rocket Logbook stores your launch data in JSON format at:
- Linux/Mac: `~/.local/share/rocket-logbook/rocket_launches.json`
- Windows: `C:\Users\<Username>\AppData\Local\rocket-logbook\rocket-logbook\rocket_launches.json`

You can specify a custom data file using the `--data-file` option.

## License

MIT