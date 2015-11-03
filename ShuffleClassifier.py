# -*- coding: utf-8 -*-

from PIL import Image           # PIL module. Only if you use the PIL library.
import operator
import time
import imagehash
import config

class ShuffleClassifier:
    def __init__(self):
        self.filepath = ''
        #config.BlockSize = 38
        #self.ClassNum = 4
        self.ref_images = []
        self.ref_names = []
        self.ref_filenames = []
        self.ref_types = []
        self.blocks = []
        self.results = []
        self.results_type = []
        self.results_filenames = []
        self.mask = Image.open(config.pathMask)
        
    def hamming_dist(self, hash1, hash2):
        return hash1 - hash2
        
    def get_hash(self, image):
        return imagehash.dhash(image, hash_size=16)
                
    def load_image(self, filepath):
        pilImage = Image.open( filepath )
        self.filepath = filepath
        #self.image = pilImage.resize((config.BlockSize * 6, config.BlockSize * 6), Image.ANTIALIAS).convert("L")
        self.image = pilImage.resize((config.BlockSize * 6, config.BlockSize * 6)).convert('RGBA')
        self.get_blocks()
        
    def load_image2(self, pilImage):
        #self.image = pilImage.resize((config.BlockSize * 6, config.BlockSize * 6), Image.ANTIALIAS).convert("L")
        self.image = pilImage.resize((config.BlockSize * 6, config.BlockSize * 6)).convert('RGBA')
        self.get_blocks()
        
    def get_blocks(self):
        self.blocks = []
        for n in range(0, 36):
            i = n / 6
            j = n - i * 6
            box = (config.BlockSize * i, config.BlockSize * j, config.BlockSize * i + config.BlockSize, config.BlockSize * j + config.BlockSize)
            block = self.image.crop(box)
            self.blocks.append(self.mask_block(block))
            
    def save_blocks(self):
        for n in range(0, 36):
            self.save_block(n)
            
    def save_block(self,n, path=False):
        i = n / 6
        j = n - i * 6
        box = (config.BlockSize * i, config.BlockSize * j, config.BlockSize * i + config.BlockSize, config.BlockSize * j + config.BlockSize)
        block = self.image.crop(box)
        if path != False:
            block.save(path, 'PNG')            
        else:
            block.save('outputs//' + str(int(time.time())) + str(n) + '.png', 'PNG')
            
    def get_block_distances(self):
        # Abandoned
        self.distances = []
        for t in range(0, 36*36):
            n = t / 36
            m = t - n * 36
            block1 = self.blocks[n]
            block2 = self.blocks[m]
            self.distances.append(self.hamming_dist(self.get_hash(block1),self.get_hash(block2)))
            
    def mask_block(self, block):
        #im = pilImage.resize((config.BlockSize, config.BlockSize), Image.ANTIALIAS).convert("L")
        tmp = block.resize((config.BlockSize, config.BlockSize)).convert('RGBA')
        
        im = self.mask.copy()
        #print self.mask, tmp
        im.paste(tmp, (0,0,config.BlockSize,config.BlockSize), self.mask)        
        return im
        
    def add_reference(self, filename, refname, reftype='false', folderpath='icons/'):
        filepath = folderpath + filename + '.png'
        # load image
        im = self.mask_block(Image.open( filepath))
        # add to ref.
        self.ref_images.append(im)
        self.ref_names.append(refname)
        self.ref_types.append(reftype)
        self.ref_filenames.append(filename)
        
    def clear_references(self):
        self.ref_filenames = []
        self.ref_images = []
        self.ref_names = []
        self.ref_types = []        
        
    def get_dist(self, block1, block2):
        return self.hamming_dist(self.get_hash(block1), self.get_hash(block2))
        
    def get_dist_rgb(self, block1, block2):
        #self.hamming_dist(self.get_hash(block1), self.get_hash(block2))
        r1,g1,b1,a1 = block1.split()
        r2,g2,b2,a2 = block2.split()
        
        dist = 0
        dist += self.hamming_dist(self.get_hash(r1), self.get_hash(r2))
        dist += self.hamming_dist(self.get_hash(g1), self.get_hash(g2))
        dist += self.hamming_dist(self.get_hash(b1), self.get_hash(b2))
        
        return dist
        
    # Rotating the block
    def get_ref_dist(self, block, ref):
        distances = []
        for r in range(-9, 9, 3):
            rotblock = block.rotate(r) 
            distances.append(self.get_dist(rotblock, ref))
            #distances.append(self.get_dist_rgb(rotblock, ref))
        min_index, min_value = min(enumerate(distances), key=operator.itemgetter(1))
        return min_value
        
    def classify(self):
        self.results = []
        self.results_type = []
        self.results_filenames = []
        for n in range(0, 36):
            block = self.blocks[n]
            distances = []
            for m in range(0, len(self.ref_images)):
                distances.append(self.get_ref_dist(block, self.ref_images[m]))
            min_index, min_value = min(enumerate(distances), key=operator.itemgetter(1))
            self.results.append(self.ref_names[min_index])
            self.results_type.append(self.ref_types[min_index])
            self.results_filenames.append(self.ref_filenames[min_index])

    def label_metal(self):
        
        if config.varMetalTimer == 5:
            label = "Metal"
        else:
            label = "Metal_" + str(config.varMetalTimer)
        return label
    
    def write_board(self, stagename,boardpath):
        file = open(boardpath, 'w')
        file.write('STAGE '+stagename+'\n')

        for j in range(0, 6):
            file.write('ROW_'+str(j+1)+' ')
            for i in range(0, 6):
                n = j + i * 6
                label = self.results[n]
                
                if label == "Metal":
                    label = self.label_metal()
                
                file.write(label)
                if i < 5: 
                    file.write(',')    
                else:
                    file.write('\n') 
                
            file.write('FROW_'+str(j+1)+' ')
            for i in range(0, 6):
                n = j + i * 6
                label = self.results_type[n]
                file.write(label)
                if i < 5: 
                    file.write(',')    
                else:
                    file.write('\n') 

        file.close()
    
    def classify_filepath(self,filepath, stagename='SP_275', boardpath='~/Shuffle-Move/config/boards/board.txt'):
        self.load_image(filepath)
        self.classify()
        self.write_board(stagename,boardpath)