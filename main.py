import pandas as pd

def prepareData():
    titles = pd.read_csv("data/title.basics.tsv", sep='\t', low_memory=False)
    ratings = pd.read_csv("data/title.ratings.tsv", sep='\t', low_memory=False)

    titles_with_ratings = titles.set_index('tconst').join(ratings.set_index('tconst'))

    movie_pool = titles_with_ratings.loc[
        (titles_with_ratings['titleType'] == 'movie') & 
        (titles_with_ratings['isAdult'] == 0) & 
        (titles_with_ratings['numVotes'] > 10000)
    ]

    return movie_pool

def run(movie_pool):
    score = 0
    high_score = 0
    game_pair = (movie_pool.sample(), movie_pool.sample())
    answer = None

    while True:
        if game_pair[0].averageRating.item() > game_pair[1].averageRating.item():
            answer = ['l']
        elif game_pair[0].averageRating.item() < game_pair[1].averageRating.item():
            answer = ['h']
        elif game_pair[0].averageRating.item() == game_pair[1].averageRating.item():
            answer = ['h','l']

        print("Movie 1: %s (rating = %s)" % (game_pair[0].primaryTitle.item(), game_pair[0].averageRating.item()))
        print("Movie 2: %s (rating = ???)" % game_pair[1].primaryTitle.item())

        user_input = input("\nIs Movie 2 rated higher (press h) or lower (press l) on IMDB?\n")
        
        if user_input in ['h', 'l']:
            if user_input in answer:
                score += 1
                if score > high_score:
                    high_score = score
                print("\n**CORRECT**")
                print(
                    "%s is rated %s and %s is rated %s\n" 
                    % (game_pair[0].primaryTitle.item(), game_pair[0].averageRating.item(), game_pair[1].primaryTitle.item(), game_pair[1].averageRating.item())
                    )
                game_pair = (game_pair[1], movie_pool.sample())
                print("SCORE: %s, HIGH SCORE: %s" % (str(score), str(high_score)))
                print("_______________________________\n")

            else:
                print("\n**INCORRECT**")
                print(
                    "%s is rated %s and %s is rated %s\n" 
                    % (game_pair[0].primaryTitle.item(), game_pair[0].averageRating.item(), game_pair[1].primaryTitle.item(), game_pair[1].averageRating.item())
                    )
                print("SCORE: %s, HIGH SCORE: %s" % (str(score), str(high_score)))
                print("_______________________________\n")
                score = 0
                if input("Play again (y,n)? ") == 'y':
                    game_pair = (movie_pool.sample(), movie_pool.sample())
                    print()
                else:
                    break
        else:
            print("\nINVALID INPUT")
            break

# GET MOVIE POSTER FROM THE MOVIE DB API, PATH FOUND @ http://image.tmdb.org/t/p/w185/<URLPATH>
        
if __name__ == "__main__":
    movie_pool = prepareData()
    run(movie_pool)
