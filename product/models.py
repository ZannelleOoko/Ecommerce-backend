from io import BytesIO
from PIL import Image # type: ignore

from django.core.files import File
from django.db import models

class Category(models.Model): #creates a django model named category
    name=models.CharField(max_length=255) #the name of the category is stored in a string of len 255 created by charfield
    slug=models.SlugField() #the url portion of the name is stored in a slugfield

    class Meta: #meta is an inner class that stores metadata of the model
        ordering =('name',) #specifies the default ordering of the categories from the database(by name in ascending order)

    def __str__(self): 
        return self.name #when you print the category object, it returns the value of the name field, if you dont use the __str__ method, what will be returned will be very uninformative(yo will not know exactly what it is)
    
    def get_absolute_url(self):
        return f'/{self.slug}/' #returns the url for the category object
    
class Product(models.Model): #we create a model named product(then create fields below(attributes of the product))
        category=models.ForeignKey(Category, related_name='products', on_delete=models.CASCADE) # type: ignore #we use the field(category) to relate the product to Category class above. this creates a foreigkey that relates a product to just one Category, enables yu to access all products in a category without specifying the names and on deleting a Category, all the products within it are also deleted, to ensure there are no orphaned products in the database
        name=models.CharField(max_length=255) #creates a string where the name of the product is stored
        slug=models.SlugField() # stores the url portion of the name
        description=models.TextField(blank=True, null=True) #store a detailed description of the product, can be blank or null
        price=models.DecimalField(max_digits=6, decimal_places=2)#stores the price of the product
        image=models.ImageField(upload_to='uploads/', blank=True, null=True)
        thumbnail=models.ImageField(upload_to='uploads/', blank=True, null=True)
        date_added=models.DateTimeField(auto_now_add=True)

        class Meta:
            ordering=('-date_added',)

        def __str__(self):
            return self.name
        
        def get_absolute_url(self):
            return f'/{self.category.slug}/{self.slug}/'
        
        def get_image(self):
            if self.image:
                return 'http://127.0.0.1:8000' + self.image.url
            return''
        
        def get_thumbnail(self):
            if self.thumbnail:
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                if self.image:
                    self.thumbnail=self.make_thumbnail(self.image)
                    self.save()
                    return 'http://127.0.0.1:8000' + self.thumbnail.url
                else:
                    return''
                
        def make_thumbnail(self, image, size=(300,200)): #creating a thumbnail image from the given image file
            img=Image.open(image)
            img.convert('RGB') # Converts the image to RGB mode. This ensures the image is in a standard color format
            img.thumbnail(size) #resizes the image to fit within the specified size

            thumb_io = BytesIO() #Creates an in-memory binary stream to hold the thumbnail image data.
            img.save(thumb_io, 'JPEG', quality=85) #Saves the thumbnail image to the thumb_io stream in JPEG format with a quality setting of 85 (on a scale from 1 to 100).
            thumbnail = File(thumb_io, name=image.name) #Wraps the in-memory binary stream (thumb_io) in a Django File object. The name=image.name argument sets the file name of the thumbnail to be the same as the original image's name.
            return thumbnail

       #summary of the function
"""     
Image Opening and Conversion: Opens and converts the image to RGB format.
Thumbnail Creation: Resizes the image to fit within specified dimensions while maintaining the aspect ratio.
Saving to BytesIO: Saves the thumbnail to an in-memory stream in JPEG format.
Creating Django File Object: Wraps the stream in a Django File object for easy manipulation and saving.
Returning Thumbnail: Returns the Django File object containing the thumbnail image."""
#the paragraph above is technically a comment, it can however be used as one since it is a string but if it is not assigned to an variable, it does not affect execution of the code

            
        
