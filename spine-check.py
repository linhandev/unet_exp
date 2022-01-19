import os
import os.path as osp

scan_base = "/home/lin/Desktop/data/CTSpine1K/data/"
scan_dirs = ["colon", "COVID-19", "HNSCC-3DCT-RT_neck", "liver", "verse"]

label_base = "/home/lin/Desktop/data/CTSpine1K/label_new/"
label_dirs = ["trainset/gt/", "test_public/gt", "test_private/gt"]

scans = []
labels = []

print("dup scans")
for scan_dir in scan_dirs:
    scan_dir = osp.join(scan_base, scan_dir)
    # print(scan_dir)
    for scan in os.listdir(scan_dir):
        scan = scan.replace(".nii.gz", "_seg.nii.gz")
        if scan in scans:
            print(scan)
        scans.append(scan)

print("dup labels")
for label_dir in label_dirs:
    label_dir = osp.join(label_base, label_dir)
    # print(label_dir)
    for label in os.listdir(label_dir):
        if label in labels:
            print(label_dir, label)
        labels.append(label)

print("scans count ", len(scans))
print("label count ", len(labels))

scans = set(scans)
labels = set(labels)
print("scans that don't have label", list(scans - labels))
print("labels that don't have scan", list(labels - scans))

# print("scans that don't have label")
# for scan in scans:
#     if scan not in labels:
#         print(scan)
#
# print("labels that don't have scan")
# for label in labels:
#     if label not in scans:
#         print(label)
