import os
import re
import shutil
import pyfiglet

# Display banner
print(pyfiglet.figlet_format("ReelName"))

# Extensions
VIDEO_EXTS = ['.mp4', '.mkv', '.avi', '.mov']
SUBTITLE_EXTS = ['.srt', '.ass', '.sub']

def format_title_year(filename):
    """
    Extract title and year, and format as 'Title (Year)'.
    This version attempts to be more robust and avoids re-processing already formatted names.
    """
    name = filename.replace('.', ' ').replace('_', ' ').strip()
    name = re.sub(r'\s+', ' ', name) # Replace multiple spaces with a single space

    # Regex to capture title, optional year in parentheses, and any trailing characters
    match = re.match(r"^(.*?)(?:\s*\(*\s*(\d{4})\)*)(.*)$", name)
    
    if match:
        title = match.group(1).strip().title()
        year = match.group(2)
        # tail = match.group(3).strip() # Not used in the final formatted name, but kept for context if needed

        formatted = f"{title} ({year})"
        
        # Avoid re-processing if the filename already starts with the desired format
        # This is a crucial check to prevent infinite renaming loops or incorrect renames
        if filename.startswith(formatted):
            return None 
        return formatted
    return None

def preview_rename(directory):
    changes = []
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(tuple(VIDEO_EXTS)):
                old_path = os.path.join(root, file)
                filename, ext = os.path.splitext(file)
                formatted = format_title_year(filename)
                if formatted:
                    new_name = f"{formatted}{ext}"
                    new_path = os.path.join(root, new_name)
                    # Only add to changes if it's actually a different path and the new path doesn't already exist
                    if old_path != new_path and not os.path.exists(new_path):
                        changes.append((old_path, new_path))
    return changes

def apply_rename(changes):
    for old, new in changes:
        try:
            os.rename(old, new)
            print(f"Renamed: '{os.path.basename(old)}' to '{os.path.basename(new)}'")
        except OSError as e:
            print(f"Error renaming '{os.path.basename(old)}' to '{os.path.basename(new)}': {e}")
    print("✅ Files renamed.\n")

def organize_movies(directory):
    for root, _, files in os.walk(directory):
        videos = [f for f in files if f.lower().endswith(tuple(VIDEO_EXTS))]
        for video in videos:
            video_path = os.path.join(root, video)
            base_name, ext = os.path.splitext(video)
            folder_name = format_title_year(base_name)
            
            # If format_title_year returns None, it means the name couldn't be formatted or was already formatted
            if not folder_name:
                continue

            target_folder = os.path.join(directory, folder_name)
            new_video_path = os.path.join(target_folder, f"{folder_name}{ext}")

            # Check if the video is already in its target organized folder
            if os.path.abspath(os.path.dirname(video_path)) == os.path.abspath(target_folder) and os.path.basename(video_path) == os.path.basename(new_video_path):
                continue # Already organized and correctly named within its target folder

            os.makedirs(target_folder, exist_ok=True)
            try:
                # If the video is already in the target_folder, but with an unformatted name, rename it there.
                # Otherwise, move it.
                if os.path.abspath(os.path.dirname(video_path)) == os.path.abspath(target_folder) and os.path.basename(video_path) != os.path.basename(new_video_path):
                    os.rename(video_path, new_video_path)
                    print(f"Renamed (inside folder): '{os.path.basename(video_path)}' to '{os.path.basename(new_video_path)}'")
                else:
                    shutil.move(video_path, new_video_path)
                    print(f"Moved and renamed: '{os.path.basename(video_path)}' to '{os.path.basename(new_video_path)}' in '{folder_name}'")
            except shutil.Error as e:
                print(f"Error moving/renaming '{os.path.basename(video)}': {e}")
            except OSError as e:
                print(f"Error moving/renaming '{os.path.basename(video)}': {e}")

            # Move subtitle if exists and matches the base name
            for f in files:
                if f.lower().endswith(tuple(SUBTITLE_EXTS)):
                    # Check if the subtitle file's base name is similar to the video's base name before formatting
                    # This helps associate subtitles that might have slight variations but belong to the same video
                    if re.match(re.escape(base_name.lower().split('(')[0].strip()), f.lower()): # Match start of unformatted base_name
                        sub_path = os.path.join(root, f)
                        sub_ext = os.path.splitext(f)[1]
                        new_sub_path = os.path.join(target_folder, f"{folder_name}{sub_ext}")
                        
                        # Only move if it's not already in the target folder or is named differently
                        if os.path.abspath(os.path.dirname(sub_path)) != os.path.abspath(target_folder) or os.path.basename(sub_path) != os.path.basename(new_sub_path):
                            try:
                                shutil.move(sub_path, new_sub_path)
                                print(f"Moved subtitle: '{os.path.basename(sub_path)}' to '{os.path.basename(new_sub_path)}' in '{folder_name}'")
                            except shutil.Error as e:
                                print(f"Error moving subtitle '{os.path.basename(f)}': {e}")
                            except OSError as e:
                                print(f"Error moving subtitle '{os.path.basename(f)}': {e}")
    print("📦 Movies and subtitles organized into folders.\n")

def main():
    print("Choose an option:")
    print("1️⃣ Rename movies")
    print("2️⃣ Organize into folders")
    print("3️⃣ Rename and Organize")
    print("4️⃣ Exit")

    choice = input("Enter your choice (1/2/3/4): ").strip()
    if choice not in ['1', '2', '3']:
        print("👋 Exiting.")
        return

    directory = input("📁 Enter the full path to your movies folder: ").strip()
    if not os.path.isdir(directory):
        print("❌ Invalid folder. Please provide a valid directory path.")
        return

    if choice in ['1', '3']:
        changes = preview_rename(directory)
        if not changes:
            print("✅ No files need renaming based on current patterns.")
        else:
            print("\n🧾 Preview Rename:")
            for i, (old, new) in enumerate(changes, 1):
                print(f"{i}. {os.path.basename(old)} → {os.path.basename(new)}")
            confirm = input("\nProceed with renaming? (y/n): ").lower()
            if confirm == 'y':
                apply_rename(changes)
            else:
                print("❌ Rename cancelled.\n")

    if choice in ['2', '3']:
        print("📦 Organizing...")
        organize_movies(directory)

    print("✅ Done.")

if __name__ == "__main__":
    main()