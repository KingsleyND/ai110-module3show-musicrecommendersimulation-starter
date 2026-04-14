# Model Card: Music Recommender Simulation

## 1. Model Name

**ScoreSong 1.0**

---

## 2. Intended Use

This recommender suggests songs from a small catalog based on what a user says they like. It takes a user's favorite genre, mood, energy level, and whether they like acoustic music. Then it returns the five songs that best match those preferences. This is for classroom exploration only. It is not meant for real users or a real music app.

---

## 3. How the Model Works

Each song gets a score based on how well it matches the user. The score has four parts.

First, if the song genre matches what the user likes, the song gets one point. Second, if the mood matches, it gets another point. Third, the system looks at how close the song's energy is to what the user wants. A perfect energy match adds three points. A song that is far off in energy gets close to zero for that part. Fourth, if the user likes acoustic music and the song is highly acoustic, it gets a small bonus of half a point.

The song with the highest total score gets recommended first. The top five are shown.

The original starter gave genre two points. This version gives genre one point and doubled the energy weight to three points. That change makes energy the most important factor now.

---

## 4. Data

The catalog has 20 songs stored in a CSV file. The songs cover 13 genres including pop, lofi, rock, jazz, hip-hop, classical, synthwave, ambient, reggae, funk, country, rnb, and indie pop. The moods in the dataset include happy, chill, intense, relaxed, moody, focused, romantic, dreamy, nostalgic, energetic, angry, and peaceful.

Most genres only appear once or twice. Pop and lofi have the most songs. Genres like reggae, country, and funk have only one song each. There are no songs for genres like bossa nova, EDM, or soul, so users who prefer those will get unrelated results.

---

## 5. Strengths

The system works best for users who like pop or lofi because those genres have the most songs in the catalog. If a user has a clear preference for one genre and a specific energy level, the top result usually feels like a good match. The scoring is simple enough that you can read the explanation for each recommendation and understand exactly why a song was chosen. That transparency is hard to get in a real recommender.

---

## 6. Limitations and Bias

The system creates a filter bubble around genre. A user who likes pop will almost always see pop songs at the top, even when a song from another genre is a better match on energy and mood. Genres like reggae, funk, and country appear only once in the catalog. The system cannot produce five good matches for users who prefer those genres. The energy penalty can also silently bury a song that matches on every other dimension. A chill lofi user asking for energy 0.25 will never see "Groove Machine" even if it fits their genre, because the energy gap alone costs that song too many points. Finally, the system has no concept of variety. It can return the same artist twice in one top-five list because nothing stops it.

---

## 7. Evaluation

Five user profiles were tested: DEFAULT_TEST_PROFILE, CHILL_LOFI, DEEP_INTENSE_ROCK, CONFLICTING_SAD_HIGH_ENERGY, and UNKNOWN_GENRE.

The most surprising result came from CONFLICTING_SAD_HIGH_ENERGY. The mood was set to "sad" but that word does not appear anywhere in the song catalog. So the mood score was zero for every single song. The system ended up recommending "Gym Hero" and "Chainsaw Heart" to someone who said they were sad, because high energy was the only signal left to rank on.

For the UNKNOWN_GENRE profile, the genre was "bossa nova," which also has no songs in the catalog. Every song started at zero for genre. The winners were decided only by energy and mood, which surfaced reggae and jazz songs. The user asked for bossa nova and got something completely different, with no warning from the system.

---

## 8. Future Work

It would help to add a fallback when a genre or mood does not match anything in the catalog. Right now the system stays silent and returns unrelated results. Adding a bigger and more balanced catalog would also reduce the bias toward pop and lofi. A diversity rule that prevents the same artist from appearing more than once in the top five would make results feel less repetitive. Letting users give a range for energy instead of one exact number would also make the recommendations more forgiving.

---

## 9. Personal Reflection

In the final section of Model Card (or the README.md), write a personal reflection on my engineering process.
What was your biggest learning moment during this project? how recommendations systems work at a high level
How did using AI tools help you, and when did you need to double-check them? It helped with implementing the systems I built. I needed to double check when I saw odd recommendations based on a specific profile 
What surprised you about how simple algorithms can still "feel" like recommendations? by adding more characteristics to the songs, recommendations can be more personalized
What would you try next if you extended this project? I'd like to use actual music data
