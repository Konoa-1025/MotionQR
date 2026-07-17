from PIL import Image, ImageDraw
from qrcode.util import pattern_position


def is_finder_area(
    row: int,
    col: int,
    matrix_size: int,
) -> bool:
    # ファインダパターン7マス＋白い分離領域1マス
    area_size = 8

    # 左上
    if row < area_size and col < area_size:
        return True

    # 右上
    if row < area_size and col >= matrix_size - area_size:
        return True

    # 左下
    if row >= matrix_size - area_size and col < area_size:
        return True

    return False


def is_alignment_area(
    row: int,
    col: int,
    version: int,
    matrix_size: int,
) -> bool:
    # Version 1にはアライメントパターンがない
    if version == 1:
        return False

    centers = pattern_position(version)

    for center_row in centers:
        for center_col in centers:
            # ファインダパターンと重なる候補は除外
            if is_finder_area(
                center_row,
                center_col,
                matrix_size,
            ):
                continue

            # アライメントパターンは中心から上下左右2マスの5×5
            if (
                abs(row - center_row) <= 2
                and abs(col - center_col) <= 2
            ):
                return True

    return False


def render_qr(
    matrix: list[list[bool]],
    version: int,
    module_size: int = 20,
    black_ratio: float = 0.25,
    white_ratio: float = 0.25,
) -> Image.Image:
    matrix_size = len(matrix)

    image = Image.new(
        "RGBA",
        (
            matrix_size * module_size,
            matrix_size * module_size,
        ),
        (255, 255, 255, 0),
    )

    draw = ImageDraw.Draw(image)

    for row_index, row in enumerate(matrix):
        for column_index, is_black in enumerate(row):
            protected = (
                is_finder_area(
                    row_index,
                    column_index,
                    matrix_size,
                )
                or is_alignment_area(
                    row_index,
                    column_index,
                    version,
                    matrix_size,
                )
            )

            if protected:
                ratio = 1.0
            elif is_black:
                ratio = black_ratio
            else:
                ratio = white_ratio

            size = max(1, round(module_size * ratio))
            offset = (module_size - size) // 2

            x1 = column_index * module_size + offset
            y1 = row_index * module_size + offset
            x2 = x1 + size - 1
            y2 = y1 + size - 1

            color = (
                (0, 0, 0, 255)
                if is_black
                else (255, 255, 255, 255)
            )

            draw.rectangle(
                (x1, y1, x2, y2),
                fill=color,
            )

    return image