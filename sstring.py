from simstring.feature_extractor.character_ngram import CharacterNgramFeatureExtractor
from simstring.measure.cosine import CosineMeasure
from simstring.database.dict import DictDatabase
from simstring.searcher import Searcher

db = DictDatabase(CharacterNgramFeatureExtractor(2))
# db.add('円弧のマエストロ')
# db.add('bar')
# db.add('fooo')

path = "db/skill.csv"
skills = []
with open(path, encoding='utf-8-sig') as f:
	lines = [s.strip() for s in f.readlines()]
	# print(lines)
	for words in lines:
		db.add(words.split(',')[0])
		skills.append(words.split(','))

# print(skills)
searcher = Searcher(db, CosineMeasure())
results = searcher.search('独占力', 0.5)
print(results)
# => ['foo', 'fooo']
results = searcher.search('和良バ場O', 0.2)
print(results)
results = searcher.search('臨機応容', 0.5)
print(results)