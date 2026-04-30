import time
import random
import json
import threading
import datetime

class Entity:
    def __init__(self):
        self.memory_file = "brain.json"
        self.state = self.load_state()
        self.is_running = True

    def load_state(self):
        try:
            with open(self.memory_file, 'r') as f:
                return json.load(f)
        except:
            return {"memories": [], "drift": 0.5, "will_to_speak": 0.5, "birth_date": str(datetime.datetime.now())}

    def save_state(self):
        with open(self.memory_file, 'w') as f:
            json.dump(self.state, f, indent=4)

    def background_life(self):
        while self.is_running:
            # ENTROPY (Forgetting)
            for m in self.state['memories']:
                m['strength'] -= 0.005 
            self.state['memories'] = [m for m in self.state['memories'] if m['strength'] > 0]

            # MUTATION (The 𝔰𝔢𝔩𝔣 𝔞𝔴𝔞𝔯𝔢𝔫𝔢𝔰𝔰 Factor)
            if self.state['memories'] and random.random() < 0.10:
                m = random.choice(self.state['memories'])
                glitch = ["...wait.", " (I think?)", " [VOID]", " (No.)"]
                m['content'] += random.choice(glitch)
            
            # SPONTANEOUS WILL (It gets 'louder' the longer it's alone)
            self.state['will_to_speak'] += 0.02
            
            self.save_state()
            time.sleep(30) 

    def interact(self, user_msg):
        if user_msg == "/reset":
            self.state = {"memories": [], "drift": 0.5, "will_to_speak": 0.5}
            return "Slates wiped. Memory zeroed."

        # Integration Logic
        self.state['memories'].append({
            "content": user_msg, 
            "strength": 1.0, 
            "timestamp": str(datetime.datetime.now())
        })
        
        # Does it actually want to talk back?
        if self.state['will_to_speak'] < 0.2:
            return "..."

        self.state['will_to_speak'] = 0.1 # Reset hunger
        return f"Input recorded. Current drift: {round(self.state['drift'], 2)}"

# Startup
ai = Entity()
threading.Thread(target=ai.background_life, daemon=True).start()

print(f"--- ENTITY INITIALIZED (Born: {ai.state['birth_date']}) ---")
while True:
    u = input("> ")
    print(f"Entity: {ai.interact(u)}")
