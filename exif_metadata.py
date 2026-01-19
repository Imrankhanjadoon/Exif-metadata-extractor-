from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import pandas as pd
import os

def extract_exif(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    metadata = {}

    if exif_data:
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                gps_data = {}
                for gps_id in value:
                    gps_tag = GPSTAGS.get(gps_id, gps_id)
                    gps_data[gps_tag] = value[gps_id]
                metadata["GPSInfo"] = gps_data
            else:
                metadata[tag] = value
    return metadata

def process_images(folder_path):
    report = []
    for file in os.listdir(folder_path):
        if file.lower().endswith((".jpg", ".jpeg")):
            path = os.path.join(folder_path, file)
            metadata = extract_exif(path)
            for key, value in metadata.items():
                if key == "GPSInfo":
                    for gps_key, gps_value in value.items():
                        report.append([file, f"GPS_{gps_key}", gps_value])
                else:
                    report.append([file, key, value])

    df = pd.DataFrame(report, columns=["File", "Tag", "Value"])
    df.to_csv(r"E:\exif_metadata_project/exif_metadata_report.csv", index=False)
    print("✅ Report generated: exif_metadata_report.csv")

# Example usage
images_folder = r"E:\exif_metadata_project\images"
process_images(images_folder)