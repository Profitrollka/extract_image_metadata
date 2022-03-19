#!/opt/homebrew/bin/python3

import argparse
import csv
from exif import Image

tags = ['make','model','datetime','datetime_digitized','datetime_original','lens_make','lens_model','lens_specification']


def check_exif_tags(img_path):
        """
        Function returns list of tags that for wich it possible to receive meta data  
        :param img_path: image file path
        :return tags_list: list of tags for image
        """
        with open(img_path, 'rb') as f:
                img = Image(f)

        if img.has_exif:
                print(f"File contains EXIF (version {img.exif_version}) information.")
                tags_list = dir(img)
                print(tags_list)
                return tags_list



def get_meta_data(img_path, output_file=None, f_mode='w'):
        """
        Function extract meta data from image
        :param img_path: mage file path
        :param output_file: csv file name for saving data, defaul value None
        :param mode: 'a' - append data to the end of exciting file, 'w' for create or owerwrite data in file   
        :return saving meta data to file or printing it
        """
        print(f'Getting meta data from {img_path}')

        meta_data_dict = {}
        meta_data_values = []

        with open(img_path, 'rb') as f:
                img = Image(f)
                if img.has_exif:
                        print(f"File contains EXIF information.")
                        if output_file:                
                                print(f'Saving meta data to file {output_file}')
                                with open(output_file, mode=f_mode) as f:
                                        writer = csv.writer(f)
                                        writer.writerow(tags)
                                        for tag in tags:
                                                if tag in dir(img):
                                                        meta_data_values.append(img.get(tag))
                                        writer.writerow(meta_data_values)
                        else:
                                for tag in tags:
                                        if tag in dir(img):
                                                meta_data_dict[tag] = img.get(tag)
                                print(meta_data_dict)
                else:
                        print(f"File doesn't contains EXIF information.")           


def main():
        parser = argparse.ArgumentParser()
        parser.add_argument('img', help='name of image file')
        parser.add_argument('-o', '--output_file', help='file for savimng meta data')
        parser.add_argument('-m', '--mode', help='"a" for append data to the end of the file, "w" for owerwrite all data in file')
        args = parser.parse_args()
        if args.img:
                get_meta_data(args.img, args.output_file, args.mode)
        else:
                print(parser.usage)

if __name__ == '__main__':
        main()

