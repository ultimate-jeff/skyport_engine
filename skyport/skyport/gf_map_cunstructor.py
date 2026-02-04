import os
import json

def main():
    base_dir = input("enter the file dir : ").strip()
    base_dir = os.path.abspath(base_dir)

    count = int(input("how meny file formats to use : "))
    extensions = []

    for i in range(count):
        ext = input("file type : ").strip().lower()
        if not ext.startswith("."):
            ext = "." + ext
        extensions.append(ext)

    print(f"\nScanning directory: {base_dir}")
    print(f"Including file types: {extensions}\n")

    manifest = {}

    for root, _, files in os.walk(base_dir):
        for file in files:
            if any(file.lower().endswith(ext) for ext in extensions):
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, base_dir)
                rel_path = rel_path.replace("\\", "/")  # engine-safe

                manifest[rel_path] = {
                    "type": "d",
                    "value": None
                }

    print("--- GENERATED ASSET MANIFEST (JSON) ---")
    print(json.dumps(manifest, indent=4))
    """
    save = input("\nSave to file? (y/n): ").lower()
    if save == "y":
        out_name = input("Output file name (ex: assets.json): ").strip()
        with open(out_name, "w", encoding="utf-8") as f:
            json.dump(manifest, f, indent=4)
        print(f"Saved to {out_name}")
    """

    #input("\npress any key to exit:")
def gen_map():
    main()

if __name__ == "__main__":
    main()
    confirm = input("Press Enter to exit...")
