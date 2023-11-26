def parse_articles_to_download(username, articles):
    f = open(f'{username}_articles.txt', 'w')
    f.write(f'Artigos de {username}\n\n')
    
    for article in articles:
        f.write('\n\n')
        f.write(f'Título: {article[1]}')
        f.write('\n\n')
        f.write(f'{article[5]}')
        f.write('\n\n')
        f.write(50 * '-')
    f.close()
    
    path = f'{username}_articles.txt'
    
    return path
