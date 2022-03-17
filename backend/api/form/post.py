from wtforms import Form, StringField, validators


class CreatePostForm(Form):
    content = StringField('Content', [validators.Length(min=3, max=200)])


class UpdatePostForm(Form):
    content = StringField('Content', [validators.Length(min=3, max=200)])


class ReplyPostForm(Form):
    content = StringField('Content', [validators.Length(min=3, max=200)])
