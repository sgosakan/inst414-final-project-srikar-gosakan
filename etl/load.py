import os
import shutil

os.makedirs('data/processed', exist_ok=True)

def move_transformed_data():
    """
    Move transformed data to the processed directory.
    """
    source_dir = 'data/transformed'
    dest_dir = 'data/processed'
    
    for file_name in os.listdir(source_dir):
        full_file_name = os.path.join(source_dir, file_name)
        if os.path.isfile(full_file_name):
            shutil.move(full_file_name, dest_dir)

def main():
    move_transformed_data()

if __name__ == "__main__":
    main()
