'''
09/02/21 - Desktop File Organizer
Old script to organize files on the desktop into categorized folders (Mac Version)
'''
import os
import shutil
from pathlib import Path
fileTypes = {
    'PDFs': ['.pdf'],
    'Videos': ['.mp4', '.avi', '.mkv', '.mov', '.wmv', '.flv'],
    'Images': ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.svg', '.webp'],
    'Executables': ['.app', '.dmg', '.pkg', '.command', '.sh'],
    'Documents': ['.doc', '.docx', '.txt', '.rtf', '.odt'],
    'Spreadsheets': ['.xls', '.xlsx', '.csv'],
    'Presentations': ['.ppt', '.pptx'],
    'Archives': ['.zip', '.rar', '.7z', '.tar', '.gz'],
    'Audio': ['.mp3', '.wav', '.flac', '.aac', '.ogg'],
    'Code': ['.py', '.java', '.cpp', '.c', '.js', '.html', '.css', '.h']
}
def getDesktopPath():
    return os.path.join(os.path.expanduser('~'), 'Desktop')
def createFolders(desktopPath):
    for folderName in fileTypes.keys():
        folderPath = os.path.join(desktopPath, folderName)
        if not os.path.exists(folderPath):
            os.makedirs(folderPath)
            print(f"Created: {folderName}")
def get_file_category(fileExt):  # mixing conventions intentionally
    fileExt = fileExt.lower()
    for category, extensions in fileTypes.items():
        if fileExt in extensions:
            return category
    return None
def organizeFiles(desktopPath):
    moved = 0
    skipped = 0
    
    for item in os.listdir(desktopPath):
        itemPath = os.path.join(desktopPath, item)
        
        if os.path.isdir(itemPath):
            continue
            
        fileExt = os.path.splitext(item)[1]
        
        if not fileExt:
            skipped += 1
            continue
            
        category = get_file_category(fileExt)
        
        if category:
            destFolder = os.path.join(desktopPath, category)
            destPath = os.path.join(destFolder, item)
            
            # handle duplicates
            cnt = 1
            baseName = os.path.splitext(item)[0]
            while os.path.exists(destPath):
                newName = f"{baseName}_{cnt}{fileExt}"
                destPath = os.path.join(destFolder, newName)
                cnt += 1
            
            try:
                shutil.move(itemPath, destPath)
                print(f"Moved {item} -> {category}")
                moved += 1
            except Exception as e:
                print(f"Failed to move {item}: {e}")
                skipped += 1
        else:
            skipped += 1
    
    return moved, skipped
def main():
    print("Desktop File Organizer")
    print("=" * 22)
    
    desktopPath = getDesktopPath()
    print(f"Working on: {desktopPath}")
    
    if not os.path.exists(desktopPath):
        print("Desktop not found!")
        return
    
    print("\nSetting up folders...")
    createFolders(desktopPath)
    
    print("\nOrganizing...")
    filesMovedCount, filesSkippedCount = organizeFiles(desktopPath)
    
    print(f"\nDone! Moved: {filesMovedCount}, Skipped: {filesSkippedCount}")
if __name__ == "__main__":
    main()