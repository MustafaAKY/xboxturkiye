from flask import Flask, render_template, request, jsonify
import pandas as pd
import json

app = Flask(__name__)

def load_games():
    try:
        # Önce JSON dosyasını okumayı dene
        try:
            with open('XboxOyunları.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                games = data['games']
                return {
                    'games': games,
                    'all_packages': sorted(games, key=lambda x: x['OyunAdı'])
                }
        except:
            # JSON dosyası yoksa veya okuma hatası varsa Excel'den oku
            excel_file = 'xbox oyunları.xlsx'
            xls = pd.ExcelFile(excel_file)
            all_games = []
            
            # Her sayfayı ayrı ayrı oku (Paket sayfaları)
            for sheet_name in xls.sheet_names:
                if sheet_name.lower() != 'tüm paketler':
                    try:
                        package_num = int(sheet_name.split()[-1])
                        df = pd.read_excel(excel_file, sheet_name=sheet_name)
                        df['Paket'] = package_num
                        all_games.append(df)
                    except:
                        continue
            
            if all_games:
                # Tüm oyunları birleştir ve alfabetik sırala
                combined_df = pd.concat(all_games, ignore_index=True)
                combined_df = combined_df.sort_values(['OyunAdı'])
                
                # NaN değerleri None ile değiştir
                games_dict = combined_df.where(pd.notnull(combined_df), None).to_dict('records')
                
                # JSON dosyasını oluştur
                with open('XboxOyunları.json', 'w', encoding='utf-8') as f:
                    json.dump({'games': games_dict}, f, ensure_ascii=False, indent=2)
                
                return {
                    'games': games_dict,
                    'all_packages': sorted(games_dict, key=lambda x: x['OyunAdı'])
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
