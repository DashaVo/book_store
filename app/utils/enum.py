from enum import Enum

class Genre(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE = "Science"
    FANTASY = "Fantasy"
    BIOGRAPHY = "Biography"
    MYSTERY = "Mystery"
    THRILLER = "Thriller"
    ROMANCE = "Romance"
    HISTORICAL = "Historical"
    ADVENTURE = "Adventure"
    HORROR = "Horror"
    SCIENCE_FICTION = "Science Fiction"
    DYSTOPIAN = "Dystopian"
    MEMOIR = "Memoir"
    SELF_HELP = "Self-Help"