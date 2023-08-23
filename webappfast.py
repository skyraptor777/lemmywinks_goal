from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from lemmy import Lemmy


def construct_webdriver():
    options = Options()
    options.add_argument("--headless=new")
    driver = webdriver.Chrome(options=options)
    return driver
    

def check_goal(sel_driver, url):
    goal_dict = []
    sel_driver.get(url)
    commentary_set = sel_driver.find_elements(By.CSS_SELECTOR, "div[class^='commentary-item_commentary-item']")
    for comment in commentary_set:
        minute = "''"
        try:
            minute = comment.find_element(By.CSS_SELECTOR, "span[class^='commentary-item_minutes']").text.replace("'",'')
        except:
            continue
        
        other_text = comment.text.replace(minute,'')
        goal_dict.append({"minute":minute, "comment_text": other_text, "comment_type": ""})
    event_set = sel_driver.find_elements(By.CSS_SELECTOR, "div[class^='event_event-container']")
    for event in event_set:
        
        # Search to see what the element is 
        e_type = ''
        e_text = '' 
        minute = event.find_element(By.CSS_SELECTOR, "span[class^='event_minutes']").text.replace("'",'')
        all_e_text = event.text
        if "Substituion" in all_e_text: 
            pass
        elif "Goal" in all_e_text or 'goal' in all_e_text:
            player = event.find_element(By.CSS_SELECTOR, "div[class^='goal-event_container']").text
            team = minute = event.find_element(By.CSS_SELECTOR, "span[class^='team_team-name']").text
            e_text = f"Goal {team}; Scorer {player}"
            e_type = '⚽'
        goal_dict.append({"minute":minute, "comment_text": e_text, "comment_type": e_type})
        
        
    goal_dict = sorted(goal_dict, key=lambda d: d['minute']) 
    return goal_dict







def main_function(url):
    sel_driver = construct_webdriver()
    goal_details = check_goal(sel_driver, url)





app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/test1")
def hello_test1():
    sample_url = 'https://www.goal.com/en-us/match/west-ham-united-vs-chelsea/c8ow08cuo1jq6wzcxapl29tzo#commentary'
    main_function(sample_url)
    return "<p>Hello, test1!</p>"

@app.route("/test2")
def hello_test2():
    return "<p>Hello, test2!</p>"

# example docs
if __name__ == "__main__":
    app.run(debug=True)
    






















# Login to your account
lemmy = Lemmy("https://lemmy.ml")
lemmy.log_in("username_or_email", "password")

# Get a community ID
community_id = lemmy.discover_community("community_name")

# Get all posts from a community by ID
community_posts = lemmy.post.list(community_id=community_id)

# Get the modlog of your server
modlog = lemmy.modlog.get()

# Post a new publication on a community
lemmy.post.create(community_id=community_id, name="First Post!", body="This is the first community post.")