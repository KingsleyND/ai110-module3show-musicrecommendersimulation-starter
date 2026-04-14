import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Read a CSV of songs and return a list of dicts with numeric fields cast to int/float."""
    print(f"Loading songs from {csv_path}...")
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"]           = int(row["id"])
            row["energy"]       = float(row["energy"])
            row["tempo_bpm"]    = float(row["tempo_bpm"])
            row["valence"]      = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Returns (score, reasons) where reasons is a list of human-readable strings.

    EXPERIMENTAL scoring recipe (energy doubled, genre halved):
      +1.0  genre match      (binary)          — was +2.0, halved
      +1.0  mood match       (binary)
      0–3.0 energy proximity (continuous: 3.0 × (1 - |song.energy - target|))
                                               — was 1.5×, doubled
      +0.5  acoustic bonus   (conditional: likes_acoustic AND acousticness > 0.6)
    Max possible score: 5.5
    Math check: 1.0 + 1.0 + 3.0 + 0.5 = 5.5  (all terms >= 0, energy floor = 0.0)
    """
    score = 0.0
    reasons = []

    # ① Genre match — +1.0 (halved from original +2.0)
    if song["genre"].lower() == user_prefs.get("genre", "").lower():
        score += 1.0
        reasons.append("genre match (+1.0)")

    # ② Mood match — +1.0
    if song["mood"].lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # ③ Energy proximity — 0.0 to +3.0 (doubled from original 1.5×)
    target_energy = user_prefs.get("energy", 0.5)
    energy_pts = 3.0 * (1.0 - abs(song["energy"] - target_energy))
    score += energy_pts
    reasons.append(f"energy proximity (+{energy_pts:.2f})")

    # ④ Acoustic bonus — +0.5
    if user_prefs.get("likes_acoustic") and song["acousticness"] > 0.6:
        score += 0.5
        reasons.append("acoustic bonus (+0.5)")

    return score, reasons


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Score every song — list comprehension calls score_song on each one
    scored = [
        (song, *score_song(user_prefs, song))   # → (song, score, reasons)
        for song in songs
    ]

    # Sort highest score first, then take the top k
    ranked = sorted(scored, key=lambda x: x[1], reverse=True)[:k]

    # Flatten reasons list into a single explanation string for each result
    return [(song, score, "; ".join(reasons)) for song, score, reasons in ranked]


DEFAULT_TEST_PROFILE = {
    "genre": "pop",
    "mood": "happy",
    "energy": 0.8,
    "likes_acoustic": False
}

HIGH_ENERGY_POP = {
    "genre": "pop",
    "mood": "energetic",
    "energy": 0.95,
    "likes_acoustic": False
}

CHILL_LOFI = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.25,
    "likes_acoustic": True
}

DEEP_INTENSE_ROCK = {
    "genre": "rock",
    "mood": "intense",
    "energy": 0.9,
    "likes_acoustic": False
}

# ── Adversarial / Edge-Case Profiles ────────────────────────────────────────
#
# These profiles probe the scoring logic for unexpected or counterintuitive
# results. Each comment explains exactly what is being stress-tested.

# Edge case: mood contradicts energy level, and "sad" does not exist in the
# dataset so mood never fires (+0). Energy 0.9 will strongly favour
# metal/rock songs (e.g. Chainsaw Heart, Storm Runner) even though the user
# claims a sad mood — exposing that genre+energy can fully override mood when
# mood has zero matches.
CONFLICTING_SAD_HIGH_ENERGY = {
    "genre": "pop",
    "mood": "sad",        # "sad" absent from songs.csv → mood score always +0
    "energy": 0.9,        # pulls toward intense/angry songs regardless of mood
    "likes_acoustic": False
}

# Edge case: genre that does not exist in the dataset.
# Genre score is always +0; the winner is decided purely by energy proximity
# and mood match. Reveals that a user still gets recommendations with an
# unknown genre — they just won't be genre-relevant at all.
UNKNOWN_GENRE = {
    "genre": "bossa nova",  # not present in songs.csv
    "mood": "relaxed",
    "energy": 0.5,
    "likes_acoustic": True
}

# Edge case: every signal at its minimum boundary.
# energy=0.0 maximally penalises energetic songs via 1.5*(1-|e-0|).
# Tests that the formula stays non-negative at the floor (result is 0.0,
# never negative). Moonlight Sonata Remix (acousticness=0.97) should rank
# highest: genre+mood+energy proximity+acoustic bonus.
EXTREME_LOW_ENERGY_ACOUSTIC = {
    "genre": "classical",
    "mood": "peaceful",
    "energy": 0.0,          # minimum possible — hardest penalty for any energetic song
    "likes_acoustic": True
}

# Edge case: acoustic bonus enabled but energy preference contradicts acoustic songs.
# High-acoustic songs (lofi, classical, jazz) cluster at energy 0.22–0.42.
# Requesting energy=0.95 means those same songs are penalised up to -1.5 by
# energy proximity while also earning +0.5 acoustic bonus — the two signals
# fight each other. Demonstrates the bonus can never overcome a large energy gap.
ACOUSTIC_BUT_HIGH_ENERGY = {
    "genre": "lofi",
    "mood": "chill",
    "energy": 0.95,         # lofi songs are ~0.35–0.42 → energy gap of ~0.55
    "likes_acoustic": True  # acoustic bonus fires, but energy proximity dominates
}

# Edge case: perfectly median preferences across every dimension.
# energy=0.5 sits equidistant from many songs, so no song earns the full +1.5.
# "rnb" has only two songs; "dreamy" matches only one. Tests whether a
# middle-of-the-road user produces a stable top-5 or exposes tie-breaking
# behaviour in the sort.
MEDIAN_AMBIGUOUS = {
    "genre": "rnb",
    "mood": "dreamy",
    "energy": 0.5,          # equidistant from many songs — may expose sort-stability issues
    "likes_acoustic": False
}


# Signal	Points	Rationale
# Genre match	+2.0	Strongest preference signal — users rarely cross genre boundaries
# Mood match	+1.0	Important but secondary — mood can flex within a genre
# Energy proximity	0–1.5	Continuous: 1.5 * (1 - abs(song.energy - target_energy)) — penalizes mismatches gradually
# Acoustic bonus	+0.5	Optional affinity — only awarded when likes_acoustic=True and acousticness > 0.6




"""
┌─────────────────────────────────────────────────────────────┐
│                        INPUT                                │
│                    User Preferences                         │
│                                                             │
│   favorite_genre = "pop"                                    │
│   favorite_mood  = "happy"                                  │
│   target_energy  = 0.8                                      │
│   likes_acoustic = False                                    │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     DATA SOURCE                             │
│                     data/songs.csv                          │
│                                                             │
│   20 songs, each with: id, title, artist, genre, mood,      │
│   energy, tempo_bpm, valence, danceability, acousticness    │
└───────────────────────────┬─────────────────────────────────┘
                            │  load_songs() reads & parses CSV
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      PROCESS                                │
│              The Scoring Loop (per song)                    │
│                                                             │
│   FOR each song in the loaded list:                         │
│                                                             │
│   ┌─────────────────────────────────────────────────────┐  │
│   │  JUDGE: score_song(song, user_prefs)                │  │
│   │                                                     │  │
│   │  score = 0.0                                        │  │
│   │                                                     │  │
│   │  ① Genre match?                                     │  │
│   │     song.genre == user.favorite_genre               │  │
│   │     YES → score += 2.0   NO → +0.0                 │  │
│   │                                                     │  │
│   │  ② Mood match?                                      │  │
│   │     song.mood == user.favorite_mood                 │  │
│   │     YES → score += 1.0   NO → +0.0                 │  │
│   │                                                     │  │
│   │  ③ Energy proximity (always runs)                   │  │
│   │     1.5 × (1 - |song.energy - target_energy|)       │  │
│   │     perfect match → +1.5   opposite ends → +0.0    │  │
│   │                                                     │  │
│   │  ④ Acoustic bonus?                                  │  │
│   │     likes_acoustic=True AND acousticness > 0.6      │  │
│   │     YES → score += 0.5   NO → +0.0                 │  │
│   │                                                     │  │
│   │  → returns (song, score, explanation_string)        │  │
│   └─────────────────────────────────────────────────────┘  │
│                                                             │
│   COLLECT all (song, score, explanation) tuples             │
│   SORT by score, descending                                 │
│   TAKE top K                                                │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                       OUTPUT                                │
│              Top K Ranked Recommendations                   │
│                                                             │
│   #1  Sunrise City      score: 4.85   ← genre+mood+energy  │
│   #2  Rooftop Lights    score: 3.64   ← genre+energy       │
│   #3  Gym Hero          score: 2.85   ← genre+energy       │
│   ...                                                       │
│                                                             │
│   Each result includes:                                     │
│     • song metadata (title, artist, genre…)                 │
│     • numeric score  (max possible: 5.0)                    │
│     • human-readable explanation of why it was chosen       │
└─────────────────────────────────────────────────────────

"""