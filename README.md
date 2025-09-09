# Multi-Format Audio Tag CSV Exporter

Supports common audio formats. Reads metadata tags using Mutagen. Handles multi-artist tracks. Supports multiple folders dragged onto the script.

## Features

- Supports common audio formats: MP3, FLAC, OGG, WAV, AIFF, AAC, M4A, MP4, WV, APE, MPC
- Reads metadata tags using Mutagen: Artist, Album, Album Artist, Track Title, Genre, Style, Label, Catalog Number, Year
- Handles multi-artist tracks: extra artists are clearly shown with an em dash (—) before the track title
- Supports multiple folders dragged onto the script
- Defaults for missing metadata:
  - Label: Not On Label (Artist Self-released)
  - Catalog Number: none
  - Format: File
  - Genre / Style: none
- Generates one CSV per folder, even if multiple albums exist
- CSV is automatically named: Artist - Album (Year).csv and saved to your Desktop
- Tracks are formatted without spaces before track duration (Title3:34) and with em dashes for extra artists

## Installation

1. Install Python 3
2. Install Mutagen for metadata parsing:
   pip install mutagen

## Usage

1. Download the script
2. Drag and drop one or more music folders onto the script file
3. CSV files will appear on your Desktop, ready to use
