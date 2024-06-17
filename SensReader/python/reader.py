import argparse
import os, sys

from SensorData import SensorData
from glob import glob
from tqdm import tqdm

def main(opt):
  if not os.path.exists(opt.output_path):
    os.makedirs(opt.output_path)
  # load the data
  sys.stdout.write('loading %s...' % opt.filename)
  sd = SensorData(opt.filename)
  sys.stdout.write('loaded!\n')
  if opt.export_depth_images:
    sd.export_depth_images(os.path.join(opt.output_path, 'depth'))
  if opt.export_color_images:
    sd.export_color_images(os.path.join(opt.output_path, 'color'))
  if opt.export_poses:
    sd.export_poses(os.path.join(opt.output_path, 'pose'))
  if opt.export_intrinsics:
    sd.export_intrinsics(os.path.join(opt.output_path, 'intrinsic'))


if __name__ == '__main__':
  data_dir = '/home/du/Proj/Dataset/ScanNet/scans'
  data_list = sorted(glob(f'{data_dir}/scene*'))
  # scene_list = [os.path.basename(d) for d in data_list]
  scene_list = ['scene0015_00', 'scene0025_00', 'scene0414_00']
  for scene_name in tqdm(scene_list, desc='extracting data'):
    print(f'---proprecess scene: {scene_name}---')
    # params 
    parser = argparse.ArgumentParser()
    # data paths
    parser.add_argument('--filename', default=f'{data_dir}/{scene_name}/{scene_name}.sens', help='path to sens file to read')
    parser.add_argument('--output_path', default=f'{data_dir}/{scene_name}/')
    parser.add_argument('--export_depth_images', dest='export_depth_images', action='store_true')
    parser.add_argument('--export_color_images', dest='export_color_images', action='store_true')
    parser.add_argument('--export_poses', dest='export_poses', action='store_true')
    parser.add_argument('--export_intrinsics', dest='export_intrinsics', action='store_true')
    parser.set_defaults(export_depth_images=True, export_color_images=True, export_poses=True, export_intrinsics=True)

    opt = parser.parse_args()
    print(opt)
    main(opt)

    # 解压 instance&semantic
    instance_file=f'{data_dir}/{scene_name}/{scene_name}_2d-instance-filt.zip'
    os.system(f'unzip -o -q {instance_file} -d {opt.output_path}')

    semantic_file=f'{data_dir}/{scene_name}/{scene_name}_2d-label-filt.zip'
    os.system(f'unzip -o -q {semantic_file} -d {opt.output_path}')
    
    