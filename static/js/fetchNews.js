function renderNews(articles) {
    let container = document.getElementById('main');

    container.innerHTML = ''

    articles.forEach(function (article) {
        // Desestruturar os dados do artigo
        console.log(article)
        let [id, title, author, curtidas, removida, body] = article;

        // Criar um contêiner para cada notícia
        let newsContainer = document.createElement('div');
        newsContainer.className = 'news-container read-news';

        // Criar elementos HTML para o título, corpo e autor
        let titleLabel = document.createElement('label');
        titleLabel.className = 'news-title';
        titleLabel.textContent = title;

        let bodyParagraph = document.createElement('p');
        bodyParagraph.className = 'news-body news-content';
        bodyParagraph.textContent = body;

        let authorParagraph = document.createElement('p');
        authorParagraph.className = 'news-body news-pub-date news-pub-author';
        authorParagraph.textContent = 'Autor: ' + author;

        // Adicionar elementos ao contêiner da notícia
        newsContainer.appendChild(titleLabel);
        newsContainer.appendChild(bodyParagraph);
        newsContainer.appendChild(authorParagraph);

        // Adicionar contêiner da notícia ao contêiner principal
        container.appendChild(newsContainer);

        // Adicionar um evento de click em cada contêiner de notícia para redirecionar 
        newsContainer.addEventListener('click', function() {
            path = window.location.pathname
            window.location.href = `${path}/get_news/?news=${title}`

            console.log('Notícia clicada: ', title);
            console.log(window.location.pathname);
        });
    });
}

function getAllNews() {
    fetch('/login/news')
        .then(response => response.json())
        .then(data => renderNews(data))
        .catch(error => console.error('Erro:', error));
}

