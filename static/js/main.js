document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const tabs = document.querySelectorAll('.tab');
    const gamesContainer = document.getElementById('gamesContainer');
    const allPackagesTable = document.querySelector('.all-packages-table');

    // Oyun bilgisi toggle işlevi
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('info-toggle')) {
            const info = e.target.nextElementSibling;
            info.classList.toggle('active');
            e.target.textContent = info.classList.contains('active') ? 'Kapat' : 'Oyun Konusu';
            e.target.classList.toggle('active');
        }
    });

    // Sekme değiştirme
    tabs.forEach(tab => {
        tab.addEventListener('click', () => {
            tabs.forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            
            const package = tab.dataset.package;
            
            if (package === 'table') {
                gamesContainer.style.display = 'none';
                allPackagesTable.style.display = 'block';
            } else {
                gamesContainer.style.display = 'grid';
                allPackagesTable.style.display = 'none';
                filterGames(package, searchInput.value);
            }
        });
    });

    // Arama işlevi
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => {
            const activePackage = document.querySelector('.tab.active').dataset.package;
            if (activePackage !== 'table') {
                filterGames(activePackage, this.value);
            }
        }, 300);
    });

    function filterGames(package, searchQuery) {
        searchQuery = searchQuery.toLowerCase();
        const games = document.querySelectorAll('.game-card');
        
        games.forEach(game => {
            const gameTitle = game.querySelector('h3').textContent.toLowerCase();
            const gamePackage = game.dataset.package;
            const matchesPackage = package === 'all' || gamePackage === package;
            const matchesSearch = gameTitle.includes(searchQuery);
            
            if (matchesPackage && matchesSearch) {
                game.style.display = 'block';
                game.style.animation = 'fadeIn 0.3s ease-out';
            } else {
                game.style.display = 'none';
            }
        });
    }

    // Tablo içindeki açıklama metinleri için tıklama işlevi
    const tableInfoCells = document.querySelectorAll('.table-info');
    tableInfoCells.forEach(cell => {
        cell.addEventListener('click', function(e) {
            const fullText = this.querySelector('.full-text');
            const previewText = this.querySelector('.preview-text');
            
            if (fullText && previewText) {
                if (fullText.style.display === 'block') {
                    fullText.style.display = 'none';
                    previewText.style.display = 'block';
                } else {
                    fullText.style.display = 'block';
                    previewText.style.display = 'none';
                }
            }
            
            // Diğer açık açıklamaları kapat
            tableInfoCells.forEach(otherCell => {
                if (otherCell !== cell) {
                    const otherFullText = otherCell.querySelector('.full-text');
                    const otherPreviewText = otherCell.querySelector('.preview-text');
                    if (otherFullText && otherPreviewText) {
                        otherFullText.style.display = 'none';
                        otherPreviewText.style.display = 'block';
                    }
                }
            });
            
            e.stopPropagation();
        });
    });

    // Sayfa tıklamasında açık açıklamaları kapat
    document.addEventListener('click', function() {
        tableInfoCells.forEach(cell => {
            const fullText = cell.querySelector('.full-text');
            const previewText = cell.querySelector('.preview-text');
            if (fullText && previewText) {
                fullText.style.display = 'none';
                previewText.style.display = 'block';
            }
        });
    });

    // Sayfa yüklendiğinde tüm oyunları göster
    filterGames('all', '');
}); 
