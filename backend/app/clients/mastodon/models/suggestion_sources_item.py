from enum import Enum


class SuggestionSourcesItem(str, Enum):
    FEATURED = "featured"
    FRIENDS_OF_FRIENDS = "friends_of_friends"
    MOST_FOLLOWED = "most_followed"
    MOST_INTERACTIONS = "most_interactions"
    SIMILAR_TO_RECENTLY_FOLLOWED = "similar_to_recently_followed"

    def __str__(self) -> str:
        return str(self.value)
