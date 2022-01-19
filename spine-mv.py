import os
import os.path as osp
import shutil

from tqdm import tqdm

scan_base = "/home/lin/Desktop/data/CTSpine1K/data/"
scan_dirs = ["colon", "COVID-19", "HNSCC-3DCT-RT_neck", "liver", "verse"]

label_base = "/home/lin/Desktop/data/CTSpine1K/label_new/"
label_dirs = [
    ["trainset/gt/", "imagesTr", "labelsTr"],
    ["test_private/gt", "imagesTs", "labelsTs"],
    ["test_public/gt", "imagesVal", "labelsVal"],
]
msd_base = "/home/lin/Desktop/data/CTSpine1K/msd/"
scans = {}
labels = []

# 1. get scan name and path map
for scan_dir in scan_dirs:
    scan_dir = osp.join(scan_base, scan_dir)
    for scan in os.listdir(scan_dir):
        scans[scan[: -len(".nii.gz")]] = osp.join(scan_dir, scan)
# print(scans)


for label_dir, scan_msd_fdr, label_msd_fdr in label_dirs:
    label_dir = osp.join(label_base, label_dir)
    print(label_dir)
    label_msd_dir = osp.join(msd_base, label_msd_fdr)
    scan_msd_dir = osp.join(msd_base, scan_msd_fdr)
    for label in tqdm(os.listdir(label_dir)):
        patient = label[: -len("_seg.nii.gz")]
        scan_file = scans[patient]
        label_file = osp.join(label_dir, label)
        print(scan_file, label_file)
        shutil.copy(scan_file, scan_msd_dir)
        shutil.copy(label_file, label_msd_dir)
        # input("here")
