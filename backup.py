import os
import shutil

# Define the directories you want to backup
folders_to_backup = ['test_images', 'test_labels', 'train_images', 'train_labels']

# Create a backup directory
backup_dir = 'backup2_morel_images'
os.makedirs(backup_dir, exist_ok=True)

# Copy each folder to the backup directory
for folder in folders_to_backup:
    if os.path.exists(folder):
        shutil.copytree(folder, os.path.join(backup_dir, folder), dirs_exist_ok=True)
        print(f"Backup of {folder} created in {backup_dir}")
    else:
        print(f"Folder {folder} does not exist.")

print("Backup process completed.")