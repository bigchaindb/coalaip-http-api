from web.utils import parse_model


user_model = parse_model(['verifyingKey', 'signingKey'])
manifestation_model = parse_model(['name', 'datePublished', 'url'])
work_model = parse_model(['name', 'author'])
