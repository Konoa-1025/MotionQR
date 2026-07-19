from generators.qrGenerator import generate_qr_matrix
from generators.qrRender import render_qr


matrix, version = generate_qr_matrix("アライメント　")

print(f"QR Version: {version}")
print(f"Matrix size: {len(matrix)}")

image = render_qr(
    matrix,
    version,
    module_size=20,
    black_ratio=0.1,
    white_ratio=0.1,
)

image.save("output/motion_qr.png")