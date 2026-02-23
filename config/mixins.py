from typing import Any

from django.forms import ModelForm


class DisableUserFieldMixin:
    disabled_on_update_fields: list[str] = ["user"]

    def get_form_class(self, for_update: bool = False) -> type[ModelForm[Any]]:
        base_form_class = super().get_form_class(for_update=for_update)  # type: ignore[misc]
        fields_to_disable: list[str] = self.disabled_on_update_fields

        class CustomForm(base_form_class):  # type: ignore[misc, valid-type]
            def __init__(self, *args: Any, **kwargs: Any) -> None:
                super().__init__(*args, **kwargs)

                if self.instance and self.instance.pk:
                    for field_name in fields_to_disable:
                        if field_name in self.fields:
                            self.fields[field_name].disabled = True

        return CustomForm
