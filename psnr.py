"""
Copyright (C) 2018  Axel Davy

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import numpy as np
import os
import os.path
import fnmatch
import argparse
import imageio
import tifffile
from skimage.measure.simple_metrics import compare_psnr

def get_files_pattern(d, pattern):
    files = os.listdir(d)
    files = fnmatch.filter(files, pattern)
    return sorted(files)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('imgdir', help='Directory of denoised images (png, tiff)')
    parser.add_argument('refdir', help='Directory of reference images (png, tiff), should only contain these images')
    args = parser.parse_args()
    files = get_files_pattern(args.refdir, '*')
    psnr = 0.
    acc = np.zeros([1], np.float64)
    acc2 = np.zeros([1], np.float64)
    for f in files:
        ref = imageio.imread(args.refdir + '/' + f)
        if os.path.exists(args.imgdir + '/' + f):
            img = imageio.imread(args.imgdir + '/' + f)
        elif os.path.exists(args.imgdir + '/' + f[:-3] + 'tiff'):
            img = tifffile.imread(args.imgdir + '/' + f[:-3] + 'tiff')
        else:
            continue
        ref = np.squeeze(ref)
        img = np.squeeze(img)
        psnr_img = compare_psnr(ref, img, data_range=255)
        print(f, psnr_img)
        psnr += psnr_img

        ref = np.asarray(ref, dtype=np.float64)
        img = np.asarray(img, dtype=np.float64)
        acc += np.sum(np.square(ref - img))
        acc2 += ref.size
    print('Average PSNR: ', psnr/len(files))
    # The PSNR below is the correct one for video
    print('PSNR on the sequence: ', 10 * np.log10((255. ** 2) / (acc[0]/acc2[0])))
