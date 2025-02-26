from psychopy import visual, core, event
import os
import time

video_file = "video1.mp4"

question = "How many cars are there in the video? (excluding the car we are driving)"
options = ["A. 1", "B. 2", "C. 3", "D. 4"]
correct_answer = "A"

video_duration = None

win = visual.Window(size=(1024, 768),fullscr=False,screen=0,winType='pyglet',allowGUI=False,allowStencil=False,monitor='testMonitor',
                    color=[0, 0, 0],colorSpace='rgb',blendMode='avg',useFBO=True)

if os.path.exists(video_file):
    mov = visual.MovieStim(win=win,filename=video_file,size=None,flipVert=False,flipHoriz=False,loop=False,noAudio=False)

    try:
        video_duration = mov.duration
        print(f"Video duration: {video_duration} seconds")
    except (AttributeError, TypeError):
        video_duration = 5.0
        print(f"Error! We cannot automatically get video duration. Use manual setting: {video_duration} seconds")
else:
    print(f"Error: Video file '{video_file}' does not exist")
    win.close()
    core.quit()

question_text = visual.TextStim(
    win=win,
    text=question,
    font='Arial',
    pos=(0, 0.3),
    height=0.05,
    wrapWidth=1.5,
    color='white'
)

option_texts = []
y_positions = [0.1, 0, -0.1, -0.2]
for i, option in enumerate(options):
    option_text = visual.TextStim(
        win=win,
        text=option,
        font='Arial',
        pos=(0, y_positions[i]),
        height=0.04,
        wrapWidth=1.5,
        color='white'
    )
    option_texts.append(option_text)

instruction_text = visual.TextStim(
    win=win,
    text="Please use the keyboard to select the correct answer.",
    font='Arial',
    pos=(0, 0.5),
    height=0.06,
    wrapWidth=1.8,
    color='white'
)

transition_text = visual.TextStim(
    win=win,
    text="The video ended. Please answer the question given.",
    font='Arial',
    pos=(0, 0),
    height=0.06,
    wrapWidth=1.8,
    color='white'
)

global_clock = core.Clock()
video_clock = core.Clock()

print("Start playing video...")
video_clock.reset()
video_ended = False
while not video_ended:
    if video_duration is not None and video_clock.getTime() >= 6.0:
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

# force to stop the video to avoid repeated playing the last frame

transition_text.draw()
win.flip()
core.wait(2.0)

print("Question is displayed. Waiting for the answer...")
global_clock.reset()
response = None
rt = None
while response is None:
    question_text.draw()
    for option_text in option_texts:
        option_text.draw()
    instruction_text.draw()
    win.flip()

    keys = event.getKeys(keyList = ['a', 'b', 'c', 'd', 'escape'], timeStamped=global_clock)

    if keys:
        for k in keys:
            if k[0] == 'escape':
                win.close()
                core.quit()
        for key, response_time in keys:
            if key in ['a', 'b', 'c', 'd']:
                response = key.upper()
                rt = response_time
                break

is_correct = (response == correct_answer) # return True or False
feedback_text = visual.TextStim(
    win=win,
    text=f"Your answer is {'correct' if is_correct else 'incorrect'}.",
    font='Arial',
    pos=(0, 0),
    height=0.06,
    wrapWidth=1.8,
    color='green' if is_correct else 'red'
)

print(f"Response: {response}, RT: {rt:.2f} seconds")
feedback_text.draw()
win.flip()
core.wait(1.0)

win.close()
core.quit()