# Trae script
A collection of my personal scripts built by vibe coding with the Trae adaptive AI IDE.

## pdf_unlock
A python script to help to decript all the encrypted pdf in current and sub-directory and save it into a new folder. ( Not for crack, used when all the document are sharing same password and you know what the password is.)

## multidel
A python script to help to delete all the files with that matching the pattern pass in.

Example：
```bash
python multidel.py "*.ts.ass"  # delete all the *.ts.ass files
```

## multiRename
A python script to help to rename all the subtitle files followed by the video file name.

Example：
```bash
    python multiRename.py                 # default mode is vid
    python multiRename.py --mode vid      # Rename the subtitle files followed by the video file name
    python multiRename.py --mode sub      # Rename the video files followed by the subtitle file name
```