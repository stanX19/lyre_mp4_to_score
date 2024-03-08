import os

join = os.path.join
root = os.path.abspath(join(os.path.dirname(__file__), ".."))
assets = join(root, "assets")
data = join(root, "data")
templates = join(assets, "templates")
first_note = join(templates, "first_note.png")