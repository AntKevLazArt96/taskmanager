from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField, DateField
from wtforms.validators import DataRequired, Length, Optional


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


class TaskForm(FlaskForm):
    title = StringField(
        "Título",
        validators=[
            DataRequired(message="El título es obligatorio."),
            Length(max=120),
        ],
    )
    description = TextAreaField(
        "Descripción",
        validators=[Optional()],
        render_kw={"rows": 4},
    )
    user_id = SelectField(
        "Usuario asignado",
        validators=[DataRequired(message="Debe asignar un usuario.")],
        choices=[],
        coerce=int,
    )
    start_date = DateField(
        "Fecha de inicio",
        validators=[DataRequired(message="La fecha de inicio es obligatoria.")],
    )
    end_date = DateField(
        "Fecha de fin",
        validators=[DataRequired(message="La fecha de fin es obligatoria.")],
    )
    submit = SubmitField("Guardar")