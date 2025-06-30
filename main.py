from flask import Flask, render_template, request,jsonify
import wikipedia
import requests
import os
NASA_API_KEY = os.environ.get("NASA_API_KEY")

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/chatbot.html')
def chatbot():
    return render_template('chatbot.html')


@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question= data.get('question', '').lower().strip()
    if 'picture of the day' in question or 'apod' in question:
        try:
            url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
            response = requests.get(url).json()

            title = response.get('title', 'No title')
            explanation = response.get('explanation', 'No explanation available.')
            media_type = response.get('media_type', 'image')
            media_url = response.get('url', '')

            return jsonify({
                'answer': f"{title}\n\n{explanation}",
                'media_type': media_type,
                'media_url': media_url
            })
        except Exception as e:
            return jsonify({
                'answer': "NASA API failed.",
                'media_type': 'image',
                'media_url': 'https://apod.nasa.gov/apod/image/2506/UmbrellaGal_Alkuwari_960.png'
            })

    elif "picture of earth" in question or "earth" in question:
        
        try:
            
            # Step 1: Call EPIC API
            epic_url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_API_KEY}"
            epic_response = requests.get(epic_url).json()

            if not epic_response:
                raise Exception("No images returned")

            # Step 2: Get first image's info
            image_info = epic_response[0]
            image_name = image_info['image']
            date = image_info['date'].split(" ")[0]  # format: YYYY-MM-DD
            year, month, day = date.split("-")

        # Step 3: Construct the image URL
            media_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{image_name}.png"

            explanation = "This is a real-time natural-color image of Earth from NASA’s EPIC camera aboard DSCOVR."

            return jsonify({
            'answer': f"Earth as seen on {date}\n\n{explanation}",
            'media_type': 'image',
            'media_url': media_url
        })
        except Exception as e:
            pass
        # print("EPIC API error:", e)
        # return jsonify({
        #     'answer': "Sorry, I couldn't fetch an Earth image right now.",
        #     'media_type': 'image',
        #     'media_url': ''
        # })


    elif "Can humans live on Mars?" in question or "mars"in question:
        return jsonify({"answer":"Humans cannot currently live on Mars without significant technological support due to the planet's harsh conditions. But with advancements in technology, it is possible that humans could live on Mars in the future."})
    elif "solar syatem" in question :
        return jsonify({"answer":"The solar system is the gravitationally bound system comprising the Sun and the objects that orbit it, either directly or indirectly. Of those objects that orbit the Sun directly, the largest eight are the planets, with the remainder being"})
    elif "dark matter" in question:
        return jsonify({"answer":"Dark matter is a type of matter that is thought to account for approximately 27% of the total mass and energy in the universe. It is called dark because it does not interact with the electromagnetic force, and it therefore does not absorb, reflect, or emit light."})
    # Else, use Wikipedia
    else:
        try:
            summary = wikipedia.summary(question, sentences=2)
            return jsonify({'answer': summary})
        except wikipedia.exceptions.DisambiguationError as e:
            return jsonify({
                'answer':
                f"Your question is too broad. Try being more specific.\nOptions: {', '.join(e.options[:5])}"
            })
        except wikipedia.exceptions.PageError:
            return jsonify({
                'answer':
                "I couldn’t find anything related to that. Try rephrasing."
            })
        except Exception as e:
            return jsonify({'answer': "Something went wrong. Try again."})
if __name__ == '__main__':
    app.run(debug=True)
