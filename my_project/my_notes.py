# Import the necessary module from DRF for creating serializers
from rest_framework import serializers

# Import the model class that this serializer will represent (e.g., Task, Book)
from .models import MyModel

# Define the serializer class. It inherits from ModelSerializer.
# ModelSerializer is a shortcut that automatically creates fields corresponding
# to the fields in the specified Django model.
class MyModelSerializer(serializers.ModelSerializer):
    
    # The Meta class provides configuration options for the ModelSerializer.
    class Meta:
        
        # 1. Specifies which Django model the serializer should be linked to.
        #    This is how the ModelSerializer knows what fields to look for.
        model = MyModel
        
        # 2. A list of model field names to be included in the serialized output 
        #    and allowed in the input data.
        #    - 'id': Typically the primary key, included for reference/updates.
        #    - 'name', 'description': Custom fields from your MyModel.
        #    - 'created_at': Often a read-only field (if set in the model)
        #                    used to show when the object was created.
        fields = ['id', 'name', 'description', 'created_at']

        # Alternative: You could use fields = '__all__' to include every field 
        # on the model, but explicitly listing them is generally better practice.
        
        # Optional: You can also specify read_only_fields here if you 
        # wanted to ensure 'created_at' can't be set or changed on creation/update.
        # e.g., read_only_fields = ['created_at']




        # Import the necessary module from DRF for creating serializers.
from rest_framework import serializers

# Import the model class (the database structure) that this serializer will represent.
from .models import MyModel

# Define the serializer class. It inherits from ModelSerializer 
# to automatically generate fields and methods for CRUD operations 
# based on MyModel.
class MyModelSerializer(serializers.ModelSerializer):
    
    # The inner Meta class provides configuration options for the ModelSerializer.
    class Meta:
        
        # 1. Specifies the Django model this serializer is linked to.
        model = MyModel
        
        # 2. A list of model field names to be included in the serialized data.
        fields = ['id', 'name', 'description', 'created_at']

    # Define a custom validation method that runs after initial field validation
    # but before the object is created or updated in the database.
    # The 'data' argument contains the complete, validated dictionary of fields.
    def validate(self, data):
        
        # Check if the length of the 'name' field in the incoming data is less than 5.
        if len(data['name']) < 5:
            # If the condition is met, raise a ValidationError.
            # This halts the serialization process and returns the message 
            # to the client as an HTTP 400 Bad Request error.
            raise serializers.ValidationError("Name must be at least 5 characters long.")
            
        # The data must be returned if validation passes. If this line is omitted, 
        # the valid data will be lost, and the object won't be saved correctly.
        return data
    


     QUERYSET AND FILTERING
    

    # Import the necessary module from DRF for creating generic class-based views.
from rest_framework import generics

# Import the model class (the database structure) this view will operate on.
from .models import MyModel

# Import the serializer class used to convert model instances to/from JSON.
from .serializers import MyModelSerializer

# Define the API view class.
# It inherits from ListCreateAPIView, which handles both:
# 1. GET requests (to list objects).
# 2. POST requests (to create a new object).
class MyModelListCreateAPIView(generics.ListCreateAPIView):
    
    # Define the base set of objects the view will interact with.
    # By default, it selects ALL records from the MyModel database table.
    queryset = MyModel.objects.all()
    
    # Specifies the serializer class that should be used to validate input 
    # (for POST) and format output (for GET).
    serializer_class = MyModelSerializer

    # Override the default get_queryset method to allow for custom filtering.
    # This method runs specifically for GET requests (listing objects).
    def get_queryset(self):
        
        # Start with the default queryset defined above (MyModel.objects.all()).
        queryset = self.queryset
        
        # Check the URL query parameters (e.g., /api/mymodels/?name=searchterm).
        # .get('name', None) retrieves the value of the 'name' parameter, 
        # defaulting to None if it's not present.
        name_filter = self.request.query_params.get('name', None)
        
        # Check if a filter value was provided by the user.
        if name_filter is not None:
            
            # Filter the queryset: only include objects where the 'name' field
            # contains the value of name_filter, case-insensitively (i stands for insensitive).
            queryset = queryset.filter(name__icontains=name_filter)
            
        # Return the final, filtered (or unfiltered) queryset to DRF for serialization.
        return queryset