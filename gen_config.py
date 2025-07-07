from dataclasses import dataclass, field


@dataclass
class Config:
	items_per_page: int
	"""Количество записей на страницу"""
	content_file: str = ''
	"""Имя файла с контентом в папке content, по умолчанию <имя ключа>.csv"""
	googlesheet_id: str = ''
	"""ID гуглдока с данными. Если есть, перебивает content_file"""
	googlesheet_page: str = ''
	"""Название страницы в гуглдоке с данными"""
	wrapper_class: str = 'a4_vert'
	"""Класс враппера для записей на одной странице"""
	template_file: str = ''
	"""Название файла шаблона, по умолчанию <имя ключа>.htm"""
	css: list[str] = field(default_factory=list)
	"""Список подключаемых css, по умолчанию [<имя ключа>.css]"""
	skip: bool = False
	"""Пропускать эту генерацию"""
	additional_data: dict[str, str] = field(default_factory=dict)
	"""Дополнительные данные для генерации. Ключ - ключ другого конфига, значение - имя поля, которое будет индексом"""


gen_config = {
	'father': Config(
		items_per_page=1,
		googlesheet_id='1M-mcJTR0QU4wIp52_bPmiNWdTk1aqUc6aaVLJnhh4Qo',
		googlesheet_page='Отцы',
		wrapper_class='father_wrapper',
		additional_data={'mother': 'name'}
	),
	'mother': Config(
		items_per_page=1,
		googlesheet_id='1M-mcJTR0QU4wIp52_bPmiNWdTk1aqUc6aaVLJnhh4Qo',
		googlesheet_page='Матери',
	)
}

