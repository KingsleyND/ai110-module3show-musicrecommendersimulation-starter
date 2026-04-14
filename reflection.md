# Reflection: Comparing User Profile Outputs

---

## DEFAULT_TEST_PROFILE vs CONFLICTING_SAD_HIGH_ENERGY

Both ask for pop at high energy, but one says "happy" and the other says "sad." Because "sad" does not exist in the dataset, the mood score is always zero. Both profiles end up with nearly identical results. The system ignored how the user felt and ranked entirely on energy. A user trusting it to understand their mood would get workout songs when they wanted something quiet.

---

## CHILL_LOFI vs ACOUSTIC_BUT_HIGH_ENERGY

Same genre, both like acoustic, but opposite energy targets. CHILL_LOFI gets soft lofi songs as expected. ACOUSTIC_BUT_HIGH_ENERGY asks for energy 0.95, but every lofi song sits around 0.35 to 0.42. The acoustic bonus adds 0.5 points but the energy gap costs nearly 1.65. Energy wins every time the gap is large enough.

---

## DEEP_INTENSE_ROCK vs MEDIAN_AMBIGUOUS

DEEP_INTENSE_ROCK is narrow and confident. "Storm Runner" rises clearly to the top and the list looks decisive. MEDIAN_AMBIGUOUS sits at energy 0.5 with only two rnb songs available. Scores bunch close together and the top five pulls in unrelated genres. Vague preferences produce vague, unstable results.

---

## UNKNOWN_GENRE vs DEFAULT_TEST_PROFILE

DEFAULT_TEST_PROFILE gets clean pop results because "pop" exists in the catalog. UNKNOWN_GENRE asks for "bossa nova," which has no songs. Genre score is zero for everyone, so the winner is whoever is closest to energy 0.5 with a "relaxed" mood. The user asked for bossa nova and got reggae and jazz. The system did not warn them, it just quietly gave an unrelated answer.

---

## Why "Gym Hero" Keeps Showing Up for Happy Pop Users

"Gym Hero" is genre: pop, mood: intense, energy: 0.93. A happy pop user asking for energy 0.8 gives it a genre match and a near-perfect energy score. It only misses on mood. That is still enough to keep it in the top three almost every run. The system sees numbers that are close. It does not know that an intense workout song and a breezy happy pop song feel completely different to an actual listener.
