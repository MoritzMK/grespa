from pathlib import Path

if __name__ == "__main__":
    my_file = Path("./venues.json")
    if my_file.exists():
        print("YES")
    else:
        print("NO")
    pass
