from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
port = 5000
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/test'
db = SQLAlchemy(app)

class Orang(db.Model):
    __tablename__ = 'orang'
    id = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(255))
    umur = db.Column(db.Integer)

@app.route('/', methods=['GET'])
def get_orang():
    orang_list = Orang.query.all()
    res = []
    for orang in orang_list:
        data = {
            'id': orang.id,
            'nama': orang.nama,
            'umur': orang.umur
        }
        res.append(data)
    return jsonify(res), 200

@app.route('/add', methods=['POST'])
def tambah_data():
    content_type = request.headers.get('Content-Type')

    # menerima json data dari paramsbody
    if content_type == 'application/json':
        data = request.get_json()
    elif content_type == 'application/x-www-form-urlencoded':
        data = request.form
    elif content_type == 'multipart/form-data':
        data = request.form
        files = request.files
        # Handle files jika diperlukan
    else:
        return jsonify({"error": "Unsupported Content-Type"}), 415

    # mengecek jika data tidak mengandung yang dicri
    if 'name' not in data or 'age' not in data:
        return jsonify({"error": "No data provided"}), 400

    # memberi nilai default jika data kosong
    name = data.get('name', 'Unknown')
    age = data.get('age', None)

    res = Orang(
        nama = data['name'],
        umur = data['age']
    )

    db.session.add(res)
    db.session.commit()

    return jsonify({
        'message': 'Data berhasil ditambahkan',
        'orang': {
            'nama': res.nama,
            'umur': res.umur
        }
    }), 200

@app.route('/delete/<int:id>', methods=['DELETE'])
def delete(id):
    id_orang = Orang.query.get_or_404(id)
    db.session.delete(id_orang)
    db.session.commit()

    return jsonify("Orang dengan id : "+str(id)+" telah dihapus")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port, debug=True)
