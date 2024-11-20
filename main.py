from srcs import save_video_as_nightly, Path, analyser


def main():
    save_video_as_nightly(Path.data)
    # analyser.main()
    input("press enter to exit")


if __name__ == '__main__':
    main()