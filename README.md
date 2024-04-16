# Diablo 4 Damage Calculator

This project is a tool designed to assist Diablo 4 players in calculating total damage and DPS (Damage Per Second) of their characters, enabling them to optimize their equipment more efficiently.

## Features

- **Total Damage Calculation:** The tool detects and sums the damage numbers that appear during gameplay, providing an accurate estimation of the total damage dealt.

- **Real-Time DPS:** Calculates DPS based on total damage and elapsed time, allowing players to assess their equipment performance and make adjustments accordingly.

- **Integration of EasyOCR:** Utilizes EasyOCR as the base for Optical Character Recognition (OCR), enabling detection and extraction of damage numbers from the game screen.

## Installation

- **Clone the GitHub package:** Use the following terminal command:
```
gh repo clone CorDub/Diablo-4-DPS-Meter
```

- **Install all dependencies:** Get into the Diablo-4-DPS-Meter folder and use the following terminal command (don't forget the dot):
```
pip install -e .
```

- **Run the app:** Once everything is installed, run the app with the command line `python D4DPSM/app.py`. This will print within the terminal "Running on local URL" and "Runnning on public URL" with two URLs. Copy either and paste them into your web browser. This will display the web interface. Once it is available, upload a video of your gameplay and click "Submit". Just wait for processing and you will be able to know how much damage you dealt :)

## Credits

- Developed by [Corentin Dubois](https://github.com/CorDub)
- Developed by [Jack Wotton](https://github.com/jlwotton17)
