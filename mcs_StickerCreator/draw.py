from ezdxf.layouts import Modelspace
from reportlab.pdfgen.canvas import Canvas
from reportlab.lib.pagesizes import A3

def draw_hline_ref_points(
        canvas: Canvas,
        x1_cen: float, x2_cen: float, y_cen: float,
        radius: float, skip: bool = False) -> None:
    if skip:
        return
    canvas.setFillColorCMYK(0.07, 0.03, 0.0, 0.13)
    canvas.circle(x_cen=x1_cen, y_cen=y_cen, r=radius, fill=1)
    canvas.circle(x_cen=x2_cen, y_cen=y_cen, r=radius, fill=1)


def draw_hline_ref_points_dxf(
        modelspace: Modelspace,
        x1_cen: float, x2_cen: float, y_cen: float,
        radius: float, skip: bool = False) -> None:
    if skip:
        return
    modelspace.add_circle(
        center=(x1_cen, y_cen),
        radius=radius,
    )
    modelspace.add_circle(
        center=(x2_cen, y_cen),
        radius=radius,
    )

