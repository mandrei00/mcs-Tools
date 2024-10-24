import ezdxf
from ezdxf import select

from reportlab.lib.pagesizes import A3
from reportlab.lib.units import mm, cm
from reportlab.pdfgen.canvas import Canvas

from new_proj.draw import draw_sticker, draw_center_text, draw_serial, draw_ref_circle, draw_lot
from read_template import read_xl

# sticker size
WIDTH_STICKER = 4.4 * cm
HEIGHT_STICKER = 2.645 * cm

# size of reference point
DIAMETER_POINT = 7 * mm

# indent sizes
X_DISTANCE = 2 * mm
Y_DISTANCE = 3 * mm

# size indent
X_PAD = 14 * mm
Y_PAD = 3 * mm


def main(max_number_sticker, path_to_stick, path_to_counter, path_to_save_pdf=None):
    # read counter dxf
    doc = ezdxf.readfile(path_to_counter)
    msp = doc.modelspace()

    # create new dxf
    new_doc = ezdxf.new("R2007")
    new_msp = new_doc.modelspace()

    window = select.Window(
        (float("-inf"), float("-inf")),
        (float("inf"), float("inf")), )
    entities = select.bbox_outside(window, msp.entity_space.entities)

    # pdf
    c = Canvas(path_to_save_pdf, pagesize=A3)

    x, y = X_PAD, Y_PAD
    number_sticker = 0
    number_row = 1
    while (A3[1] - y) > HEIGHT_STICKER:

        if number_sticker == max_number_sticker:
            break

        if WIDTH_STICKER > (A3[0] - x):
            x = X_PAD
            y += Y_DISTANCE + HEIGHT_STICKER
            number_row += 1
            continue

        draw_sticker(
            plot=c, x=x, y=y,
            path_to_stick=path_to_stick, height=HEIGHT_STICKER, width=WIDTH_STICKER
        )

        text = "MCScap PROFESSIONAL, L\nMod: 15E-03M25\nmks.ru"

        draw_center_text(
            plot=c, x=x, y=y + 22 * mm, text=text, max_width=WIDTH_STICKER
        )

        draw_lot(
            plot=c, x=x, y=y, lot="123443"
        )

        for entity in entities:
            cp_entity = entity.copy()
            cp_entity.translate(x / mm, y / mm, 0)
            new_msp.add_foreign_entity(cp_entity)

        x += X_DISTANCE + WIDTH_STICKER
        number_sticker += 1

    # down left circle in pdf
    draw_ref_circle(
        plot=c,
        x_cen=X_DISTANCE + DIAMETER_POINT / 2, y_cen=2*Y_PAD + DIAMETER_POINT / 2,
        radius=DIAMETER_POINT / 2
    )
    # down left circle in dxf
    new_msp.add_circle(
        ((X_DISTANCE + DIAMETER_POINT / 2) / mm, (2*Y_PAD + DIAMETER_POINT / 2) / mm),
        DIAMETER_POINT / 2 / mm
    )

    # down right circle in pdf
    draw_ref_circle(
        plot=c,
        x_cen=A3[0] - 2 * mm - DIAMETER_POINT / 2,
        y_cen=2*Y_PAD + DIAMETER_POINT / 2,
        radius=DIAMETER_POINT / 2
    )
    # down right circle in dxf
    new_msp.add_circle(
        ((A3[0] - 2 * mm - DIAMETER_POINT / 2) / mm, (2 * Y_PAD + DIAMETER_POINT / 2) / mm),
        DIAMETER_POINT / 2 / mm
    )

    if number_row > 1:
        # up left circle in pdf
        draw_ref_circle(
            plot=c,
            x_cen=X_DISTANCE + DIAMETER_POINT / 2,
            y_cen=number_row * Y_PAD + HEIGHT_STICKER * (number_row - 1) + X_PAD,
            radius=DIAMETER_POINT / 2
        )
        # up left circle in dxf
        new_msp.add_circle(
            ((X_DISTANCE + DIAMETER_POINT / 2) / mm, (number_row * Y_PAD + HEIGHT_STICKER * (number_row - 1) + X_PAD) / mm),
            DIAMETER_POINT / 2 / mm
        )

        # up right circle in pdf
        draw_ref_circle(
            plot=c,
            x_cen=A3[0] - 2 * mm - DIAMETER_POINT / 2,
            y_cen=number_row * Y_PAD + HEIGHT_STICKER * (number_row - 1) + X_PAD,
            radius=DIAMETER_POINT / 2,
        )
        # up right circle in dxf
        new_msp.add_circle(
            ((A3[0] - 2 * mm - DIAMETER_POINT / 2) / mm,
             (number_row * Y_PAD + HEIGHT_STICKER * (number_row - 1) + X_PAD) / mm),
            DIAMETER_POINT / 2 / mm
        )

    # save pdf with stickers
    c.save()
    # save dxf file
    new_doc.saveas("output.dxf")


if __name__ == "__main__":
    main(
        max_number_sticker=24, path_to_save_pdf="output.pdf",
        path_to_stick="sticker.jpg",
        path_to_counter="new.dxf"
    )
    # # read_xl(path_to_xl="input/template_sn.xlsx")
