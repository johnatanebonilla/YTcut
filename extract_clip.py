import subprocess
import sys

# Instalar las dependencias necesarias si no están instaladas
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import pandas as pd
except ImportError:
    install('pandas')
    import pandas as pd

try:
    from yt_dlp import YoutubeDL
except ImportError:
    install('yt-dlp')
    from yt_dlp import YoutubeDL

try:
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
except ImportError:
    install('moviepy')
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip

import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('--filename', type=str, required=True, help='Path to the Excel file')
    parser.add_argument('--sheet', type=str, required=True, help='Sheet name in the Excel file')
    parser.add_argument('--columnword', type=str, required=True, help='Column name for the word "haber"')
    parser.add_argument('--columntimestamp', type=str, required=True, help='Column name for the exact timestamp')
    parser.add_argument('--columnid', type=str, required=True, help='Column name for the video ID')
    parser.add_argument('--output', type=str, required=True, help='Output folder for the videos and clips')
    return parser.parse_args()

# Función para descargar un video de YouTube usando yt-dlp
def download_video(video_id, output_dir):
    video_url = f"https://www.youtube.com/watch?v={video_id}"
    output_path = os.path.join(output_dir, f"{video_id}.mp4")
    
    if not os.path.exists(output_path):
        ydl_opts = {
            'format': 'best[height<=360]',  # Descargar el mejor formato disponible con una altura de hasta 360p
            'outtmpl': output_path,
            'noplaylist': True,
            'continuedl': False,  # No intentar reanudar descargas
        }
        
        success = False
        while not success:
            try:
                with YoutubeDL(ydl_opts) as ydl:
                    ydl.download([video_url])
                success = True
            except Exception as e:
                print(f"Error al descargar {video_id}: {e}")
                # Puedes implementar un límite de reintentos aquí si es necesario
                
    return output_path

# Función para cortar un clip de un video
def cut_clip(video_path, start_time, end_time, output_path):
    if not os.path.exists(output_path):
        ffmpeg_extract_subclip(video_path, start_time, end_time, targetname=output_path)

def main():
    args = parse_arguments()

    # Cargar el archivo Excel
    df = pd.read_excel(args.filename, sheet_name=args.sheet)

    # Inicializar la columna 'clip' con True para todos los videos
    df['clip'] = True

    processed_videos = set()
    clip_counter = 1  # Inicializar el contador de clips

    output_video_dir = os.path.join(args.output, "videos")
    output_clip_dir = os.path.join(args.output, "clips")

    # Crear las carpetas de salida si no existen
    os.makedirs(output_video_dir, exist_ok=True)
    os.makedirs(output_clip_dir, exist_ok=True)

    for idx, row in df.iterrows():
        if row['clip'] == True:
            video_id = row[args.columnid]
            exact_timestamp = row[args.columntimestamp]
            haber = row[args.columnword]

            # Descargar el video si no ha sido descargado ya
            video_path = os.path.join(output_video_dir, f"{video_id}.mp4")
            if video_id not in processed_videos:
                video_path = download_video(video_id, output_video_dir)
                processed_videos.add(video_id)

            # Calcular los tiempos de inicio y fin del clip (10 segundos antes y después)
            start_time = max(exact_timestamp - 10, 0)
            end_time = exact_timestamp + 10

            # Crear el nombre del archivo de salida para el clip con un entero autoincremental
            clip_output_path = os.path.join(output_clip_dir, f"{clip_counter}_{haber}_{video_id}_{exact_timestamp}_clip.mp4")

            # Cortar el clip
            cut_clip(video_path, start_time, end_time, clip_output_path)

            # Incrementar el contador de clips
            clip_counter += 1

    print("Clips creados exitosamente y videos completos guardados.")

if __name__ == '__main__':
    main()

