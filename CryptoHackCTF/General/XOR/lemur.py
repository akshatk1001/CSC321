from PIL import Image

lemur = Image.open("General/XOR/lemur_ed66878c338e662d3473f0d98eedbd0d.png").convert("RGB")
flag = Image.open("General/XOR/flag_7ae18c704272532658c10b5faad06d74.png").convert("RGB")

result = Image.new("RGB", lemur.size)

for x in range(lemur.width):
    for y in range(lemur.height):
        lemur_pixel = lemur.getpixel((x, y))
        flag_pixel = flag.getpixel((x, y))
        xored_pixel = []

        for a, b in zip(lemur_pixel, flag_pixel):
            xored_pixel.append(a ^ b)

        result.putpixel((x, y), tuple(xored_pixel))

result.save("General/XOR/lemur-xor.png")
