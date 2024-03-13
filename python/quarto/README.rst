# Quarto

See:
- https://quarto.org
- https://quarto.org/docs/dashboards/
- https://www.youtube.com/watch?v=3HCAScFqr10


## Installation

Install quarto on Ubuntu 18+/Debian 10+ :
1. Download the latest .deb file from https://quarto.org/docs/download/ or https://github.com/quarto-dev/quarto-cli/releases/latest
2. Install it with `sudo apt install ./	quarto-1.4.551-linux-amd64.deb` or `sudo dpkg -i ./	quarto-1.4.551-linux-amd64.deb`
3. Check the installation with `quarto --version`
4. Install the Quarto VSCode extension https://marketplace.visualstudio.com/items?itemName=quarto.quarto


From this directory:

```
conda deactivate         # Only if you use Anaconda...
python3 -m venv env
source env/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
```