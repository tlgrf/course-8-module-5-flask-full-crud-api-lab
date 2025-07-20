from flask import Flask, jsonify, request

app = Flask(__name__)

# Simulated data
class Event:
    def __init__(self, id, title):
        self.id = id
        self.title = title

    def to_dict(self):
        return {"id": self.id, "title": self.title}

# In-memory "database"
events = [
    Event(1, "Tech Meetup"),
    Event(2, "Python Workshop")
]

# Root welcome route
@app.route("/", methods=["GET"])
def welcome():
    return jsonify({"message": "Welcome to the Event API!"}), 200

# READ all events
@app.route("/events", methods=["GET"])
def list_events():
    return jsonify([e.to_dict() for e in events]), 200

#CREATE: POST /events
@app.route("/events", methods=["POST"])
def create_event():
    #parse the JSON body and pull out the title
    data = request.get_json() or {}
    title = data.get("title")
    if not title:
        #Return and handle errors
        return jsonify({"error": "Missing 'title' field"}), 400
    #compute new ID and build the object
    new_id = max((e.id for e in events), default=0) + 1
    new_event = Event(new_id, title)
    events.append(new_event)
    #Return the result
    return jsonify(new_event.to_dict()), 201
 
#UPDATE: PATCH /events/<id>
@app.route("/events/<int:event_id>", methods=["PATCH"])
def update_event(event_id):
   # inline lookup
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    data = request.get_json() or {}
    if "title" in data:
        event.title = data["title"]
    return jsonify(event.to_dict()), 200

#DELETE: DELETE /events/<id>
@app.route("/events/<int:event_id>", methods=["DELETE"])
def delete_event(event_id):
    event = next((e for e in events if e.id == event_id), None)
    if not event:
        return jsonify({"error": "Event not found"}), 404

    events.remove(event)
    return "", 204

if __name__ == "__main__":
    app.run(debug=True)