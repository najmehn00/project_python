from tkinter import Tk, Text, BOTH, W, N, E, S, Y, LEFT, NS, EW, StringVar, IntVar, messagebox
from tkinter.ttk import Frame, Button, Label, Entry, Style, Separator, Radiobutton
from instapy import InstaPy
from instapy.util import smart_run
from instapy import set_workspace
from instapy import get_workspace
from datetime import date, timedelta
from collections import Counter
import json
import os


def create_user(user_name):
    user_dict = list([user_name])
    if(not(os.path.exists('config'))):
        os.mkdir('config')
    with open('./config/user.json', 'w') as fout:
        json.dump(user_dict, fout)


def check_if_user_already_exists(path):
    if (not (os.path.exists(path))):
        return False
    else:
        return True


def get_user_data(path):
    f = open(path,)
    # returns JSON object as
    # a dictionary
    data = json.load(f)
    data = list(data)
    return data[0]


root = Tk()
root.geometry("410x420+300+300")
root.iconbitmap('icon.ico')

app = Frame(root)
bframe = Frame(root)


app.master.title("Smart Instagram Following Bot")
app.pack(fill=BOTH, expand=True)
bframe.pack(side='bottom', fill='x', expand=True)


app.columnconfigure(1, weight=1)

app.columnconfigure(0, pad=3)
app.columnconfigure(1, pad=3)

app.rowconfigure(0, pad=3)
app.rowconfigure(1, pad=3)
app.rowconfigure(2, pad=3)
app.rowconfigure(3, pad=3)
app.rowconfigure(4, pad=3)

lbl = Label(app, text="Login Username")
lbl.grid(row=0, column=0, sticky=W, pady=4, padx=5)
user = ''
if (check_if_user_already_exists('./config/user.json')):
    user = get_user_data('./config/user.json')
    login_username = Label(app, text=user)
else:
    login_username = Entry(app)


login_username.grid(row=1, column=0, padx=5, sticky=E+W+S+N)
login_username.focus_set()

login_password = Entry(app)
lbl = Label(app, text="Login Password")
lbl.grid(row=0, column=1, sticky=W, pady=4, padx=5)
login_password.grid(row=1, column=1, padx=5, sticky=E+W+S+N)

separator = Separator(app, orient='horizontal')
separator.grid(row=2, columnspan=2, padx=5, pady=10, sticky=(W, E))


lbl = Label(app, text="Desired User to perform on")
lbl.grid(row=3, column=0, sticky=W, pady=4, padx=5)
desire_user = Entry(app)
desire_user.grid(row=4, column=0, padx=5, sticky=E+W+S+N)


lbl = Label(app, text="Max users to follow (-1 for no limit)")
lbl.grid(row=3, column=1, sticky=W, pady=4, padx=5)
max_to_follow = Entry(app)
max_to_follow.grid(row=4, column=1, padx=5, sticky=E+W+S+N)

separator = Separator(app, orient='horizontal')
separator.grid(row=5, columnspan=2, padx=5, pady=10, sticky=(W, E))


lbl = Label(app, text="Users to follow contraints:")
lbl.grid(row=6, column=0, sticky=W, pady=4, padx=5)

lbl = Label(app, text="Potency Ratio (Suggestion: 1)")
lbl.grid(row=7, column=0, sticky=W, pady=4, padx=5)
potency_ratio = Entry(app)
potency_ratio.grid(row=8, column=0, padx=5, sticky=E+W+S+N)

lbl = Label(app, text="Max Following (Suggestion: 5000)")
lbl.grid(row=7, column=1, sticky=W, pady=4, padx=5)
max_following = Entry(app)
max_following.grid(row=8, column=1, padx=5, sticky=E+W+S+N)

lbl = Label(app, text="Max Followers (Suggestion: 50000)")
lbl.grid(row=9, column=0, sticky=W, pady=4, padx=5)
max_followers = Entry(app)
max_followers.grid(row=10, column=0, padx=5, sticky=E+W+S+N)

lbl = Label(app, text="Min Followers (Suggestion: 150)")
lbl.grid(row=9, column=1, sticky=W, pady=4, padx=5)
min_followers = Entry(app)
min_followers.grid(row=10, column=1, padx=5, sticky=E+W+S+N)

lbl = Label(app, text="Min Posts (Suggestion: 10)")
lbl.grid(row=11, column=0, sticky=W, pady=4, padx=5)
min_posts = Entry(app)
min_posts.grid(row=12, column=0, padx=5, sticky=E+W+S+N)
v = IntVar()
v.set(True)

lbl = Label(app, text="On:")
lbl.grid(row=13, column=0, sticky=W, pady=4, padx=5)

rb1 = Radiobutton(app,
                  text="Following",
                  variable=v,
                  value=True)
rb1.grid(row=14, column=0, padx=5, sticky=E+W+S+N)
rb2 = Radiobutton(app,
                  text="Followers",
                  variable=v,
                  value=False)
rb2.grid(row=14, column=1, padx=5, sticky=E+W+S+N)


def run_clicked():
    if check_inputs():
        Main_bot()

    else:
        messagebox.showerror("Error", "Check your entries, something is wrong")


def check_inputs():
    if(check_if_user_already_exists('./config/user.json')):
        if len(max_to_follow.get()) == 0 or len(login_password.get()) == 0 or len(desire_user.get()) == 0 or len(potency_ratio.get()) == 0 or len(max_following.get()) == 0 or len(max_followers.get()) == 0 or len(min_followers.get()) == 0 or len(min_posts.get()) == 0:
            return False
        else:
            return True

    else:
        if len(max_to_follow.get()) == 0 or len(login_username.get()) == 0 or len(login_password.get()) == 0 or len(desire_user.get()) == 0 or len(potency_ratio.get()) == 0 or len(max_following.get()) == 0 or len(max_followers.get()) == 0 or len(min_followers.get()) == 0 or len(min_posts.get()) == 0:
            return False
        else:
            return True


def Main_bot():

    # login credentials
    insta_password = login_password.get()

    if (not(check_if_user_already_exists('./config/user.json'))):
        user = login_username.get()
        insta_username = login_username.get()
        create_user(insta_username)
    else:
        insta_username = get_user_data('./config/user.json')

    # get an InstaPy session!
    # set headless_browser=True to run InstaPy in the background
    session = InstaPy(username=insta_username,
                      password=insta_password,
                      headless_browser=False)

    

    following = v.get()
    # # settings
    # time handling
    follow_per_hour = 10

    # process data
    desired_user = desire_user.get()

    global max_to_follow
    global potency_ratio
    global max_following
    global max_followers
    global min_followers
    global min_posts

    how_many_to_follow = int(max_to_follow.get())
    potency_ratio = int(potency_ratio.get())
    max_following = int(max_following.get())
    max_followers = int(max_followers.get())
    min_followers = int(min_followers.get())
    min_posts = int(min_posts.get())

    # data structures
    all_users_following = []

    #
    sleep_delay = 6000 / follow_per_hour

    # time
    today = date.today()
    yesterday = date.today() - timedelta(days=1)
    ereyesterday = date.today() - timedelta(days=2)
    today = today.strftime("%d-%m-%Y")
    yesterday = yesterday.strftime("%d-%m-%Y")
    ereyesterday = ereyesterday.strftime("%d-%m-%Y")

    # path
    workspace_in_use = get_workspace()
    workspace_path = workspace_in_use['path']
    username_path = workspace_path + '/logs/' + insta_username
    desired_user_path = username_path + '/relationship_data/' + desired_user

    def json_to_list(path):
        # Opening JSON file
        f = open(path,)

        # returns JSON object as
        # a dictionary
        data = json.load(f)
        data = list(data)
        return data

    def check_if_grabbed_already(path):
        return (os.path.exists(path)) and (any((fname.endswith('.json')) and ((fname.split('~')[0] == today) or (fname.split('~')[0] == yesterday) or (fname.split('~')[0] == ereyesterday)) for fname in os.listdir(path)))

    def check_if_generated_already(path):
        return (os.path.exists(path)) and (any((fname.endswith('.json')) and ((fname.split('~')[0] == today) or (fname.split('~')[0] == yesterday) or (fname.split('~')[0] == ereyesterday)) for fname in os.listdir(path)))

    def get_latest_json(path):
        path_files = os.listdir(path)
        json_files = list(
            filter(lambda item: item.endswith('.json'), path_files))
        json_path = path + '/' + json_files[0]
        return json_path

    def write_list_to_json_file(count_dict):
        with open('{}~{}~on{}~outputfile.json'.format(today, desired_user, ing_or_ers(following)), 'w') as fout:
            json.dump(count_dict, fout)

    def ing_or_ers(value):
        if value:
            return 'following'
        else:
            return 'followers'

    with smart_run(session):
        """ Activity flow """
        # # settings
        session.set_relationship_bounds(enabled=True, potency_ratio=potency_ratio, delimit_by_numbers=True,
                                        max_following=max_following, max_followers=max_followers, min_followers=min_followers, min_posts=min_posts)
        session.set_do_story(enabled=True, percentage=70, simulate=False)
        session.set_skip_users(skip_private=True,
                               skip_no_profile_pic=True,
                               no_profile_pic_percentage=100)

        # # relations

        if (following):
            desired_user_following_path = desired_user_path + '/following'

            if(check_if_grabbed_already(desired_user_following_path)):
                json_path = get_latest_json(desired_user_following_path)
                duser_following = json_to_list(json_path)
                print('desired user data exist')
            else:
                duser_following = session.grab_following(
                    username=desired_user, amount="full", live_match=True, store_locally=True)
            i = 0
            for user in duser_following:
                i += 1
                following_user_path = username_path + '/relationship_data/' + user
                following_user_following_path = following_user_path + '/following'
                if(check_if_grabbed_already(following_user_following_path)):
                    json_path = get_latest_json(following_user_following_path)
                    user_following = json_to_list(json_path)
                    print('user data exist')
                else:
                    user_following = session.grab_following(
                        username=user, amount="full", live_match=True, store_locally=True)

                if (user_following):
                    if desired_user in user_following:
                        user_following.remove(desired_user)
                    all_users_following.append(user_following)
                # if(i > 10):
                #     break

        else:
            desired_user_followers_path = desired_user_path + '/followers'

            if(check_if_grabbed_already(desired_user_followers_path)):
                json_path = get_latest_json(desired_user_followers_path)
                duser_followers = json_to_list(json_path)
                print('desired user data exist')
            else:
                duser_followers = session.grab_followers(
                    username=desired_user, amount="full", live_match=True, store_locally=True)
            i = 0
            for user in duser_followers:
                i += 1
                follower_user_path = username_path + '/relationship_data/' + user
                follower_user_following_path = follower_user_path + '/following'
                if(check_if_grabbed_already(follower_user_following_path)):
                    json_path = get_latest_json(follower_user_following_path)
                    user_following = json_to_list(json_path)
                    print('user data exist')
                else:
                    user_following = session.grab_following(
                        username=user, amount="full", live_match=True, store_locally=True)

                if (user_following):
                    if desired_user in user_following:
                        user_following.remove(desired_user)
                    all_users_following.append(user_following)

        flat_final_users_to_follow = [
            item for sublist in all_users_following for item in sublist]

        occurance_count = dict(Counter(flat_final_users_to_follow))
        occurance_count_sorted = dict(
            sorted(occurance_count.items(), key=lambda item: item[1], reverse=True))
        print(occurance_count_sorted)
        write_list_to_json_file(occurance_count_sorted)
        max_intersect = max(occurance_count.values())
        print("max_intersect:{}".format(max_intersect))
        desired_intersect_number = max_intersect * .2

        to_follow = []

        for key in occurance_count.keys():
            if (occurance_count[key] >= desired_intersect_number) and (occurance_count[key] > 1):
                to_follow.append(key)

        if(how_many_to_follow > len(to_follow) and how_many_to_follow != -1):
            how_many_to_follow = -1
        # # actions
        session.follow_by_list(followlist=to_follow, times=1,
                               sleep_delay=sleep_delay, interact=False)


obtn = Button(bframe, text="Run!", command=run_clicked)
obtn.pack()
root.mainloop()
