import pymupdf

doc = pymupdf.open('PDF/Chapter-07-Scope-Hoisting.pdf')
doc[0].get_pixmap(dpi=150).save('temp/ch7_p1.png')
doc[1].get_pixmap(dpi=150).save('temp/ch7_p2.png')
doc[-1].get_pixmap(dpi=150).save('temp/ch7_plast.png')
print("Rendered preview pages 1, 2, and last for Chapter 7")
