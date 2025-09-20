ROLE_CHOICES = (
    ("ADMIN", "Admin"),
    ("DOCTOR", "Doctor"),
    ("NURSE", "Nurse"),
)

RELATION_CHOICES = (
    ("Father", "Father"),
    ("Mother", "Mother"),
    ("Spouse", "Spouse"),
    ("Sibling", "Sibling"),
    ("Other", "Other"),
)

GENDER_CHOICES = (
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
)










# choice mapping

CHOICES_MAP = {
    "role": ROLE_CHOICES,
    "gender": GENDER_CHOICES,
    "relation": RELATION_CHOICES,
}