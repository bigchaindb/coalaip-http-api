from web.utils import parse_model


user_model = parse_model(['publicKey', 'privateKey'])
manifestation_model = parse_model(['name', 'datePublished', 'url'])
work_model = parse_model(['name', 'author'])
right_model = parse_model(['license'])
