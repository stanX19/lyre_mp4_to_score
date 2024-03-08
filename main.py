from srcs import save_video_as_nightly, Path


def main():
    save_video_as_nightly(Path.data)
    input("press enter to exit")


if __name__ == '__main__':
    main()