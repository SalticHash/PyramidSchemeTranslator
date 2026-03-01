from fitz import open as openPDF, Rect
from io import BytesIO

def translate(donor_bytes: BytesIO, translated_bytes: BytesIO) -> BytesIO | str:
    try:
        donor_doc = openPDF(stream=donor_bytes, filetype="pdf")
        translated_base = openPDF(stream=translated_bytes, filetype="pdf")
        translated_doc = openPDF(stream=translated_bytes, filetype="pdf")
    except:
        return "Couldn't open PDF files! Make sure the files are PDFs!"

    if len(translated_base) != 1:
        return "Translation template should only contain one page!"
    poster_count = len(donor_doc)
    for poster_i in range(poster_count):
        pg = donor_doc[poster_i]
        
        page_h = pg.bound().bottom_right.y
        base_h = translated_base[0].bound().bottom_right.y
        page_w = pg.bound().bottom_right.x
        base_w = translated_base[0].bound().bottom_right.x
        if (abs(page_h - base_h) > 32.0) or (abs(page_w - base_w) > 32.0):
            return "Translation template size mismatch with document, QR codes would result misplaced!"
        if poster_i > 0:
            translated_doc.insert_pdf(translated_base, to_page=0, start_at=poster_i)
        
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
        if qr_bytes == None:
            return "Couldn't find QR code! Make sure that you didn't mix up the PFDs!"

        translated_doc[poster_i].insert_image(qr_rect, stream=qr_bytes)
    
    return translated_doc.tobytes()

# QR png format:
# FormXob._32_charachter_hash_of_qr_code__.png
