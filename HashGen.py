import os
import sys
import hashlib
import gzip
import argparse


class HashGen:
    args = None
    hashFile = None
    inputPath = None
    outputPath = None

    def __init__(self):
        # Set up the accepted arguments
        parser = argparse.ArgumentParser(description='NI Hash Gen Args')
        parser.add_argument('-i', '--input', help='Input Directory', required=True)
        parser.add_argument('-o', '--output', help='Output Directory', required=True)
        parser.add_argument('-v', '--version', help='Module Version', required=True)
        parser.add_argument('-u', '--updater', help='Updater Version', required=False)
        self.args = parser.parse_args()

        # Prepare the output directory
        self.outputPath = os.path.abspath(self.args.output)
        if not os.path.exists(self.outputPath):
            os.mkdir(self.outputPath)
        if not os.path.exists(os.path.join(self.outputPath, self.args.version)):
            os.mkdir(os.path.join(self.outputPath, self.args.version))

        # Check the input directory
        self.inputPath = os.path.abspath(self.args.input)
        if not os.path.exists(self.inputPath):
            print('Error: Input directory "' + self.inputPath + '" does not exist!')
            sys.exit()

        # Create the hash file
        self.hashFile = open(os.path.join(self.outputPath, 'hash.txt'), 'wt')
        self.hashFile.write("V::1\n")
        self.hashFile.write("W::http://nordinvasion.com/mod/" + str(self.args.version) + "/\n")
        self.process_path(self.inputPath)
        self.hashFile.close()
        print('Hash generation complete.')

    def process_path(self, path):
        # Loop through the input directory
        for item in os.listdir(path):
            current_path = os.path.join(path, item)
            relative_path = os.path.relpath(current_path, self.inputPath)
            if os.path.isdir(current_path):
                print('Hashing ' + relative_path)
                self.hashFile.write("F::" + relative_path + "\n")
                self.hashFile.write("X::\n")
                if not os.path.exists(os.path.join(self.outputPath, self.args.version, relative_path)):
                    os.mkdir(os.path.join(self.outputPath, self.args.version, relative_path))
                self.process_path(current_path)
            elif ".revision" not in relative_path:
                print('Hashing ' + relative_path)
                file_hash = (hashlib.sha1(open(current_path, 'rb').read()).hexdigest())
                self.hashFile.write(relative_path + "\n")
                self.hashFile.write(file_hash + "\n")
                # gzip the file
                original_file = open(current_path, 'rb')
                gz_file = gzip.open(os.path.join(self.outputPath, self.args.version, relative_path + '.gz'), 'wb')
                gz_file.writelines(original_file)
                gz_file.close()
                original_file.close()

HashGen()
