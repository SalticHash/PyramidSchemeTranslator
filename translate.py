import fitz

donor_doc = fitz.open("test_bin/qr_donor_poster.pdf")
pg = donor_doc[0]
translated_doc = fitz.open("test_bin/translation_base2.pdf")

qr_rect = None
qr_bytes = None
for img in pg.get_images(full=True):
    name = img[7]
    if len(name) != 40 or not name.startswith("FormXob."): continue
    qr_rect = pg.get_image_bbox(img)
    
    xref = img[0]
    img_dict = donor_doc.extract_image(xref)
    qr_bytes = img_dict["image"]
    break

translated_doc[0].insert_image(qr_rect, stream=qr_bytes)
translated_doc.save("test_bin/translated_poster.pdf")

# QR png format:
# FormXob._32_charachter_hash_of_qr_code__.png
