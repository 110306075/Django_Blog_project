# create a class to define the shape of form(input), validation rules
from django import forms
from .models import Review, Comment
# class BlogForm(forms.Form):
#     username = forms.CharField(label="USERNAMEEE",required=True,max_length=10,error_messages={})
#     review = forms.CharField(label="Your feedback",widget=forms.Textarea,max_length=200)
#     rating = forms.IntegerField(label="Your Rating",min_value=1,max_value=5)


class CommentForm(forms.ModelForm):
    class Meta:
        model  = Comment
        exclude = ['post', 'date']
        labels = {"name":'Your name:',
                   "email": "Your Email:",
                   "text":"Your comment"}


#  automaticall/ define a form based on  model
class BlogForm(forms.ModelForm):
    # this nested class in to connect the form to which models and define the field should be involved in the form ,
    # also the basic setting of the form
    class Meta:
        model = Review
        # feild=['username','review','rating']
        exclude = ['']
        field = '__all__'
        lables={"username":'Your name',"review":'Your review', 'rating':'Your rating'}
        error_message={'username':{'required':'this reild should not be blank'}}


class FileForm(forms.Form):
    user_image = forms.ImageField(allow_empty_file=True)
