import pymupdf

doc = pymupdf.open('PDF/Chapter-05-Loops-Iteration.pdf')
# Render Page 1 to image for verification
page1 = doc[0]
pix1 = page1.get_pixmap(dpi=150)
pix1.save('temp/page1_preview.png')
print("Page 1 saved as temp/page1_preview.png")
