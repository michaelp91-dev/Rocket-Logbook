#!/data/data/com.termux/files/usr/bin/bash
# Install script for Rocket Logbook on Termux (Works with Google Play version)

echo "===== Rocket Logbook Installer for Termux ====="
echo "This installer works with both F-Droid and Google Play Store versions of Termux"

# Check if running in Termux
if [ ! -d "/data/data/com.termux" ]; then
    echo "Error: This script must be run in Termux"
    exit 1
fi

# Make sure packages are up to date
echo "Updating Termux packages..."
apt update && apt upgrade -y

# If apt update fails, try to fix repositories
if [ $? -ne 0 ]; then
    echo "Package update failed. Trying to fix repositories..."
    if command -v termux-change-repo &> /dev/null; then
        echo "Using termux-change-repo to update repositories..."
        termux-change-repo
        apt update && apt upgrade -y
    else
        echo "Could not fix repositories automatically."
        echo "Please run 'pkg install termux-tools' and then 'termux-change-repo' manually."
        exit 1
    fi
fi

# Install Python and Git
echo "Installing Python and Git..."
apt install -y python git

# Install required Python packages
echo "Installing required Python packages..."
pip install rich appdirs

# Install Rocket Logbook
echo "Installing Rocket Logbook..."
cd "$HOME"
if [ -d "rocket-logbook" ]; then
    echo "Updating existing Rocket Logbook installation..."
    cd rocket-logbook
    git pull
    pip install -e .
else
    echo "Performing new Rocket Logbook installation..."
    git clone https://github.com/yourusername/rocket-logbook.git
    cd rocket-logbook
    pip install -e .
fi

# Create a launcher script in Termux's bin directory
echo "Creating launcher script..."
cat > "$PREFIX/bin/rocket-logbook" << 'EOL'
#!/data/data/com.termux/files/usr/bin/bash
python $HOME/rocket-logbook/rocket_logbook.py "$@"
EOL

# Make the launcher script executable
chmod +x "$PREFIX/bin/rocket-logbook"

echo ""
echo "===== Installation Complete! ====="
echo "You can now run Rocket Logbook by typing 'rocket-logbook' in Termux."
echo ""
echo "If you encounter any issues, you can run the app directly with:"
echo "  cd ~/rocket-logbook && python rocket_logbook.py"
echo ""
echo "To update in the future, just run this install script again."