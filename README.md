# unet_exp
在paddlecv-sig fork了nnunet，单进程用for替换starmap避免挂住，加入tqdm显示进度，并对代码做了一些注释

https://github.com/PaddleCV-SIG/nnUNet

# 数据集
在共享文件夹里

- msd 10个task
- msd nnunet 预处理
- CT spine 1k

# 环境
```shell
# 装torch
conda create -n torch python=3.9
conda activate torch
conda update -n base -c defaults conda
nvcc --version
conda install pytorch torchvision torchaudio cpuonly -c pytorch

# 装nnunet
pip install -r requirements.txt
git clone https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e .
pip install --upgrade git+https://ghproxy.com/https://github.com/FabianIsensee/hiddenlayer.git@more_plotted_details#egg=hiddenlayer
pip install matplotlib
```

# 设置环境变量
```shell
data_dir=/home/lin/Desktop/data/nnunet/CTSpine1K
# data_dir=/home/work/prep
export nnUNet_raw_data_base=${data_dir}
export nnUNet_preprocessed=${data_dir}/nnUNet_preprocessed
export RESULTS_FOLDER=${data_dir}/RESULTS_FOLDER

echo  nnUNet_raw_data_base: ${nnUNet_raw_data_base}
echo  nnUNet_preprocessed: ${nnUNet_preprocessed}
echo  RESULTS_FOLDER: ${RESULTS_FOLDER}

```

# nnunet预处理

```shell
# msd10个任务预处理
# 环境
zip_name=Task04_Hippocampus
task_name=$(python -c "print('Task0'+'${zip_name}'[4:])")
task_num=$(python -c "print('${zip_name}'[4:6])")
nnunet_data_dir=/home/lin/Desktop/data/nnunet/${task_name}
msd_zip_dir=/home/lin/Desktop/msd
wangpan_base=/med_dataset/nnunet/prep

export nnUNet_raw_data_base=${nnunet_data_dir}
export nnUNet_preprocessed=${nnunet_data_dir}/nnUNet_preprocessed
export RESULTS_FOLDER=${nnunet_data_dir}/RESULTS_FOLDER

echo -e '\n\n'
echo zip_name: ${zip_name}
echo task_name: ${task_name}
echo task_num: ${task_num}
echo msd_zip_dir: ${msd_zip_dir}
echo wangpan_base: ${wangpan_base}
echo nnUNet_raw_data_base: ${nnUNet_raw_data_base}
echo nnUNet_preprocessed: ${nnUNet_preprocessed}
echo RESULTS_FOLDER: ${RESULTS_FOLDER}
echo -e '\n\n'
sleep 3

conda activate torch

cd ${msd_zip_dir}
tar -xvf ${zip_name}.tar
pwd
ls
sleep 3

nnUNet_convert_decathlon_task -i ${msd_zip_dir}/${zip_name} # 4d序列会拆分成3d

# rm -rf ${msd_zip_dir}/${zip_name}

xfce4-terminal --hold --title "nnUNet_raw_data/${task_name}" -e "baidupcs u ${nnUNet_raw_data_base}/nnUNet_raw_data/${task_name} ${wangpan_base}/nnUNet_raw_data/"

nnUNet_plan_and_preprocess -t ${task_num} -tl 1 -tf 1 --verify_dataset_integrity

python /home/lin/Desktop/git/seg/unet_exp/covpkl.py ${nnunet_data_dir}

xfce4-terminal --hold --title "nnUNet_cropped_data/${task_name}" -e "baidupcs u ${nnUNet_raw_data_base}/nnUNet_cropped_data/${task_name} ${wangpan_base}/nnUNet_cropped_data/"

xfce4-terminal --hold --title "nnUNet_preprocessed/${task_name}" -e "baidupcs u ${nnUNet_raw_data_base}/nnUNet_preprocessed/${task_name} ${wangpan_base}/nnUNet_preprocessed/"


cd ${nnUNet_raw_data_base}
zip -r nnunet-${task_name}.zip nnUNet_cropped_data/${task_name} nnUNet_preprocessed/${task_name} nnUNet_raw_data/${task_name}

baidupcs u ${nnUNet_raw_data_base}/nnunet-${task_name}.zip ${wangpan_base}/zip/
```

预处理流程
1. 裁剪数据，找到扫描中非0的部分，用bb包起来，把bb里的裁出来。对头部这种目标小的会有用。每个扫描在 nnUNet_cropped_data 下一个 npz，一个pkl。
2. 计算每组扫描和整个数据集的统计信息：median，mean，sd，mn，mx，percentile_99_5，percentile_00_5。写data_properties.pkl和intensityproperties.pkl
3. 生成计划，都是规则，很快也就1s
4. 进行预处理，每次都是从头开始没有断点
