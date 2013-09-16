# -*- encoding: utf-8 -*-
"""
django-thumbs by Antonio Melé
http://django.es
"""
from django.db.models import ImageField
from django.db.models.fields.files import ImageFieldFile
from PIL import Image, ImageOps
from django.forms import forms
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str
import cStringIO

OUTPUT_QUALITY = 80
ORIGINAL_WIDTH = 1500


def resize_original(img):

    img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)

    xsize, ysize = image.size
    if xsize > ORIGINAL_WIDTH:
        height = int( ( float(ORIGINAL_WIDTH)/xsize)*ysize )
        image.thumbnail( (ORIGINAL_WIDTH, height), Image.ANTIALIAS )

        io = cStringIO.StringIO()
        image.save(io, 'JPEG', quality=OUTPUT_QUALITY)

        return ContentFile(io.getvalue())
    else:
        return img



def generate_thumb(img, thumb_size, format):
    """
    Generates a thumbnail image and returns a ContentFile object with the thumbnail
    
    Parameters:
    ===========
    img         File object
    
    thumb_size  desired thumbnail size, ie: (200,120)
    
    format      format of the original image ('jpeg','gif','png',...)
                (this format will be used for the generated thumbnail, too)
    """
    
    img.seek(0) # see http://code.djangoproject.com/ticket/8222 for details
    image = Image.open(img)
    
    # Convert to RGB if necessary
    if image.mode not in ('L', 'RGB'):
        image = image.convert('RGB')
        
    # get size
    thumb_w, thumb_h = thumb_size
    image2 = ImageOps.fit(image, (thumb_w, thumb_h), Image.ANTIALIAS)

    
    io = cStringIO.StringIO()
    # PNG and GIF are the same, JPG is JPEG
    if format.upper()=='JPG':
        format = 'JPEG'
    
    image2.save(io, format, quality=OUTPUT_QUALITY)
    return ContentFile(io.getvalue())    



class ImageWithThumbsFieldFile(ImageFieldFile):
    """
    See ImageWithThumbsField for usage example
    """

    def __init__(self, *args, **kwargs):
        super(ImageWithThumbsFieldFile, self).__init__(*args, **kwargs)
        self.sizes = self.field.sizes
        
        if self.sizes:
            def get_size(self, size):
                if not self:
                    return ''
                else:
                    split = self.url.rsplit('.',1)
                    try:
                        thumb_url = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                    except:
                        thumb_url = '%s.%sx%s' % (split,w,h)
                    return thumb_url
                    
            for size in self.sizes:
                (w,h) = size
                setattr(self, 'url_%sx%s' % (w,h), get_size(self, size))
                
    def save(self, name, content, save=True):
        content = resize_original( content )
        super(ImageWithThumbsFieldFile, self).save(name, content, save)
        
        if self.sizes:
            for size in self.sizes:
                (w,h) = size
                split = self.name.rsplit('.',1)
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])

                # you can use another thumbnailing function if you like
                thumb_content = generate_thumb(content, size, split[1])
                
                
                
                thumb_name_ = self.storage.save(thumb_name, thumb_content)        
                
                if not thumb_name == thumb_name_:
                    raise ValueError('There is already a file named %s' % thumb_name)


    def delete(self, save=True):
        name=self.name
        super(ImageWithThumbsFieldFile, self).delete(save)
        if self.sizes:
            for size in self.sizes:
                (w,h) = size
                split = name.rsplit('.',1)
                thumb_name = '%s.%sx%s.%s' % (split[0],w,h,split[1])
                try:
                    self.storage.delete(thumb_name)
                except:
                    pass




class ImageWithThumbsField(ImageField):
    attr_class = ImageWithThumbsFieldFile
    """
    Usage example:
    ==============
    photo = ImageWithThumbsField(upload_to='images', sizes=((125,125),(300,200),)
    
    To retrieve image URL, exactly the same way as with ImageField:
        my_object.photo.url
    To retrieve thumbnails URL's just add the size to it:
        my_object.photo.url_125x125
        my_object.photo.url_300x200
    
    Note: The 'sizes' attribute is not required. If you don't provide it, 
    ImageWithThumbsField will act as a normal ImageField
        
    How it works:
    =============
    For each size in the 'sizes' atribute of the field it generates a 
    thumbnail with that size and stores it following this format:
    
    available_filename.[width]x[height].extension

    Where 'available_filename' is the available filename returned by the storage
    backend for saving the original file.
    
    Following the usage example above: For storing a file called "photo.jpg" it saves:
    photo.jpg          (original file)
    photo.125x125.jpg  (first thumbnail)
    photo.300x200.jpg  (second thumbnail)
    
    With the default storage backend if photo.jpg already exists it will use these filenames:
    photo_.jpg
    photo_.125x125.jpg
    photo_.300x200.jpg
    
    Note: django-thumbs assumes that if filename "any_filename.jpg" is available 
    filenames with this format "any_filename.[widht]x[height].jpg" will be available, too.
    
    To do:
    ======
    Add method to regenerate thubmnails
    
    """
    def __init__(self, verbose_name=None, name=None, width_field=None, height_field=None, sizes=None, **kwargs):
        self.verbose_name=verbose_name
        self.name=name
        self.width_field=width_field
        self.height_field=height_field
        self.sizes = sizes
        super(ImageField, self).__init__(**kwargs)

    '''
    def clean(self, value, model_instance):
        "Check if value consists only of a valid image."

        # Use the parent's handling of required fields, etc.
        super(ImageWithThumbsField, self).clean(value, model_instance)
        
        if value.name is not None and len(value.name) > 4:
            split = value.name.rsplit('.',1)

            try:
                a = split[1]
                return value
            except:
                raise forms.ValidationError( ("O arquivo enviado n&atilde;o possui uma extens&atilde;o definida: "+smart_str(value.name)).decode('utf-8') )
        return value'''

    '''
    def clean(self, value):
        if not value:
            return
        file_exts = ('.png', '.jpg', '.jpeg', '.bmp',)
        
        from os.path import splitext
        if splitext(value)[1].lower() not in file_exts:
            raise forms.ValidationError("Only following Picture types accepted: %s" % ", ".join([f.strip('.') for f in file_exts]))
        return value'''
        