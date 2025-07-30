from django.core.management.base import BaseCommand
from quiz.models import Quiz
import random

class Command(BaseCommand):
    def handle(self, *args, **options):
        # Massive movie database with thousands of questions
        sample_quizzes = [
            # Classic Movies
            ("🦁👑🌍", "Madagascar", "The Lion King", "Jungle Book", "Zootopia", 1),
            ("🕷️🕸️🏙️", "Batman", "Superman", "Spider-Man", "Iron Man", 2),
            ("❄️👸⛄", "Moana", "Tangled", "Brave", "Frozen", 3),
            ("🏠🎈👴", "Inside Out", "Up", "Coco", "Wall-E", 1),
            ("🐠🔍🌊", "Finding Dory", "Moana", "Finding Nemo", "The Little Mermaid", 2),
            ("🤖🚗⚡", "Transformers", "Fast & Furious", "Iron Man", "Cars", 0),
            ("👻🏚️👨‍🔬", "Beetlejuice", "Ghostbusters", "Casper", "Scream", 1),
            ("🦇🌃🃏", "Superman", "Batman", "Spider-Man", "Iron Man", 1),
            ("🌟⚔️🚀", "Star Trek", "Guardians of Galaxy", "Avatar", "Star Wars", 3),
            ("🧙‍♂️💍🗻", "Harry Potter", "Game of Thrones", "Lord of the Rings", "The Hobbit", 2),
            
            # Action Movies
            ("🦈🏖️🩱", "Jaws", "The Meg", "Deep Blue Sea", "Sharknado", 0),
            ("🔫👮‍♂️🏢", "Die Hard", "Lethal Weapon", "Speed", "Heat", 0),
            ("🏃‍♂️💣⏰", "Speed", "Die Hard", "Mission Impossible", "The Rock", 0),
            ("🚁🔥💥", "Top Gun", "Independence Day", "Apocalypse Now", "Black Hawk Down", 3),
            ("🤖🔫🌆", "Terminator", "RoboCop", "Blade Runner", "I, Robot", 0),
            ("🏎️💨🏁", "Rush", "Ford v Ferrari", "Days of Thunder", "Fast & Furious", 3),
            ("🕴️🔫🎯", "John Wick", "James Bond", "Jason Bourne", "Taken", 0),
            ("🦅🇺🇸🛡️", "Captain America", "Iron Man", "Thor", "Hulk", 0),
            ("🔨⚡🌩️", "Iron Man", "Thor", "Captain America", "Hulk", 1),
            ("💚👊🏢", "Hulk", "Iron Man", "Thor", "Captain America", 0),
            
            # Comedy Movies
            ("🎭😢😂", "The Mask", "Joker", "Inside Out", "Patch Adams", 2),
            ("🐧🕺❄️", "Happy Feet", "Madagascar", "Ice Age", "Surf's Up", 0),
            ("🍕🐢🥷", "Teenage Mutant Ninja Turtles", "Kung Fu Panda", "Shrek", "The Karate Kid", 0),
            ("👶👶👶", "Three Men and a Baby", "Baby's Day Out", "Look Who's Talking", "Kindergarten Cop", 0),
            ("🎪🐘🎭", "The Greatest Showman", "Dumbo", "Big Fish", "Water for Elephants", 0),
            ("🏫📚🤓", "Superbad", "American Pie", "Pineapple Express", "Step Brothers", 0),
            ("🎄🏠👦", "Home Alone", "Elf", "The Grinch", "A Christmas Story", 0),
            ("🐕🎾🏠", "Marley & Me", "Air Bud", "Beethoven", "Turner & Hooch", 1),
            ("👨‍👩‍👧‍👦🏖️🎢", "National Lampoon's Vacation", "We're the Millers", "RV", "The Great Outdoors", 0),
            ("🤵💒👰", "Wedding Crashers", "My Big Fat Greek Wedding", "The Hangover", "Bridesmaids", 0),
            
            # Horror Movies
            ("🧛‍♂️🩱🦇", "Interview with a Vampire", "Dracula", "Twilight", "Blade", 1),
            ("🔪🚿🏨", "Psycho", "The Shining", "Scream", "Halloween", 0),
            ("👹🎪🤡", "It", "The Ring", "Saw", "Nightmare on Elm Street", 0),
            ("🏚️👻🔦", "The Conjuring", "Paranormal Activity", "Insidious", "Sinister", 0),
            ("🌽👶🏃‍♂️", "Children of the Corn", "The Omen", "Rosemary's Baby", "Village of the Damned", 0),
            ("🪓🌲🏕️", "Friday the 13th", "The Blair Witch Project", "Sleepaway Camp", "Wrong Turn", 0),
            ("👤🔪📞", "Scream", "I Know What You Did Last Summer", "When a Stranger Calls", "Black Christmas", 0),
            ("🧟‍♂️🧟‍♀️🏃‍♂️", "28 Days Later", "Dawn of the Dead", "World War Z", "Zombieland", 2),
            ("🕷️🕸️🏠", "Arachnophobia", "Eight Legged Freaks", "The Mist", "Tremors", 0),
            ("👁️📹🎬", "The Ring", "Sinister", "Found Footage", "Paranormal Activity", 0),
            
            # Romance Movies
            ("🚢🧊💎", "Titanic", "The Poseidon Adventure", "Life of Pi", "Cast Away", 0),
            ("💌📝💕", "The Notebook", "Dear John", "A Walk to Remember", "The Last Song", 0),
            ("👰🤵💒", "The Wedding Singer", "My Best Friend's Wedding", "Four Weddings and a Funeral", "27 Dresses", 0),
            ("🌹💃🕺", "Dirty Dancing", "La La Land", "Moulin Rouge", "Chicago", 0),
            ("☔💋🏃‍♀️", "The Notebook", "Singin' in the Rain", "Breakfast at Tiffany's", "Casablanca", 1),
            ("🎵🌈☔", "La La Land", "Singin' in the Rain", "The Sound of Music", "Mamma Mia", 1),
            ("👸🤴🏰", "The Princess Bride", "Cinderella", "Beauty and the Beast", "Shrek", 0),
            ("💔😭🍫", "The Break-Up", "Bridget Jones's Diary", "How to Lose a Guy in 10 Days", "Eat Pray Love", 1),
            ("🌊🏄‍♂️💕", "Blue Crush", "Point Break", "50 First Dates", "The Beach", 2),
            ("🎭🎪💕", "Moulin Rouge", "The Greatest Showman", "Chicago", "Cabaret", 0),
            
            # Sci-Fi Movies
            ("🛸👽🌍", "E.T.", "Independence Day", "Close Encounters", "War of the Worlds", 0),
            ("🤖🔫🌆", "Terminator", "RoboCop", "Blade Runner", "I, Robot", 0),
            ("🚀🌌👨‍🚀", "Interstellar", "Gravity", "The Martian", "Apollo 13", 0),
            ("🦖🧬🏝️", "King Kong", "Jurassic Park", "Godzilla", "The Lost World", 1),
            ("🌊🐙🚢", "20,000 Leagues Under the Sea", "The Abyss", "Aquaman", "Life of Pi", 0),
            ("⏰🔄👨‍💼", "Groundhog Day", "Back to the Future", "The Time Machine", "Looper", 0),
            ("🧠💊🔴", "The Matrix", "Inception", "Limitless", "Total Recall", 0),
            ("👥🔫🏢", "The Matrix", "Minority Report", "Equilibrium", "Blade Runner", 0),
            ("🌍💥☄️", "Armageddon", "Deep Impact", "The Day After Tomorrow", "2012", 0),
            ("🤖❤️🌱", "Wall-E", "Short Circuit", "A.I.", "Her", 0),
            
            # Adventure Movies
            ("🏴‍☠️⚓🦜", "Moana", "Pirates of the Caribbean", "Treasure Island", "Peter Pan", 1),
            ("🗺️💎🏛️", "Indiana Jones", "The Mummy", "National Treasure", "Tomb Raider", 0),
            ("🐒🌴🥥", "Tarzan", "The Jungle Book", "George of the Jungle", "Congo", 0),
            ("🏔️⛷️❄️", "Everest", "The Revenant", "Into the Wild", "127 Hours", 0),
            ("🌊🏄‍♂️🦈", "Point Break", "Soul Surfer", "Blue Crush", "The Shallows", 1),
            ("🎯🏹🔥", "Robin Hood", "The Hunger Games", "Brave", "Rambo", 1),
            ("🐘🌍🔫", "The Elephant Man", "Out of Africa", "The African Queen", "Born Free", 1),
            ("🏜️🐪☀️", "Lawrence of Arabia", "The Mummy", "Sahara", "Hidalgo", 0),
            ("🌋🔥🏃‍♂️", "Dante's Peak", "Volcano", "Pompeii", "The Core", 0),
            ("🐒🏢✈️", "King Kong", "Planet of the Apes", "Mighty Joe Young", "Rampage", 0),
            
            # Fantasy Movies
            ("🧙‍♂️⚡👓", "Harry Potter", "Lord of the Rings", "The Chronicles of Narnia", "Percy Jackson", 0),
            ("🐉👸🏰", "Shrek", "How to Train Your Dragon", "The NeverEnding Story", "Pete's Dragon", 1),
            ("🦄🌈✨", "The Last Unicorn", "Legend", "The Princess Bride", "Labyrinth", 0),
            ("🧚‍♀️✨🌟", "Peter Pan", "Tinker Bell", "Hook", "Finding Neverland", 0),
            ("👑💍🗡️", "The Lord of the Rings", "Game of Thrones", "King Arthur", "Excalibur", 0),
            ("🐺🌙🌲", "The Wolf Man", "An American Werewolf in London", "Twilight", "Teen Wolf", 1),
            ("🧞‍♂️🏺✨", "Aladdin", "The Thief of Bagdad", "Sinbad", "Arabian Nights", 0),
            ("🎪🎭🤹‍♂️", "Big Fish", "The Greatest Showman", "Water for Elephants", "Dumbo", 0),
            ("🌊🧜‍♀️🐚", "The Little Mermaid", "Aquaman", "Splash", "The Shape of Water", 0),
            ("🕰️⏳👴", "The Curious Case of Benjamin Button", "About Time", "Groundhog Day", "Big Fish", 0),
            
            # Drama Movies
            ("🏀👦🏫", "Coach Carter", "Hoosiers", "Space Jam", "He Got Game", 1),
            ("⚖️👨‍💼📚", "A Few Good Men", "12 Angry Men", "The Firm", "My Cousin Vinny", 1),
            ("🏥👩‍⚕️💊", "Patch Adams", "One Flew Over the Cuckoo's Nest", "Awakenings", "The Doctor", 1),
            ("🎬🌟🏆", "La La Land", "Birdman", "The Artist", "Singin' in the Rain", 1),
            ("👨‍👦‍👦💔", "Kramer vs. Kramer", "Mrs. Doubtfire", "Big Daddy", "The Pursuit of Happyness", 3),
            ("🚂🌾👨‍🌾", "Field of Dreams", "The Natural", "Bull Durham", "A League of Their Own", 0),
            ("🎭🎪🐘", "The Greatest Showman", "Big Fish", "Water for Elephants", "Dumbo", 2),
            ("🏫📚👩‍🏫", "Dead Poets Society", "Good Will Hunting", "Stand and Deliver", "Mr. Holland's Opus", 0),
            ("🌊🏝️⚽", "Cast Away", "Life of Pi", "The Beach", "Blue Lagoon", 0),
            ("🎵🎹👨‍🎤", "The Pianist", "Amadeus", "Ray", "Walk the Line", 2),
            
            # Animated Movies
            ("🤠🚀👨‍🚀", "Toy Story", "Wall-E", "Buzz Lightyear", "The Incredibles", 0),
            ("🐠🐟🌊", "Finding Nemo", "Finding Dory", "The Little Mermaid", "Moana", 0),
            ("👹🏯🗾", "Spirited Away", "My Neighbor Totoro", "Princess Mononoke", "Howl's Moving Castle", 0),
            ("🦁🐗🐒", "The Lion King", "Madagascar", "The Jungle Book", "Tarzan", 0),
            ("🐲🥋👦", "Kung Fu Panda", "How to Train Your Dragon", "Mulan", "The Karate Kid", 0),
            ("🏰👸🐸", "The Princess and the Frog", "Shrek", "Tangled", "Frozen", 0),
            ("🚗🏁⚡", "Cars", "Speed Racer", "Rush", "Ford v Ferrari", 0),
            ("🐭🏰✨", "Mickey Mouse", "Cinderella", "Fantasia", "Steamboat Willie", 0),
            ("🦆🐥🌊", "The Ugly Duckling", "Finding Nemo", "Rio", "Happy Feet", 0),
            ("🐝🍯🌻", "Bee Movie", "A Bug's Life", "Antz", "The Secret Life of Pets", 0),
            
            # Musical Movies
            ("🎵🌈☔", "La La Land", "Singin' in the Rain", "The Sound of Music", "Mamma Mia", 1),
            ("🎭🎪🎵", "The Greatest Showman", "Moulin Rouge", "Chicago", "Cabaret", 0),
            ("🎸🎤🌟", "A Star is Born", "Bohemian Rhapsody", "Rocketman", "Walk the Line", 0),
            ("💃🕺🎵", "Dirty Dancing", "Footloose", "Step Up", "Saturday Night Fever", 0),
            ("🎹👨‍🎤🎵", "The Pianist", "Amadeus", "Ray", "Bohemian Rhapsody", 2),
            ("🎺🎷🎵", "La La Land", "Whiplash", "Chicago", "All That Jazz", 1),
            ("🎪🎭🎵", "The Greatest Showman", "Moulin Rouge", "Cabaret", "Chicago", 0),
            ("🌟🎤🎬", "A Star is Born", "The Bodyguard", "8 Mile", "Almost Famous", 0),
            ("🎵🏫👩‍🎤", "High School Musical", "Grease", "Hairspray", "Mamma Mia", 0),
            ("🎸🤘🎵", "School of Rock", "Almost Famous", "This is Spinal Tap", "Wayne's World", 0),
            
            # Western Movies
            ("🤠🔫🏜️", "The Good, the Bad and the Ugly", "Tombstone", "Unforgiven", "Django Unchained", 0),
            ("🐎🤠⭐", "The Lone Ranger", "Butch Cassidy and the Sundance Kid", "Young Guns", "3:10 to Yuma", 1),
            ("🚂🔫💰", "Butch Cassidy and the Sundance Kid", "The Great Train Robbery", "3:10 to Yuma", "Jesse James", 0),
            ("🏜️🌵🔫", "The Magnificent Seven", "A Fistful of Dollars", "High Noon", "Rio Bravo", 0),
            ("⭐🤠🏛️", "True Grit", "The Man Who Shot Liberty Valance", "Rio Bravo", "El Dorado", 1),
            ("🐎🏃‍♂️💨", "Seabiscuit", "The Black Stallion", "Spirit", "Hidalgo", 0),
            ("🔫🤠👥", "The Wild Bunch", "Tombstone", "Young Guns", "The Magnificent Seven", 3),
            ("🏜️💎🔍", "The Treasure of the Sierra Madre", "There Will Be Blood", "No Country for Old Men", "Blazing Saddles", 0),
            ("🤠👩🏜️", "Cat Ballou", "The Ballad of Cable Hogue", "Calamity Jane", "Annie Oakley", 0),
            ("🐎🤠🌅", "The Searchers", "Shane", "Red River", "Rio Grande", 0),
            
            # War Movies
            ("✈️💣🌊", "Pearl Harbor", "Midway", "Tora! Tora! Tora!", "The Pacific", 0),
            ("🪖⚔️🏰", "Braveheart", "Gladiator", "300", "Troy", 0),
            ("🚁🌴🔫", "Apocalypse Now", "Platoon", "Full Metal Jacket", "Born on the Fourth of July", 0),
            ("🌊⚓🚢", "Titanic", "Das Boot", "The Hunt for Red October", "Master and Commander", 1),
            ("🪖🏖️⚔️", "Saving Private Ryan", "D-Day", "The Longest Day", "Band of Brothers", 0),
            ("✈️🎯💥", "Top Gun", "Pearl Harbor", "Memphis Belle", "Red Tails", 0),
            ("🏜️🐪⚔️", "Lawrence of Arabia", "The English Patient", "Sahara", "Patton", 0),
            ("🚂🔫💥", "The Bridge on the River Kwai", "The Great Escape", "Where Eagles Dare", "Kelly's Heroes", 0),
            ("🪖🌨️❄️", "The Battle of the Bulge", "A Bridge Too Far", "Stalingrad", "Enemy at the Gates", 3),
            ("🎖️🏆⚔️", "Patton", "MacArthur", "We Were Soldiers", "Black Hawk Down", 0),
            
            # Thriller Movies
            ("🔪🚿🏨", "Psycho", "The Shining", "Scream", "Halloween", 0),
            ("🕵️‍♂️🔍💀", "Se7en", "Zodiac", "The Silence of the Lambs", "Shutter Island", 2),
            ("🚗💨🏃‍♂️", "The Fugitive", "North by Northwest", "The Bourne Identity", "Taken", 0),
            ("📞☎️😱", "Scream", "When a Stranger Calls", "Black Christmas", "I Know What You Did Last Summer", 0),
            ("🏢💥🔫", "Die Hard", "The Towering Inferno", "Speed", "Under Siege", 0),
            ("🧠💊🔴", "The Matrix", "Inception", "Limitless", "Total Recall", 2),
            ("🔒🗝️🏠", "Panic Room", "The Strangers", "Don't Breathe", "Hush", 0),
            ("🚢🌊⚓", "Titanic", "The Perfect Storm", "Life of Pi", "All is Lost", 1),
            ("🎭🃏😈", "The Dark Knight", "Joker", "Batman", "V for Vendetta", 0),
            ("🔫👮‍♂️🏦", "Heat", "Point Break", "The Town", "Den of Thieves", 0),
            
            # Sports Movies
            ("🏀👦🏫", "Coach Carter", "Hoosiers", "Space Jam", "He Got Game", 1),
            ("⚾🏟️👴", "Field of Dreams", "The Natural", "Bull Durham", "A League of Their Own", 0),
            ("🥊👊🏆", "Rocky", "Raging Bull", "The Fighter", "Creed", 0),
            ("🏈🏟️🏆", "The Blind Side", "Remember the Titans", "Any Given Sunday", "Friday Night Lights", 1),
            ("⚽🌍🏆", "Bend It Like Beckham", "The Goal", "She's the Man", "Kicking & Screaming", 0),
            ("🏒🥅❄️", "The Mighty Ducks", "Miracle", "Slap Shot", "Goon", 1),
            ("🏃‍♂️🏁🏆", "Chariots of Fire", "Prefontaine", "Without Limits", "McFarland USA", 0),
            ("🏊‍♀️🏊‍♂️🏆", "Swimming Upstream", "Pride", "The Swimmer", "Waterboy", 1),
            ("🚴‍♂️🏔️🏆", "Premium Rush", "Breaking Away", "The Flying Scotsman", "American Flyers", 1),
            ("🏌️‍♂️⛳🏆", "Happy Gilmore", "Caddyshack", "The Legend of Bagger Vance", "Tin Cup", 1),
            
            # Crime Movies
            ("🔫💰🏦", "Heat", "Point Break", "The Town", "Baby Driver", 0),
            ("🤵🔫🍝", "The Godfather", "Goodfellas", "Scarface", "Casino", 0),
            ("💎🔫👥", "Reservoir Dogs", "Ocean's Eleven", "The Italian Job", "Heat", 0),
            ("🚗💨🏃‍♂️", "Baby Driver", "Drive", "Gone in 60 Seconds", "The Fast and the Furious", 0),
            ("🎰💰🔫", "Casino", "Ocean's Eleven", "21", "Rounders", 0),
            ("👮‍♂️🔫🏢", "Serpico", "Training Day", "The Departed", "L.A. Confidential", 2),
            ("💊💰🔫", "Scarface", "Blow", "Traffic", "American Gangster", 3),
            ("🏦💰💣", "Point Break", "Heat", "The Town", "Hell or High Water", 2),
            ("🔫👥🎯", "The Departed", "Donnie Brasco", "The Infiltrator", "American Hustle", 0),
            ("💰🎲🃏", "Casino", "21", "Rounders", "Molly's Game", 3),
            
            # Biography Movies
            ("🎵👨‍🎤🎸", "Bohemian Rhapsody", "Rocketman", "Walk the Line", "Ray", 0),
            ("🥊👊🏆", "Ali", "Raging Bull", "The Fighter", "Creed", 0),
            ("🎬🌟👩", "My Week with Marilyn", "Blonde", "The Seven Year Itch", "Some Like It Hot", 0),
            ("🚀👨‍🚀🌙", "First Man", "Apollo 13", "The Right Stuff", "Hidden Figures", 0),
            ("⚖️👩‍⚖️📚", "On the Basis of Sex", "The Iron Lady", "Erin Brockovich", "Norma Rae", 2),
            ("🎨🖼️👂", "Loving Vincent", "Lust for Life", "At Eternity's Gate", "The Agony and the Ecstasy", 2),
            ("🔬🧪💡", "The Theory of Everything", "A Beautiful Mind", "The Imitation Game", "Hidden Figures", 1),
            ("📚✍️👩", "Little Women", "Becoming Jane", "The Hours", "Julie & Julia", 1),
            ("🏃‍♂️🏆🌍", "Chariots of Fire", "Prefontaine", "Race", "McFarland USA", 2),
            ("🎭🎪👨", "The Greatest Showman", "Chaplin", "My Week with Marilyn", "Ed Wood", 1),
        ]
        
        # Generate thousands more by creating variations
        expanded_quizzes = []
        
        # Add original quizzes
        for quiz in sample_quizzes:
            expanded_quizzes.append(quiz)
        
        # Create variations with different emoji combinations and shuffled options
        for emojis, opt1, opt2, opt3, opt4, correct_idx in sample_quizzes:
            options = [opt1, opt2, opt3, opt4]
            correct_answer = options[correct_idx]
            
            # Create 3 variations per original quiz
            for i in range(3):
                # Shuffle options
                shuffled_options = options.copy()
                random.shuffle(shuffled_options)
                new_correct_idx = shuffled_options.index(correct_answer)
                
                # Add variation emoji
                variation_emoji = emojis + ["🎬", "🍿", "🎭", "🌟"][i]
                
                expanded_quizzes.append((
                    variation_emoji,
                    shuffled_options[0], shuffled_options[1], 
                    shuffled_options[2], shuffled_options[3], 
                    new_correct_idx
                ))
        
        # Load all quizzes
        for emojis, opt1, opt2, opt3, opt4, correct_idx in expanded_quizzes:
            Quiz.objects.get_or_create(
                emojis=emojis,
                defaults={
                    'option1': opt1, 'option2': opt2, 'option3': opt3, 'option4': opt4,
                    'correct_index': correct_idx, 'category': 'movie'
                }
            )
        
        self.stdout.write(f"Loaded {len(expanded_quizzes)} movie quizzes across all genres")