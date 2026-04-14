"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs, DEFAULT_TEST_PROFILE


def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded {len(songs)} songs.\n")

    user_prefs = DEFAULT_TEST_PROFILE

    print("User preferences:")
    for key, value in user_prefs.items():
        print(f"  {key}: {value}")

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "=" * 50)
    print("  TOP RECOMMENDATIONS")
    print("=" * 50)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n#{rank}  {song['title']}  —  {song['artist']}")
        print(f"    Score : {score:.2f} / 5.00")
        print(f"    Genre : {song['genre']}   Mood: {song['mood']}   Energy: {song['energy']:.2f}")
        print(f"    Why   : {explanation}")

    print("\n" + "=" * 50)


if __name__ == "__main__":
    main()
