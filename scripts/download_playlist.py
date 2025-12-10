#!/usr/bin/env python3
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Leetspeak mapping
LEET_MAP = str.maketrans({
    'a': '4', 'A': '4',
    'e': '3', 'E': '3',
    'i': '1', 'I': '1',
    'o': '0', 'O': '0',
    's': '5', 'S': '5',
    't': '7', 'T': '7',
    'l': '1', 'L': '1',
})

def to_leetspeak(text):
    return text.translate(LEET_MAP)

def main():
    print("🎵 Spotify/YouTube Playlist Downloader (Leetspeak Edition) 🎵")
    print("---------------------------------------------------------")
    
    # Get inputs
    playlist_url = input("Enter Playlist URL: ").strip()
    if not playlist_url:
        print("Error: URL is required")
        sys.exit(1)
        
    folder_name = input("Enter Playlist Name (folder name): ").strip()
    if not folder_name:
        print("Error: Playlist name is required")
        sys.exit(1)

    # Setup directories
    base_dir = Path("playlists")
    output_dir = base_dir / folder_name
    
    # Check if exists
    if output_dir.exists():
        resp = input(f"Warning: Folder '{folder_name}' already exists. Overwrite? (y/n): ").lower()
        if resp == 'y':
            shutil.rmtree(output_dir)
        else:
            print("Aborted.")
            sys.exit(0)
            
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\n🚀 Starting download to: {output_dir}")
    print("Process: Download -> Rename (Leetspeak)")
    
    try:
        # Download using yt-dlp with index
        cmd = [
            "yt-dlp",
            "-x", "--audio-format", "mp3",
            "--output", str(output_dir / "%(playlist_index)02d_%(title)s.%(ext)s"),
            "--yes-playlist",
            # Add some robustness options
            "--ignore-errors",
            "--no-warnings",
            playlist_url
        ]
        
        subprocess.run(cmd, check=True)
        
        print("\n✨ Download complete. Transforming to Leetspeak...")
        
        # Rename files
        count = 0
        for file_path in sorted(output_dir.glob("*.mp3")):
            # Split index and name
            if "_" in file_path.name:
                parts = file_path.name.split("_", 1)
                if len(parts) == 2:
                    index, rest = parts
                    name_stem = file_path.stem.split("_", 1)[1]
                    
                    # Convert name part to leetspeak
                    leet_name = to_leetspeak(name_stem)
                    
                    # Reconstruct filename: 01_L337N4M3.mp3
                    new_name = f"{index}_{leet_name}{file_path.suffix}"
                    new_path = file_path.parent / new_name
                    
                    if new_path != file_path:
                        file_path.rename(new_path)
                        count += 1
                        print(f"Renamed: {file_path.name} -> {new_name}")
        
        print(f"\n✅ Done! {count} files processed.")
        print(f"To play this playlist, run: /playlist switch {folder_name}")
        
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Error during download: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
