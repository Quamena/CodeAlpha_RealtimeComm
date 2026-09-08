\# CodeAlpha\_RealtimeComm



A real-time video/audio communication app built with Django, Django Channels, and WebRTC. Supports mesh-style group calls for 3–6 participants in a shared room.



\*\*Live demo:\*\* https://codealpha-realtimecomm.onrender.com/call/testroom/

\*(Note: free-tier hosting spins down after inactivity — first load may take 30–60 seconds.)\*



\*\*Demo video:\*\* \[add your video link here]



\## Features



\- Real-time signaling over WebSockets using Django Channels (Daphne/ASGI)

\- Peer-to-peer audio/video calls using WebRTC (`RTCPeerConnection`)

\- Mesh architecture — supports 3–6 simultaneous participants in one room, each connected directly to every other peer

\- Dynamic video grid that adds/removes tiles as peers join and leave

\- STUN + TURN (Open Relay) configured for NAT traversal across different networks

\- Connection-state logging and automatic ICE restart on failed connections



\## Tech stack



\- Django 6.1

\- Django Channels 4 + Daphne (ASGI server)

\- Vanilla JavaScript (WebRTC APIs)

\- Deployed on Render (Python 3, free web service tier)



\## How it works



1\. A user opens `/call/<room\_name>/` — this joins a Channels group for that room over a WebSocket.

2\. When a new peer joins, the server broadcasts a `peer-joined` event to everyone already in the room.

3\. Existing peers each create an `RTCPeerConnection` and send a WebRTC offer directly to the new peer (targeted via their channel name).

4\. Offers, answers, and ICE candidates are relayed through the Django Channels consumer (`calls/consumers.py`), which routes messages either to a specific peer (`target`) or broadcasts them to the whole room.

5\. Once ICE negotiation completes, audio/video flows peer-to-peer (or via TURN relay if a direct path isn't possible).



\## Known limitations



\- \*\*Mesh topology\*\*: each peer connects directly to every other peer, so bandwidth/CPU usage scales with the number of participants. This is fine for small groups (3–6) but wouldn't scale to larger calls — a production app at scale would use an SFU (Selective Forwarding Unit) instead.

\- \*\*TURN reliability\*\*: this project uses a free, shared public TURN server (Open Relay). It works reliably for same-network or two-different-network calls; with 3+ participants on entirely different networks/locations, the shared relay can occasionally be unreliable. A dedicated TURN provider (e.g. Metered.ca, Twilio) would resolve this in a production setting.

\- \*\*Free-tier hosting\*\*: Render's free instance spins down after inactivity, causing a delay on first load.



\## Local setup



```bash

git clone https://github.com/Quamena/CodeAlpha\_RealtimeComm.git

cd CodeAlpha\_RealtimeComm

python -m venv myenv

myenv\\Scripts\\Activate.ps1   # Windows PowerShell

pip install -r requirements.txt

python manage.py migrate

python manage.py runserver

```



Then open `http://127.0.0.1:8000/call/testroom/` in multiple browser tabs to test.



\## Project structure



\- `realtimecomm/` — Django project settings, ASGI config

\- `calls/` — app containing the signaling consumer, room view, and template

&#x20; - `consumers.py` — WebSocket consumer handling signaling (offer/answer/ICE relay)

&#x20; - `templates/calls/room.html` — front-end WebRTC logic and video grid UI

