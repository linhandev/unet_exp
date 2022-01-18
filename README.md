# unet_exp
hl进展

# 数据集
- msd
链接: https://pan.baidu.com/s/13QyioAcNbHCk7QpRJ0B4pA 提取码: a9g2
--来自百度网盘超级会员v6的分享

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
git clone https://github.com/MIC-DKFZ/nnUNet.git
cd nnUNet
pip install -e .
pip install --upgrade git+https://github.com/FabianIsensee/hiddenlayer.git@more_plotted_details#egg=hiddenlayer
pip install matplotlib

# 设置环境变量
data_dir=/home/lin/Desktop/data/nnunet
export nnUNet_raw_data_base=${data_dir}
export nnUNet_preprocessed=${data_dir}/nnUNet_preprocessed
export RESULTS_FOLDER=${data_dir}/RESULTS_FOLDER

echo  nnUNet_raw_data_base: ${nnUNet_raw_data_base}
echo  nnUNet_preprocessed: ${nnUNet_preprocessed}
echo  RESULTS_FOLDER: ${RESULTS_FOLDER}
```

# nnunet预处理

nnUNet_convert_decathlon_task -i /home/lin/Desktop/msd # 4d序列会拆分成3d

nnUNet_plan_and_preprocess -t 6 -tl 2 -tf 1 --verify_dataset_integrity
