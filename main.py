from flood import Flood


def main():
    side_length = 7
    colors = 6
    # side_length = int(input("Enter the side length: "))
    # num_of_colors = int(input("Enter the number of colors: "))
    flood = Flood(side_length, colors)
    flood.start_flood()


if __name__ == '__main__':
    main()
