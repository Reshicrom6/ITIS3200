import os
import json
import hashlib

def hash_file(filepath):
    hash_obj = hashlib.sha256()
    with open(filepath, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b''):
            hash_obj.update(chunk)
    return hash_obj.hexdigest()

def traverse_directory(directory):
    hashes = {}
    for root, _, files in os.walk(directory):
        for file in files:
            filepath = os.path.join(root, file)
            rel_path = os.path.relpath(filepath, directory)
            hashes[rel_path] = hash_file(filepath)
    return hashes

def generate_table(directory):
    hashes = traverse_directory(directory)
    with open('hash_table.json', 'w') as f:
        json.dump(hashes, f, indent=4)
    print("Hash table generated")

def validate_hash(directory):
    try:
        with open('hash_table.json', 'r') as f:
            stored_hashes = json.load(f)
    except FileNotFoundError:
        print("Hash table file not found.")
        return

    current_hashes = traverse_directory(directory)
    
    stored_paths = set(stored_hashes.keys())
    current_paths = set(current_hashes.keys())
    
    deleted = stored_paths - current_paths
    for d in deleted:
        print(f"{d} has been deleted")
    

    added = current_paths - stored_paths
    for a in added:
        print(f"{a} is a new file")
    
    common = stored_paths & current_paths
    for path in common:
        if stored_hashes[path] == current_hashes[path]:
            print(f"{path} hash is valid")
        else:
            print(f"{path} hash is invalid")

def main():
    print("1 for generating a new hash table")
    print("2 for verifying hashes")
    choice = input("Enter your choice: ").strip()
    
    if choice == '1':
        directory = input("Enter directory path: ").strip()
        generate_table(directory)
    elif choice == '2':
        directory = input("Enter directory path: ").strip()
        validate_hash(directory)
    else:
        print("Invalid choice")

if __name__ == "__main__":
    main()