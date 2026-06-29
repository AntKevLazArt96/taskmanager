from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField
from wtforms.validators import DataRequired, Length


class UserForm(FlaskForm):
    name = StringField(
        "Nombre",
        validators=[
            DataRequired(message="El nombre es obligatorio."),
            Length(max=120),
        ],
    )
    profile = SelectField(
        "Perfil profesional",
        validators=[DataRequired(message="El perfil es obligatorio.")],
        choices=[],
    )
    submit = SubmitField("Guardar")