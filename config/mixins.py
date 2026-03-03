from typing import Any

from django.forms import ModelForm


class DisableUserFieldMixin:
    """Mixin that disables specific form fields when updating an existing instance

    This mixin was created for wagtail_hooks.snippets. It dynamically wraps the form
    class and disables configured fields if the form is bound to an existing model
    inctance.

    Attributes:
        disabled_on_update_fields (list[str]): List of field names that should be
        disabled when editing an existing object
    """

    disabled_on_update_fields: list[str] = ["user"]

    def get_form_class(self, for_update: bool = False) -> type[ModelForm[Any]]:
        """Return a form class with selected fields disabled on update

        Args:
            for_update (bool): Flag provided by the parent view indicating
            if the form is being used in update mode

        Returns:
            type[ModelForm[Any]]: Dynamically generated form class where configured
            fields are disabled if the instance already exists
        """
        base_form_class = super().get_form_class(for_update=for_update)  # type: ignore[misc]
        fields_to_disable: list[str] = self.disabled_on_update_fields

        class CustomForm(base_form_class):  # type: ignore[misc, valid-type]
            """Wrapped form class that disables configured fields on update."""

            def __init__(self, *args: Any, **kwargs: Any) -> None:
                """Initialize the form and disable configured fields if editing."""
                super().__init__(*args, **kwargs)

                if self.instance and self.instance.pk:
                    for field_name in fields_to_disable:
                        if field_name in self.fields:
                            self.fields[field_name].disabled = True

        return CustomForm
