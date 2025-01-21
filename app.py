from flask import Flask, render_template, request, jsonify
import pandas as pd

app = Flask(__name__)

def load_games():
    try:
        # Excel dosyasını oku
        excel_file = 'xbox oyunları.xlsx'
        xls = pd.ExcelFile(excel_file)
        all_games = []
        
        # Her sayfayı ayrı ayrı oku (Paket sayfaları)
        for sheet_name in xls.sheet_names:
            if sheet_name.lower() != 'tüm paketler':
                try:
                    package_num = int(sheet_name.split()[-1])  # "Paket 1" -> 1
                    df = pd.read_excel(excel_file, sheet_name=sheet_name)
                    df['Paket'] = package_num
                    all_games.append(df)
                except:
                    continue
        
        if all_games:
            # Tüm oyunları birleştir ve alfabetik sırala
            combined_df = pd.concat(all_games, ignore_index=True)
            combined_df = combined_df.sort_values(['OyunAdı'])  # Oyun adına göre sırala
            games_dict = combined_df.to_dict('records')
            
            # Tüm paketler tablosu için oyunları alfabetik sırala
            all_packages = sorted(games_dict, key=lambda x: x['OyunAdı'])
            
            return {
                'games': games_dict,
                'all_packages': all_packages
            }
        return {'games': [], 'all_packages': []}
    
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return {'games': [], 'all_packages': []}

@app.route('/')
def index():
    data = load_games()
    games = data['games']
    all_packages = data['all_packages']
    packages = sorted(list(set(game['Paket'] for game in games))) if games else []
    return render_template('index.html', 
                         games=games, 
                         packages=packages, 
                         all_packages=all_packages)

@app.route('/search')
def search():
    query = request.args.get('q', '').lower()
    games = load_games()['games']
    results = [
        game for game in games 
        if query in str(game['OyunAdı']).lower()
    ]
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True) 
