from fitz import open as openPDF, Rect
from io import BytesIO

def translate(donor_bytes: BytesIO, translated_bytes: BytesIO) -> BytesIO:
    donor_doc = openPDF(stream=donor_bytes, filetype="pdf")
    translated_base = openPDF(stream=translated_bytes, filetype="pdf")
    translated_doc = openPDF(stream=translated_bytes, filetype="pdf")

    poster_count = len(donor_doc)
    print(poster_count)
    for poster_i in range(poster_count):
        pg = donor_doc[poster_i]
        if poster_i > 0:
            translated_doc.insert_pdf(translated_base, to_page=0, start_at=poster_i)
            print("Made new page on translated!")
        
        qr_rect: Rect = None
        qr_bytes: BytesIO = None
        for img in pg.get_images(full=True):
            name: str = img[7]
            if len(name) != 40 or not name.startswith("FormXob."): continue
            qr_rect = pg.get_image_bbox(img)
            
            xref: int = img[0]
            img_dict: dict = donor_doc.extract_image(xref)
            qr_bytes = img_dict["image"]
            break

        translated_doc[poster_i].insert_image(qr_rect, stream=qr_bytes)
        print("Added qr to translated")
    
    return translated_doc.tobytes()

# QR png format:
# FormXob._32_charachter_hash_of_qr_code__.png
