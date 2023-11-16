function fetchUpdate(articles, buttons) {
    console.log(articles, buttons)
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
        titleLabel.className = 'news-title update-body-content';
        titleLabel.id = 'title-content'
        titleLabel.textContent = title;
        titleLabel.contentEditable = true    

        let bodyParagraph = document.createElement('p');
        bodyParagraph.className = 'news-body news-content update-body-content';
        bodyParagraph.id = 'body-content'
        bodyParagraph.textContent = body;
        bodyParagraph.contentEditable = true    

        let authorParagraph = document.createElement('p');
        authorParagraph.className = 'news-body news-pub-date news-pub-author';
        authorParagraph.textContent = 'Autor: ' + author;

        // Adicionar elementos ao contêiner da notícia
        newsContainer.appendChild(titleLabel);
        newsContainer.appendChild(bodyParagraph);
        newsContainer.appendChild(authorParagraph);     
        
        if(buttons.sendUpdate) {
            let button = document.createElement('button');
            button.className = 'update-button send-update';
            button.id = 'update-button'
            button.textContent = 'Atualizar';
            buttonsContainer.appendChild(button);

            button.addEventListener('click', (e) => {
                newTitle = document.getElementById('title-content').innerHTML
                content = document.getElementById('body-content').innerHTML
                console.log(e, title, content)
                path = window.location.pathname
                window.location.href = `send_update/?old_title=${title}&news=${newTitle}&content=${content}`
            })
        }

        // Adicionar contêiner da notícia ao contêiner principal
        container.appendChild(newsContainer);
        newsContainer.appendChild(buttonsContainer)
       

    });
}



