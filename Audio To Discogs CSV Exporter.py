import os
import sys
import csv
from mutagen import File as MutagenFile
from pathlib import Path

AUDIO_EXTENSIONS = {
    ".mp3", ".flac", ".ogg", ".oga", ".wav", ".aiff", ".aif",
    ".aac", ".m4a", ".mp4", ".wv", ".ape", ".mpc"
}

def get_tag(tags, *keys, default=""):
    for key in keys:
        if key in tags:
            value = tags[key]
            if isinstance(value, list):
                return value
            return [str(value)]
    return [default]

def process_folder(folder, desktop):
    folder_data = {
        "artist": None,
        "albums": set(),
        "label": None,
        "catno": "none",
        "format": "File",
        "genre": set(),
        "style": set(),
        "tracks": [],
        "date": None
    }

    for root, _, files in os.walk(folder):
        for file in files:
            ext = os.path.splitext(file)[1].lower()
            if ext not in AUDIO_EXTENSIONS:
                continue

            path = os.path.join(root, file)
            audio = MutagenFile(path, easy=True)
            if not audio or not audio.tags:
                continue

            tags = audio.tags

            artist_list = get_tag(tags, "artist", default="Unknown Artist")
            artist_str = ";".join(artist_list)
            album = get_tag(tags, "album", default=os.path.splitext(file)[0])[0]
            album_artist = get_tag(tags, "albumartist", "album artist", default=artist_str)[0]
            title = get_tag(tags, "title", default=os.path.splitext(file)[0])[0]
            genre = get_tag(tags, "genre", default="none")[0]
            style = get_tag(tags, "style", "styles", default="none")[0]
            label = get_tag(tags, "label", default=f"Not On Label ({album_artist} Self-released)")[0]
            catno = get_tag(tags, "catalog", "catno", "cat#", default="none")[0]
            date = get_tag(tags, "date", "year", default="Unknown")[0]

            if folder_data["artist"] is None:
                folder_data["artist"] = album_artist
            if folder_data["label"] is None:
                folder_data["label"] = label
            if folder_data["date"] is None:
                folder_data["date"] = date

            folder_data["albums"].add(album)
            folder_data["genre"].add(genre)
            folder_data["style"].add(style)

            # Track length
            length_str = ""
            if audio.info and audio.info.length:
                minutes = int(audio.info.length // 60)
                seconds = int(audio.info.length % 60)
                length_str = f"{minutes}:{seconds:02d}"

            # Track formatting with em dash if different
            track_artist_clean = artist_str.strip()
            album_artist_clean = album_artist.strip()

            if track_artist_clean == album_artist_clean:
                track_entry = f"{title}{length_str}"
            elif album_artist_clean in track_artist_clean:
                extras = track_artist_clean.replace(album_artist_clean, "").strip(" ;,")
                track_entry = f"{extras} — {title}{length_str}" if extras else f"{title}{length_str}"
            else:
                track_entry = f"{track_artist_clean} — {title}{length_str}"

            folder_data["tracks"].append(track_entry)

    # Combine album titles if multiple
    combined_album = " / ".join(folder_data["albums"])
    combined_genre = ", ".join(sorted(folder_data["genre"]))
    combined_style = ", ".join(sorted(folder_data["style"]))

    safe_artist = "".join(c for c in folder_data["artist"] if c.isalnum() or c in " _-").strip()
    safe_album = "".join(c for c in combined_album if c.isalnum() or c in " _-").strip()
    safe_date = folder_data["date"]

    filename = f"{safe_artist} - {safe_album} ({safe_date}).csv"
    filepath = os.path.join(desktop, filename)

    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["artist", "title", "label", "catno", "format", "genre", "style", "tracks", "date"])
        writer.writerow([
            folder_data["artist"],
            combined_album,
            folder_data["label"],
            folder_data["catno"],
            folder_data["format"],
            combined_genre,
            combined_style,
            "\n".join(folder_data["tracks"]),
            folder_data["date"]
        ])

    print(f"Saved merged CSV: {filepath}")

def main():
    if len(sys.argv) < 2:
        print("Drag and drop one or more folders onto this script.")
        return

    desktop = str(Path.home() / "Desktop")

    for folder in sys.argv[1:]:
        process_folder(folder, desktop)

if __name__ == "__main__":
    main()
