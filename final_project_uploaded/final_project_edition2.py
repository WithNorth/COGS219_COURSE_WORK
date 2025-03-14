# 请输入Full name 用来区分csv file 中是否已有此位参与者 但是在做数据分析的时候会把Full name column 删去
# video 三个 随机random 挑一个 function1
# 播放视频 function2
# 问题顺序 8个 function3
# 播放问题 function4
# 记录至csv file function5


import time
import sys
import os
import random
from psychopy import visual,event,core,gui,clock
import pandas as pd


# get the participants names
participant_info = {'Participant Name': ''}
dialog = gui.DlgFromDict(dictionary=participant_info, title='Participant Information')

if not dialog.OK:
    core.quit()

participant_name = participant_info['Participant Name']

def select_random_video(video_files):
    if not isinstance(video_files, list) or len(video_files) == 0:
        raise ValueError("This is an empty list of video files!")
    
    # Select a random video from a video list
    return random.choice(video_files)


my_videos = ["video_list\Ten_Day_Ultimatum_with_no subtitles.mp4", 
             "video_list\Ten_Day_Ultimatum_with_subtitles_and_live_comments.mp4",
            "video_list/Ten_Day_Ultimatum_with_subtitles.mp4"]
selected_video = select_random_video(my_videos)
# Successfully get the selected video
print(f"Random video selected: {selected_video}")

win = visual.Window(size=(1920, 1080),fullscr=False,winType='pyglet',allowStencil=False,useFBO=True)


# create a new function to put into the past test py file 
def video_play(win,video_file):
    video_duration = None

    if os.path.exists(video_file):
        mov = visual.MovieStim(win,video_file,size=(1500,700),noAudio=False)

        try:
            video_duration = mov.duration
            print(f"Video duration: {video_duration} seconds")
        except (AttributeError, TypeError):
            # 11mins 6secs => 11 * 60 + 6 = 666
            video_duration = 666
            print(f"Error! We cannot automatically get video duration. Use manual setting: {video_duration} seconds")
    else:
        print(f"Error: Video file '{video_file}' does not exist")
        win.close()
        core.quit()

    global_clock = core.Clock()
    video_clock = core.Clock()

    print("Start playing video...")
    video_clock.reset()
    video_ended = False
    while not video_ended:
        if video_duration is not None and video_clock.getTime() >= 666.0:
            video_ended = True
            print("Video ended. (based on the time check)")
            break
        if mov.status == visual.FINISHED:
            video_ended = True
            print("Video ended. (based on the status check)")
            break

        mov.draw()
        win.flip()

        keys = event.getKeys(keyList=['escape', 'space'])
        if 'escape' in keys:
            win.close()
            core.quit()
        elif 'space' in keys:
            video_ended = True
            print("Video ended. (based on the manual check)")
            break

    try:
        if hasattr(mov, 'stop'):
            mov.stop()
    except Exception as e:
        print(f"Error: {e}")

# video play done
video_play(win,selected_video)

transition_text = visual.TextStim(
    win=win,
    text="The video ended. Please answer the questions given.",
    font='Arial',
    pos=(0, 0),
    height=0.06,
    wrapWidth=1.8,
    color='white'
)

transition_text.draw()
win.flip()
core.wait(2.0)

def present_questions(win, questions, participant_name, save_file=None):
    question_text = visual.TextStim(win, text='', height=0.05, pos=(0, 0.2), wrapWidth=1.5)
    options_text = visual.TextStim(win, text='', height=0.04, pos=(0, -0.2), wrapWidth=1.5)
    feedback_text = visual.TextStim(win, text='', height=0.05, pos=(0, -0.4), color='white')
    results = []
    
    for i, q in enumerate(questions):
        question_text.text = f"Question {i+1}/{len(questions)}:\n\n{q['question']}"
        
        if 'options' in q:
            options_str = "\n".join([f"{key}: {option}" for key, option in q['options'].items()])
            options_text.text = options_str
        else:
            options_text.text = ""
        
        question_text.draw()
        options_text.draw()
        win.flip()
        
        timer = clock.Clock()
        keys = event.waitKeys(keyList=None if 'options' not in q else list(q['options'].keys()),
                              timeStamped=timer)
        
        response_key, response_time = keys[0]
        response_time =  round(response_time * 1000)

        is_correct = response_key == q['correct_answer']

        if is_correct:
            feedback_text = visual.TextStim(win,text = "Correct!!!",font='Arial',pos=(0, 0),height=0.06,wrapWidth=1.8,color='white')
        else:
            feedback_text = visual.TextStim(win,text = "Incorrect~",font='Arial',pos=(0, 0),height=0.06,wrapWidth=1.8,color='white')

        feedback_text.draw()
        win.flip()
        core.wait(0.5)
        
        result = {
            'participant_name': participant_name,
            'question_number': i+1,
            'question': q['question'],
            'response': response_key,
            'correct_answer': q['correct_answer'],
            'is_correct': is_correct,
            'rt': response_time
        }
        results.append(result)
        
    if save_file:
        csv_file = save_file + '.csv'
        
        file_exists = os.path.isfile(csv_file)
        
        pd.DataFrame(results).to_csv(csv_file, mode='a', index=False, header=not file_exists)
        
    return results



questions_chinese = [
    {
        'question': '他们见到的第一位生肖是谁?',
        'options': {'a': '人羊', 'b': '地牛', 'c': '人龙', 'd': '地蛇','e':'地猴'},
        'correct_answer': 'a' # 人羊
    },
    {
        'question': '这里面介绍的人物中没有哪一个职业?',
        'options': {'a': '医生', 'b': '消防员', 'c': '刑警', 'd': '律师','e':'心理咨询师'},
        'correct_answer': 'b' #消防员
    },
    {
        'question': '仓库寻道这个游戏中，要求是几分钟内找到道(那一颗需要收集的球)?',
        'options': {'a': '十分钟', 'b': '二十分钟', 'c': '三分钟', 'd': '五分钟','e':'八分钟'},
        'correct_answer': 'd' #五分钟
    },    
    {
        'question': '人猪说它之前都是靠什么来过日子的?',
        'options': {'a': '运气', 'b': '力量', 'c': '毅力', 'd': '生命','e':'人脉'},
        'correct_answer': 'a' #运气
    },    
    {
        'question': '视频中曾解开的一次密码是什么?',
        'options': {'a': 'NI SHI HUN DAN', 'b': 'WO YAO HUO ZHE', 'c': 'JI DAO WAN SUI', 'd': 'HAPPY BIRTHDAY','e':'ZHANG GUAN MING YUN'},
        'correct_answer': 'c'
    },    
    {
        'question': '以下选项中没有出现过的游戏是?',
        'options': {'a': '四情扇', 'b': '蓬莱', 'c': '灾厄年', 'd': '顺手牵羊','e':'黑白棋'},
        'correct_answer': 'd' # 顺手牵羊
    },
    {
        'question': '掌管游戏 木牛流马 的是哪一个生肖?',
        'options': {'a': '地牛', 'b': '牛马', 'c': '人马', 'd': '地马','e':'人牛'},
        'correct_answer': 'd' #地马
    },
    {
        'question': '视频中提到的悟出的道理是 只要怎么样 就会相见?',
        'options': {'a': '冷静', 'b': '活着', 'c': '坚持', 'd': '勇敢','e':'想念'},
        'correct_answer': 'e'
    }
]


results = present_questions(win, questions_chinese, participant_name, save_file='participants_results')
for result in results:
    print(f"Question: {result['question']}")
    print(f"Response: {result['response']}, Correct: {result['is_correct']}, RT: {result['rt']:.3f}s")
    print("---")

ending_text = visual.TextStim(
    win=win,
    text="All questions have been answered. Thank you for your participation!",
    font='Arial',
    pos=(0, 0),
    height=0.06,
    wrapWidth=1.8,
    color='white'
)

ending_text.draw()
win.flip()
core.wait(2.0)

win.close()