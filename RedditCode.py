import praw
from collections import Counter


CLIENT_ID = 'Client id'
CLIENT_SECRET = 'client secret'
USER_AGENT = 'python:clientid:0.1 (by /u/username)'
reddit = praw.Reddit(client_id=CLIENT_ID,
                     client_secret=CLIENT_SECRET,
                     user_agent=USER_AGENT)

def get_hot_posts(subreddit_name, limit=10):
    subreddit = reddit.subreddit(subreddit_name)
    hot_posts = subreddit.hot(limit=limit)
    return hot_posts

def extract_keywords(title):
    title = title.lower()
    # Remove common words
    ignore_words = ['the', 'has','your','that','will','have','any','best','get','gets','world','time','it','devices','where','deal','til','was','system','year','million','media','world','app','help','need','only','work','there','their','which','would','had','his','old','when','big','some','power','been','other','then','test','why','made','getting','without','billion','then','were','control','against','than','ceo','next','it','human','it','john','most','this','just','not','used','life','study','they','people','cut','all','future','takes','off','after','about','set','uses','new','could','can','into','but','over','make','support','may','says','one','like','makes','years','from','how','tech','first','its','more','found','out','now','you','use','using','free','what','sources','a', 'in', 'on', 'is', 'are', 'and', 'of', 'to', 'for', 'with', '-', '(', ')', '[', ']']
    words = [word.strip('.,!?;:\'"') for word in title.split() if word not in ignore_words and len(word) > 2]
    return words

def analyze_trends(subreddit_names, num_posts=100): #post number
    all_keywords = []
    for sub_name in subreddit_names:
        hot_posts = get_hot_posts(sub_name, limit=num_posts)
        for post in hot_posts:
            keywords = extract_keywords(post.title)
            all_keywords.extend(keywords)

    keyword_counts = Counter(all_keywords)
    most_common_keywords = keyword_counts.most_common(30)  # Get the top 30 keywords
    return most_common_keywords

def main():
    """Main function to define subreddits, analyze trends, and write output to a file."""
    tech_subreddits = [ 'technology', 'truetech','DailyTechNewsShow','tech','technews','it','InsaneTechnology','AskTechnology','todayilearned','BigTech']
    output_filename = "output"  # Dosya

    try:
        with open(output_filename, "w", encoding="utf-8") as outfile:
            outfile.write(f"Analyzing hot posts from the following subreddits: {', '.join(tech_subreddits)}\n\n")

            trends = analyze_trends(tech_subreddits)

            if trends:
                outfile.write("Top trending tech topics:\n")
                for keyword, count in trends:
                    outfile.write(f"- {keyword}: {count} mentions\n")
            else:
                outfile.write("Could not identify any significant trends at the moment.\n")

        print(f"Trend analizi '{output_filename}' dosyasına kaydedildi.")

    except Exception as e:
        print(f"Bir hata oluştu: {e}")

if __name__ == "__main__":
    main()
