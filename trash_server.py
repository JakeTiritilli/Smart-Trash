import flask
import flask_socketio
import trash_can_timer
import average_time


app = flask.Flask(__name__)
app.config["SECRET KEY"] = "cs190"
socketio = flask_socketio.SocketIO(app)

garbage_timer = trash_can_timer.TrashCanTimer("can1")
avg_time_calc = average_time.AverageTime("can1")

can_height = 0
contains_trash = False


def get_percent_full(trash_dist):
    if can_height == 0:
        return None
    else:
        can_height_inch = can_height * 12
        if trash_dist > can_height_inch:
            return 0
        else:
            trash_height = can_height_inch - trash_dist
            percent_full = (trash_height / can_height_inch) * 100
            percent_full = int(round(percent_full))
            if percent_full % 10:
                percent_full = percent_full + (10 - percent_full % 10)
            return percent_full


def set_timer(percent_full: int):
    global contains_trash
    if percent_full == 0:
        if not garbage_timer.is_in_progress() and not contains_trash:
            garbage_timer.set_start_time()
            socketio.emit("time", namespace = '/update')
        elif contains_trash:
            garbage_timer.set_taken_out()
            contains_trash = False
    elif percent_full == 100:
        garbage_timer.set_time_full()


def get_state(trash_dist, temp):
    global contains_trash
    socketio.emit('temp', {"temp": temp}, namespace = '/update')
    percent_full = get_percent_full(trash_dist)
    if percent_full != None:
        if percent_full > 0:
            contains_trash = True
        set_timer(percent_full)
        socketio.emit('dist', {"dist": percent_full}, namespace = '/update')


@app.route('/', methods = ['POST', 'GET'])
def result():
    if flask.request.method == 'POST':
        result = flask.request.get_json()
        print("Received Distance (in):", result["dist"])
        print("Received Temperature (F):", result["temp"])
        get_state(result["dist"], result["temp"])
        return "Received"
    else:
        return flask.render_template("form.html")
    
    
@app.route('/monitor', methods = ['POST', 'GET'])
def set_height():
    print(flask.request.form['height'])
    global can_height
    can_height = int(flask.request.form['height'])
    return flask.render_template("index.html")
    
    
@app.route('/stats')
def get_avg_stats():
    stats_dict = {"total": avg_time_calc.avg_trash_cycle(),
                  "after-full": avg_time_calc.avg_full_time(),
                  "before-full": avg_time_calc.avg_time_to_full(),
                  "highest-month": avg_time_calc.heighest_trash_month()
                 }
    return flask.json.jsonify(stats_dict)
    

@socketio.on('connect', namespace = '/update')
def sock_connect():
    print('Client connected')
    
    
@socketio.on('disconnect', namespace = '/update')
def sock_disconnect():
    print("Client Diconnected")
        

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0')
    #socketio.run(app) # Run only locally (127.0.0.1)
