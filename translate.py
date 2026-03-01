import fitz


donor_doc = fitz.open("test_bin/FlavorDono.pdf")
translated_base = fitz.open("test_bin/FlavorTrad.pdf")
translated_doc = fitz.open("test_bin/FlavorTrad.pdf")

poster_count = len(donor_doc)

for poster_i in range(poster_count):
    pg = donor_doc[poster_i]
    if poster_i > 0:
        translated_doc.insert_pdf(translated_base, to_page=0, start_at=poster_i)
    
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

    translated_doc[poster_i].insert_image(qr_rect, stream=qr_bytes)
translated_doc.save("test_bin/translated_multi_poster.pdf")

# QR png format:
# FormXob._32_charachter_hash_of_qr_code__.png
