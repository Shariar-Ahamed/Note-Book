import pymupdf

doc = pymupdf.open('PDF/Chapter-06-Functions.pdf')
doc[0].get_pixmap(dpi=150).save('temp/ch6_p1.png')
doc[1].get_pixmap(dpi=150).save('temp/ch6_p2.png')
doc[-1].get_pixmap(dpi=150).save('temp/ch6_plast.png')
print("Rendered preview pages 1, 2, and last")
