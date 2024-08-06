def load_texts(file_path: str) -> list:
    with open(file_path) as f:
        return f.readlines()
