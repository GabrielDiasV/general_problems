from PIL import Image, ImageChops, ImageDraw
import random
import os


def generate_random_key(width, height) -> Image:
    image = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(image)

    for _ in range(width * height):
        draw.point((random.randint(0, width), random.randint(0, height)), fill="black")

    image.save(os.path.join("pictures", "key.png"))
    return image.convert("1")


def encrypt(original: Image, key: Image) -> Image:
    encrypted = ImageChops.logical_xor(original, key)
    encrypted.save(os.path.join("pictures", "encrypted.png"))
    return encrypted


def decrypt(encrypted: Image, key: Image) -> Image:
    decrypted = ImageChops.logical_xor(encrypted, key)
    decrypted.save(os.path.join("pictures", "decrypted.png"))
    return decrypted


if __name__ == "__main__":
    original = Image.open(os.path.join("pictures", "original.png")).convert("1")
    key = generate_random_key(original.width, original.height)
    encrypted = encrypt(original, key)
    decrypted = decrypt(encrypted, key)
