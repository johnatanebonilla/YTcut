

# YT Clip Extractor

This script processes an Excel file containing YouTube video IDs and timestamps, downloads the specified videos, and extracts clips around the specified timestamps. 

## Installation

You can clone the repository using the following link:

```sh
git clone https://github.com/johnatanebonilla/extract_clip.git
cd extract_clip
```

The script automatically installs the required dependencies (`pandas`, `yt-dlp`, and `moviepy`). 

## Usage

Run the script from the command line with the following arguments:

- `--filename`: Path to the Excel file
- `--sheet`: Sheet name in the Excel file
- `--columnword`: Column name for the key word of the timestamp (e.g. haber)
- `--columntimestamp`: Column name for the exact timestamp (in seconds)
- `--columnid`: Column name for the video ID (put the name in quotes if it contains spaces)
- `--output`: Output folder for the videos and clips
- `--start_time`: (Optional) Start time offset in seconds before the timestamp (default: 10 seconds)
- `--end_time`: (Optional) End time offset in seconds after the timestamp (default: 10 seconds)

Example command:

```sh
python extract_clip.py --filename /path/to/excel_file.xlsx --sheet SheetName --columnword Haber --columntimestamp Exact_Timestamp --columnid "Video ID" --output /path/to/output_folder --start_time 5 --end_time 15
```

## Table Format

The Excel file should have minimun the following columns:

- `Keyword`: The keyword (e.g. "Haber")
- `Exact_Timestamp`: The exact timestamp in seconds
- `Video ID`: The ID of the YouTube video

Example:

| Before                                                             | Haber | After                                                        | Exact_Timestamp | Video ID   |
|--------------------------------------------------------------------|-------|--------------------------------------------------------------|-----------------|------------|
| la nueva propiedad del mirador del río cuyos terrenos aunque       | hay   | ahí una disputa con unos particulares esos terrenos no son   | 139             | mnQy0hJ3I9o|
| que está en atrás en la trasera eso está claro                     | hay   | un valor de mercado es decir en este caso es                 | 554             | ly5Y7uQgPi0|
| una atención especializada en canarias las mujeres pueden estar tranquilas | hay   | un compromiso por parte del gobierno de canarias y hay       | 63              | TS4WPDvWiRw|

## Contact

For more information, contact johnatanebonilla@gmail.com.
