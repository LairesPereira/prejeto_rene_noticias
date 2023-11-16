function renderNews(articles) {
    console.log(articles)
    let container = document.getElementById('main');

    container.innerHTML = ''

    articles.forEach(function (article) {
        // Desestruturar os dados do artigo
        console.log(article)
        let [id, title, author, curtidas, removida, body] = article;

        // Criar um contêiner para cada notícia
        let newsContainer = document.createElement('div');
        newsContainer.className = 'news-container read-news';

        let buttonsContainer = document.createElement('div')
        buttonsContainer.className = 'buttons-container';

        // Criar elementos HTML para o título, corpo e autor
        let titleLabel = document.createElement('label');
        titleLabel.className = 'news-title';
        titleLabel.id = 'news-title';
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
        
        if(buttons.deleteOption) {
            let button = document.createElement('button');
            button.className = 'delete-button';
            button.id = 'delete-button'
            button.textContent = 'Deletar';
            buttonsContainer.appendChild(button);

            button.addEventListener('click', (e) => {
                console.log(title)
                path = window.location.pathname
                window.location.href = `delete_news_page/delete/?news=${title}`
            })
        }

        if(buttons.updateOption) {
            let button = document.createElement('button');
            button.className = 'update-button';
            button.id = 'update-button'
            button.textContent = 'Atualizar';
            buttonsContainer.appendChild(button);

            button.addEventListener('click', (e) => {
                console.log(title)
                path = window.location.pathname
                window.location.href = `update_news_page/?news=${title}`
            })
        }


        // Adicionar contêiner da notícia ao contêiner principal
        container.appendChild(newsContainer);
        newsContainer.appendChild(buttonsContainer)
        
        newsContainer.addEventListener('click', (e) => {
            title = document.getElementById('news-title').innerHTML
            console.log(title)
            path = window.location.pathname
            window.location.href = `/login/get_news/?news=${title}`
        })
       

    });
}

function getAllNews() {
    fetch('/login/news')
        .then(response => response.json())
        .then(data => renderNews(
            data, 
            buttons = {
            'deleteOption': false,
            'updateOption': false,
        }))
        .catch(error => console.error('Erro:', error));
}

