import io
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4


def prepare_canva(canva, font_size=10):
    canva.setFont('FreeSans', font_size)
    canva.setTitle('Shoping cart')


def print_title(canva, page, pos='up'):
    prepare_canva(canva, 16)
    if pos == 'up':
        canva.drawString(
            150, 820, "Список покупок c сайта foodgramm.virtual-it.ru")
        canva.line(0, 815, 595, 815)
    else:
        canva.line(0, 40, 595, 40)
        canva.drawString(
            150, 25,
            'Список покупок c сайта foodgramm.virtual-it.ru')
        prepare_canva(canva, 8)
        canva.drawString(
            50, 10, f' страница: {page}')


def make_pdf_file(text):
    zero_y = 820
    rowHeight = 14
    page = 1

    buffer = io.BytesIO()
    pdfmetrics.registerFont(
        TTFont('FreeSans', settings.BASE_DIR / 'FreeSans.ttf'))
    canva = canvas.Canvas(buffer, pagesize=A4)

    print_title(canva, page, 'up')

    y = 20
    prepare_canva(canva)
    for line in text:
        y += rowHeight
        if y > 770:
            print_title(canva, page, 'down')
            canva.showPage()
            page += 1
            print_title(canva, page, 'up')
            prepare_canva(canva)
            y = 20

        canva.drawString(10, zero_y - y, line)

    print_title(canva, page, 'down')
    canva.showPage()
    canva.save()
    buffer.seek(0)
    return buffer


if __name__ == '__main__':
    pass
