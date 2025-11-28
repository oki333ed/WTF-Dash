import os
import shutil
from PIL import Image

ROOT = os.getcwd()
ORG_DIR = os.path.join(ROOT, "org")

os.makedirs(ORG_DIR, exist_ok=True)

def scale_image(input_path, output_path, factor):
    img = Image.open(input_path)
    w, h = img.size
    img = img.resize((max(1, w // factor), max(1, h // factor)), Image.LANCZOS)
    img.save(output_path)

for root, dirs, files in os.walk(ROOT):
    if ORG_DIR in root:
        continue

    for file in files:

        if file.lower() == "pack.png":
            continue

        if not file.lower().endswith(".png"):
            continue

        fname = file[:-4]
        if fname.endswith("-hd") or fname.endswith("-uhd"):
            continue

        full_path = os.path.join(root, file)

        rel = os.path.relpath(root, ROOT)
        org_target_dir = os.path.join(ORG_DIR, rel)
        os.makedirs(org_target_dir, exist_ok=True)

        shutil.copy2(full_path, os.path.join(org_target_dir, file))

        uhd_path = os.path.join(root, f"{fname}-uhd.png")
        shutil.copy2(full_path, uhd_path)

        hd_path = os.path.join(root, f"{fname}-hd.png")
        scale_image(full_path, hd_path, factor=2)

        normal_path = os.path.join(root, f"{fname}.png")
        scale_image(full_path, normal_path, factor=4)