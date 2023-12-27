import HashCalc as HC
import imagehash
import os
import shutil
from PIL import Image
from tqdm import tqdm


#==================================================================================================
#=================================== CUSTOMIZATION PART ===========================================
#=========================== requires changes based on your case ==================================
#==================================================================================================
#  provide the list of image extensions you want to look at
extension_lst = ['.jpg' '.jpeg', '.png']

# load the hash calculator function. first argument is the hash function used (default=imagehash.dhash), the second
# argument is the hash size for which the default value of 128 is balanced. Smaller values should be used for
# graphs and notes and when want to make sure minute details are not missed when comparing two pictures (like open/closed eyes, etc).
dhash_z_transformed = HC.with_ztransform_preprocess(hash_size=8)

# manually provide the list of folders you want to consider for finding duplicate images
folders = ["Path to Folder 1",
           "Path to Folder 2",
           "Path to Folder 3"]

# the duplicate photos are not deleted but moved here. Do some random checking before deleting.
folder_duplicate = "Path to Duplicate Files Folder"
if not os.path.exists(folder_duplicate):
    os.makedirs(folder_duplicate)

# the corrupt files that cannot be opened or cannot be used to calculate the hash value are moved here. Manually
# check them to see how much they are usuable.
folder_corrupt = "Path to Unreadable Files Folder"
if not os.path.exists(folder_corrupt):
    os.makedirs(folder_corrupt)

#==================================================================================================
#======================================== MAIN PART ===============================================
#============================= you do not need to change this part=================================
#==================================================================================================
uniq_hash = []  # list of hashes for unique images
uniq_images = []  # list of the name of unique images
uniq_images_folder = []  # list of the name of folders each unique image is located in

counter_folder = 0
for folder in folders:
    counter_folder += 1
    print('Folder ' + str(counter_folder) + '/' + str(len(folders)) + ':')

    for image_name in tqdm(os.listdir(folder), position=0, leave=True):
        [image_name_raw, image_extension] = os.path.splitext(image_name)
        if image_extension.lower() in extension_lst:

            path_image = folder + '/' + image_name

            try:
                im = Image.open(path_image)
                img_hash = str(dhash_z_transformed(path_image))
            except:
                shutil.move(path_image, folder_corrupt + '/' + image_name)
                continue

            if img_hash in uniq_hash:
                base_image_name = uniq_images[uniq_hash.index(img_hash)]
                base_image_folder = uniq_images_folder[uniq_hash.index(img_hash)]
                [base_image_name_raw, base_image_extension] = os.path.splitext(base_image_name)
                path_base_image = base_image_folder + '/' + base_image_name
                im_base = Image.open(path_base_image)

                move_from = path_image
                copykount = 1
                while (base_image_name_raw + '-copy-' + str(copykount) + base_image_extension in os.listdir(folder_duplicate)):
                    copykount += 1


                move_to = folder_duplicate + '/' + base_image_name_raw + '-copy-' + str(copykount) + base_image_extension

                if im.size > im_base.size:
                    move_from = path_base_image
                    copykount = 1
                    while (image_name_raw + '-copy-' + str(copykount) + image_extension in os.listdir(folder_duplicate)):
                        copykount += 1

                    move_to = folder_duplicate + '/' + image_name_raw + '-copy-' + str(copykount) + image_extension

                    uniq_images[uniq_hash.index(img_hash)] = image_name
                    uniq_images_folder[uniq_hash.index(img_hash)] = folder

                shutil.move(move_from, move_to)

            else:
                uniq_images.append(image_name)
                uniq_images_folder.append(folder)
                uniq_hash.append(img_hash)
