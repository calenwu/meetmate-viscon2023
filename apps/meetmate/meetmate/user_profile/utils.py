import logging
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


logger = logging.getLogger('django')


def file_size(value) -> None:
	limit = 3 * 1024 * 1024
	if value.size > limit:
		raise ValidationError(_('File too large. Size should not exceed 3 MB.'))

