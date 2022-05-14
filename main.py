from image_processing import *


def main():
    with Image.open('yoda.jpeg') as img:
        to_gray_enchance_constarst(img, True)
        img.show()


if __name__ == '__main__':
    main()
