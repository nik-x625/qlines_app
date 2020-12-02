from instaloader import Instaloader, Profile
import datetime

MAX_DAYS = 50

LIKES_WEIGHT = 1
COMMENTS_WEIGHT = 1
NUM_FOLLOWERS_WEIGHT = 1
NUM_POSTS_WEIGHT = 1

def get_summary(profile):
    user = {}
    # print('Engagement.get_summary: {}'.format(profile.username))
    user['followers'] = profile.followers
    # print('  Followers: {}'.format(profile.followers))

    total_num_likes = 0
    total_num_comments = 0
    total_num_posts = 0
    current_date = datetime.datetime.now()

    for post in profile.get_posts():
        delta = current_date - post.date
        if (delta.days > MAX_DAYS):
            break
        if (post.likes is not None):
            total_num_likes += post.likes
        if (post.comments is not None):
            total_num_comments += post.comments
        total_num_posts += 1
        # print('  {} - Number of Likes: {}, Number of Comments: {}, Post Date: {}'.format(total_num_posts, total_num_likes, total_num_comments, post.date))

    engagement = 0
    if profile.followers > 0 and total_num_posts > 0:
        engagement = float( (LIKES_WEIGHT * total_num_likes) + (COMMENTS_WEIGHT * total_num_comments)) / ((NUM_FOLLOWERS_WEIGHT * profile.followers) * (NUM_POSTS_WEIGHT * total_num_posts))
    user['engagement'] = engagement * 100
    # print('  Engagement: {}'.format(user['engagement']))
    user['num_recent_posts'] = total_num_posts
    # print('  Number of Recent Posts: {}'.format(user['num_recent_posts']))
    post_freq = 0.0
    if (total_num_posts > 0):
        post_freq = float(MAX_DAYS) / total_num_posts
    user['post_frequency'] = post_freq
    # print('  Recent Post Frequency: {}'.format(user['post_frequency']))
    return user

print('# xx: '+str(get_summary('mehdi.ix')))
