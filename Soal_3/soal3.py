from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/soal/pretest', methods=['GET','POST'])
def home():
    data = {
        "nama": "mukidi",
        "email": "mukidi@ai.astra.co.id",
        "usia": "28 Tahun, 3 Bulan"
}
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, port=5000)