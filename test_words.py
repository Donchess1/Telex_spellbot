import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Telex_spellbot.settings')
django.setup()

from spellbot.tasks import guess_words
import time

print("Testing word generation performance:")
for i in range(3):
    start = time.time()
    word = guess_words()
    duration = time.time() - start
    print(f"Test {i+1}: {word}, Time: {duration:.3f}s")
