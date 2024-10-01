import os
import sys
import shutil
import json
from pdf2image import convert_from_path
from PyPDF2 import PdfReader

def convert_pdfs_to_jpgs(input_directory, course_name, year):
    if not os.path.isdir(input_directory):
        print(f"Input directory {input_directory} bestaat niet.")
        return

    output_directory = os.path.join(course_name, year)
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Output directory {output_directory} aangemaakt.")

    pdf_files = [f for f in os.listdir(input_directory) if f.lower().endswith('.pdf')]
    image_files = [f for f in os.listdir(input_directory) if f.lower().endswith(('.png', '.jpg'))]

    if not pdf_files and not image_files:
        print("Geen PDF, PNG of JPG bestanden gevonden in de input directory.")
        return

    saved_images = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(input_directory, pdf_file)
        try:
            reader = PdfReader(pdf_path)
            if len(reader.pages) > 1:
                print(f"{pdf_file} heeft meer dan 1 pagina, wordt overgeslagen.")
                continue

            images = convert_from_path(pdf_path)
            jpg_path = os.path.join(output_directory, f"{os.path.splitext(pdf_file)[0]}.jpg")
            images[0].save(jpg_path, 'JPEG')
            saved_images.append(jpg_path)
            print(f"Opgeslagen: {jpg_path}")
        except Exception as e:
            print(f"Fout bij het converteren van {pdf_file}: {e}")

    for image_file in image_files:
        src_path = os.path.join(input_directory, image_file)
        dst_path = os.path.join(output_directory, image_file)
        try:
            shutil.copy(src_path, dst_path)
            saved_images.append(dst_path)
            print(f"Bestand gekopieerd: {dst_path}")
        except Exception as e:
            print(f"Fout bij het kopiëren van {image_file}: {e}")

    # Schrijf de lijst van opgeslagen afbeeldingen naar een JSON bestand
    json_path = os.path.join(output_directory, 'posters.json')
    json_data = {
        "course_name": course_name,
        "year": year,
        "saved_images": saved_images
    }
    try:
        with open(json_path, 'w') as json_file:
            json.dump(json_data, json_file, indent=4)
        print(f"JSON bestand opgeslagen: {json_path}")
    except Exception as e:
        print(f"Fout bij het opslaan van JSON bestand: {e}")

if __name__ == "__main__":
    input_directory = input("Voer de input directory in: ")
    course_name = input("Voer de naam van het vak in: ")
    year = input("Voer het jaar in: ")
    convert_pdfs_to_jpgs(input_directory, course_name, year)