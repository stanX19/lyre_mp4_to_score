import easygui

video_path = easygui.fileopenbox("select designated 720p mp4 file", "Select Video",
                                        "D:\\Downloads\\", filetypes=["*.mp4"], multiple=True)