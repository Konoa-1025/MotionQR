import qrcode


def generate_qr_matrix(
    text: str,
) -> tuple[list[list[bool]], int]:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=1,
        border=0,
    )

    qr.add_data(text)
    qr.make(fit=True)

    return qr.get_matrix(), qr.version