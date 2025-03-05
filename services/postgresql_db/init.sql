-- Création de la table des utilisateurs
CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL UNIQUE,  -- Contrôle de l'unicité des noms d'utilisateurs
    password TEXT NOT NULL  -- Stockage du mot de passe haché
);

-- Création de la table des notes
CREATE TABLE IF NOT EXISTS notes (
    date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    user_id INT NOT NULL,
    repo_link VARCHAR(255) NOT NULL,
    note INT CHECK (note >= 1 AND note <= 5),  -- Contrôle de validité des notes entre 1 et 5

    PRIMARY KEY (user_id, repo_link),  -- Clé primaire composite
    FOREIGN KEY (user_id) REFERENCES users(user_id)  -- Clé étrangère vers la table des utilisateurs
);

insert into users (username, password) values ('admin', 'admin');
