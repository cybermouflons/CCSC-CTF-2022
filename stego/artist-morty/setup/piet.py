from PIL import Image

flag = open("flag.txt", "r").read()

def prime_factors(n):
    i = 2
    factors = []
    while i * i <= n:
        if n % i:
            i += 1
        else:
            n //= i
            factors.append(i)
    if n > 1:
        factors.append(n)
    return factors

print([prime_factors(ord(f)) for f in flag])

original_im = Image.open(r"./original.png") 
original_pixel_map = original_im.load()


stego_im = Image.new("RGB", (original_im.size[0], original_im.size[1]), (255, 255, 255))
stego_pixel_map = stego_im.load()

print(stego_pixel_map[0, 2])