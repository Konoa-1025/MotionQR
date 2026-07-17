import qrcode


def create_qr(text: str, output_path: str = "qr1.png") -> None:
    if not text.strip():
        raise ValueError("QRコードに入れる文字が空です")

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=4,
    )

    qr.add_data(text)
    qr.make(fit=True)

    image = qr.make_image(
        fill_color="black",
        back_color="white",
    )

    image.save(output_path)


if __name__ == "__main__":
    text = input("QRコードに入れる文字: ")
    create_qr(text)
    print("qr.pngを生成しました")