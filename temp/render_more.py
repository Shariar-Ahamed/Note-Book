import pymupdf

doc = pymupdf.open('PDF/Chapter-05-Loops-Iteration.pdf')
# Render Page 2
doc[1].get_pixmap(dpi=150).save('temp/page2_preview.png')
# Render Page 34 (last page)
doc[-1].get_pixmap(dpi=150).save('temp/page34_preview.png')
print("Page 2 and Page 34 saved as preview images")
